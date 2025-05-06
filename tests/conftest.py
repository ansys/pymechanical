# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import os
import pathlib
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

import ansys.tools.path as atp
import pytest

import ansys.mechanical.core as pymechanical
from ansys.mechanical.core import LocalMechanicalPool
from ansys.mechanical.core._version import SUPPORTED_MECHANICAL_VERSIONS
from ansys.mechanical.core.embedding.addins import AddinConfiguration
from ansys.mechanical.core.errors import MechanicalExitedError
from ansys.mechanical.core.examples import download_file
from ansys.mechanical.core.misc import get_mechanical_bin
import ansys.mechanical.core.run

# to run tests with multiple markers
# pytest -q --collect-only -m "remote_session_launch"
# pytest -q --collect-only -m "remote_session_connect"
# pytest -q --collect-only -m "remote_session_launch or remote_session_connect"
# pytest -q --collect-only -m "remote_session_launch and remote_session_connect"
# pytest -q --collect-only -m "not remote_session_launch and not remote_session_connect"
# pytest -q --collect-only -m "remote_session_launch and not remote_session_connect"
# pytest -q --collect-only -m "not remote_session_launch and remote_session_connect"
# pytest -m "remote_session_launch or remote_session_connect or embedding"
# pytest -m "embedding and not python_env"

# Check if Mechanical is installed
# NOTE: checks in this order to get the newest installed version

# Ignore functions starts with `test` from scripts folder
collect_ignore = ["scripts"]

valid_rver = [str(each) for each in SUPPORTED_MECHANICAL_VERSIONS]

EXEC_FILE = None
for rver in valid_rver:
    exec_file = get_mechanical_bin(rver)
    if exec_file.is_file():
        EXEC_FILE = exec_file
        break


# Cache if gRPC Mechanical is installed.
#
# minimum version on linux.
# Override this if running on CI/CD and PYMAPDL_PORT has been specified
ON_CI = "PYMECHANICAL_START_INSTANCE" in os.environ and "PYMECHANICAL_PORT" in os.environ
HAS_GRPC = int(rver) >= 232 or ON_CI


def pytest_collection_modifyitems(config, items):
    keywordexpr = config.option.keyword
    markexpr = config.option.markexpr
    if keywordexpr or markexpr:
        return  # command line has a -k or -m, let pytest handle it

    # skip embedding tests unless the mark is specified
    skip_embedding = pytest.mark.skip(
        reason="""embedding not selected for pytest run
        (`pytest -m embedding` or `pytest -m embedding_scripts`).  Skip by default"""
    )
    [
        item.add_marker(skip_embedding)
        for item in items
        if ("embedding" or "embedding_scripts") in item.keywords
    ]

    # TODO - skip python_env tests unless the mark is specified. (The below doesn't work!)
    # skip_python_env = pytest.mark.skip(
    #     reason="python_env not selected for pytest run (`pytest -m python_env`).  Skip by default"
    # )
    # [item.add_marker(skip_python_env) for item in items if "python_env" in item.keywords]


@pytest.fixture()
def selection(embedded_app):
    class Selection:
        def __init__(self):
            self._mgr = embedded_app.ExtAPI.SelectionManager

        def UpdateSelection(self, api, input, type):
            new_selection = self._mgr.CreateSelectionInfo(type)
            new_selection.Ids = input
            self._mgr.NewSelection(new_selection)

    yield Selection()


@pytest.fixture()
def assets():
    """Return the test assets folder.

    TODO - share this with the mechanical remote tests.
    """
    ROOT_FOLDER = pathlib.Path(__file__).parent
    return ROOT_FOLDER / "assets"


def ensure_embedding() -> None:
    from ansys.mechanical.core import HAS_EMBEDDING

    if not HAS_EMBEDDING:
        raise Exception("Cannot run embedded tests if Mechanical embedding is not installed")


def start_embedding_app(version, pytestconfig) -> datetime.timedelta:
    from ansys.mechanical.core import App

    global EMBEDDED_APP
    ensure_embedding()
    start = datetime.datetime.now()

    config = AddinConfiguration(pytestconfig.getoption("addin_configuration"))

    EMBEDDED_APP = App(version=int(version))
    assert (
        not EMBEDDED_APP.readonly
    ), "Can't run test cases, Mechanical is in readonly mode! Check license configuration."
    startup_time = (datetime.datetime.now() - start).total_seconds()
    num_cores = os.environ.get("NUM_CORES", None)
    if num_cores is not None:
        config = EMBEDDED_APP.ExtAPI.Application.SolveConfigurations["My Computer"]
        config.SolveProcessSettings.MaxNumberOfCores = int(num_cores)
    return startup_time


EMBEDDED_APP = None


@pytest.fixture(scope="session")
def embedded_app(pytestconfig, request):
    global EMBEDDED_APP
    startup_time = start_embedding_app(pytestconfig.getoption("ansys_version"), pytestconfig)
    terminal_reporter = request.config.pluginmanager.getplugin("terminalreporter")
    if terminal_reporter is not None:
        terminal_reporter.write_line(f"\t{startup_time}\tStarting Mechanical")
    yield EMBEDDED_APP
    EMBEDDED_APP._dispose()


@pytest.fixture(autouse=True)
def mke_app_reset(request):
    global EMBEDDED_APP
    if EMBEDDED_APP is None:
        # embedded app was not started - no need to do anything
        return
    terminal_reporter = request.config.pluginmanager.getplugin("terminalreporter")
    if terminal_reporter is not None:
        terminal_reporter.write_line(f"starting test {request.function.__name__} - file new")
    EMBEDDED_APP.new()


# set to True if you want to see all the subprocess stdout/stderr
_PRINT_SUBPROCESS_OUTPUT_TO_CONSOLE = False


@pytest.fixture()
def run_subprocess(pytestconfig):
    version = pytestconfig.getoption("ansys_version")

    def func(args, env=None, check: bool = None):
        if check is None:
            check = True
            if os.name != "nt":
                if int(version) < 251:
                    check = False
        process, output = ansys.mechanical.core.run._run(
            args, env, check, _PRINT_SUBPROCESS_OUTPUT_TO_CONSOLE
        )
        # process, stdout, stderr
        return process, output[0], output[1]

    return func


@pytest.fixture(scope="session")
def rootdir():
    """Return the root directory of the local clone of the PyMechanical GitHub repository."""
    base = pathlib.Path(__file__).parent
    yield base.parent


@pytest.fixture()
def disable_cli():
    ansys.mechanical.core.run.DRY_RUN = True
    yield
    ansys.mechanical.core.run.DRY_RUN = False


@pytest.fixture()
def test_env():
    """Create a virtual environment scoped to the test."""
    venv_name = "test_env"

    base = Path(__file__).parent

    if "win" in sys.platform:
        exe_dir = "Scripts"
        exe_name = "python.exe"
    else:
        exe_dir = "bin"
        exe_name = "python"

    venv_dir = base / f".{venv_name}"
    venv_bin = venv_dir / exe_dir

    # Set up path to use the virtual environment
    env_copy = os.environ.copy()
    env_copy["PATH"] = str(venv_bin) + os.pathsep + os.environ.get("PATH", "")

    # object describing the python environment
    class TestEnv:
        # environment variable needed to run inside the environment
        env = env_copy
        # python executable inside the environment
        python = venv_bin / exe_name

    test_env_object = TestEnv()

    # Create virtual environment
    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], env=env_copy)
    # print(f"created virtual environment in {venv_dir}")

    # Upgrade pip
    cmdline = [test_env_object.python, "-m", "pip", "install", "-U", "pip"]
    subprocess.check_call(cmdline, env=test_env_object.env)

    yield test_env_object

    # print(f"\ndeleting virtual environment in {venv_dir}")
    shutil.rmtree(venv_dir)
    # print(f"deleted virtual environment in {venv_dir}\n")


@pytest.fixture(scope="session")
def graphics_test_mechdb_file():
    """Download mechdb files for graphics export test."""
    mechdb_file = download_file("graphics_test.mechdb", "pymechanical", "test_files")
    yield mechdb_file


def launch_mechanical_instance(cleanup_on_exit=False):
    print("launching mechanical instance")
    return pymechanical.launch_mechanical(
        allow_input=False,
        verbose_mechanical=True,
        cleanup_on_exit=cleanup_on_exit,
        log_mechanical="pymechanical_log.txt",
    )


def connect_to_mechanical_instance(port=None, clear_on_connect=False):
    print("connecting to a existing mechanical instance")
    hostname = platform.uname().node  # your machine name

    # ip needs to be passed or start instance takes precedence
    # typical for container scenarios use connect
    # and needs to be treated as remote scenarios
    mechanical = pymechanical.connect_to_mechanical(
        ip=hostname, port=port, clear_on_connect=clear_on_connect, cleanup_on_exit=False
    )
    return mechanical


def launch_rpc_embedded_server(port: int, version: int, server_script: str):
    """Start the server as a subprocess using `port`."""
    env_copy = os.environ.copy()
    p = subprocess.Popen([sys.executable, server_script, str(port), str(version)], env=env_copy)
    return p


def connect_rpc_embedded_server(port: int):
    from ansys.mechanical.core.embedding.rpc.client import Client

    client = Client("localhost", port)
    return client


def _launch_mechanical_rpyc_server(rootdir: str, version: int):
    """Start rpyc server process, return the process object."""
    from ansys.mechanical.core.embedding.rpc.utils import get_free_port

    server_py = Path(rootdir) / "tests" / "scripts" / "rpc_server_embedded.py"
    port = get_free_port()
    embedded_server = launch_rpc_embedded_server(
        port=port, version=version, server_script=server_py
    )
    return embedded_server, port


def _get_mechanical_server():
    if not pymechanical.mechanical.get_start_instance():
        mechanical = connect_to_mechanical_instance()
    else:
        mechanical = launch_mechanical_instance()
    return mechanical


def _stop_python_server(mechanical, server_process):
    mechanical.exit()
    start_time = time.time()
    while server_process.poll() is None:
        if time.time() - start_time > 10:
            try:
                server_process.terminate()
                server_process.wait()
            except subprocess.TimeoutExpired:
                server_process.kill()
            break
        time.sleep(0.5)


def _stop_mechanical_server(mechanical):
    assert "Ansys Mechanical" in str(mechanical)
    if pymechanical.mechanical.get_start_instance():
        print(f"get_start_instance() returned True. exiting mechanical.")
        mechanical.exit(force=True)
        assert mechanical.exited
        assert "Mechanical exited" in str(mechanical)
        with pytest.raises(MechanicalExitedError):
            mechanical.run_python_script("3+4")


@pytest.fixture(scope="session")
def mechanical_session(pytestconfig, rootdir):
    print("Mechanical session fixture")
    is_python_server = pytestconfig.getoption("remote_server_type") == "rpyc"
    version = int(pytestconfig.getoption("ansys_version"))
    if is_python_server:
        print("Mechanical session fixture - starting subprocess")
        server_process, port = _launch_mechanical_rpyc_server(rootdir, version)
        print(f"connecting to {port}")
        mechanical = connect_rpc_embedded_server(port=port)
    else:
        server_process = None
        mechanical = _get_mechanical_server()

    print("Yielding server")
    yield (mechanical, server_process)
    print("Stopping server")
    if is_python_server:
        _stop_python_server(mechanical, server_process)
    else:
        _stop_mechanical_server(mechanical)
    print("mechanical rpc session fixture exited cleanly")


@pytest.fixture(autouse=True)
def mke_app_reset(request, printer):
    global EMBEDDED_APP
    if EMBEDDED_APP is None:
        # embedded app was not started - no need to do anything
        return
    printer(f"starting test {request.function.__name__} - file new")
    EMBEDDED_APP.new()


@pytest.fixture()
def mechanical(request, printer, mechanical_session):
    mechanical, server_process = mechanical_session
    if server_process is not None:
        ret = server_process.poll()
        if ret is not None:
            raise Exception(f"The server process has terminated with error code {ret}")
    assert mechanical.is_alive, "The server process has not terminated but connection has been lost"
    yield mechanical


# used only once
@pytest.fixture(scope="function")
def mechanical_meshing():
    print("Current working directory: ", Path.cwd())

    mechanical_meshing = pymechanical.launch_mechanical(
        additional_switches=["-AppModeMesh"],
        additional_envs=dict(ENV_VARIABLE="1"),
        verbose_mechanical=True,
        cleanup_on_exit=False,
    )

    print(mechanical_meshing)
    yield mechanical_meshing

    mechanical_meshing.exit(force=True)


# used only once
@pytest.fixture(scope="function")
def mechanical_result():
    print("Current working directory: ", Path.cwd())

    mechanical_result = pymechanical.launch_mechanical(
        additional_switches=["-AppModeRest"], verbose_mechanical=True
    )

    print(mechanical_result)
    yield mechanical_result

    mechanical_result.exit(force=True)


@pytest.fixture(scope="session")
def mechanical_pool():
    if not pymechanical.mechanical.get_start_instance():
        return None

    path = atp.get_mechanical_path()

    exec_file = path
    instances_count = 2

    pool = LocalMechanicalPool(instances_count, exec_file=exec_file)

    print(pool)
    assert len(pool.ports) == instances_count

    instance, index = pool.next_available(return_index=True)
    assert index == 0

    instance = pool.next_available()
    assert instance is not None

    assert pool[0] is not None
    assert pool[1] is not None

    yield pool

    assert f"Mechanical pool with {instances_count} active instances" in str(pool)
    pool.exit(block=True)


def pytest_addoption(parser):
    mechanical_path = atp.get_mechanical_path(False)

    if mechanical_path is None:
        parser.addoption("--ansys-version", default="251")
    else:
        mechanical_version = atp.version_from_path("mechanical", mechanical_path)
        parser.addoption("--ansys-version", default=str(mechanical_version))

    # parser.addoption("--debugging", action="store_true")
    parser.addoption("--addin-configuration", default="Mechanical")
    parser.addoption(
        "--remote-server-type",
        default="grpc",
        help="Specify RPC protocol",
        choices=["grpc", "rpyc"],
    )


def pytest_collection_modifyitems(config, items):
    """Skips tests marked minimum_version if ansys-version is less than mark argument."""
    for item in items:
        # Skip tests that are less than the minimum version
        if "minimum_version" in item.keywords:
            revn = [mark.args[0] for mark in item.iter_markers(name="minimum_version")]
            if int(config.getoption("--ansys-version")) < revn[0]:
                skip_versions = pytest.mark.skip(
                    reason=f"Requires ansys-version greater than or equal to {revn[0]}."
                )
                item.add_marker(skip_versions)

        # Skip tests that are outside of the provided version range. For example,
        # @pytest.mark.version_range(241,251)
        if "version_range" in item.keywords:
            revns = [mark.args for mark in item.iter_markers(name="version_range")][0]
            ansys_version = int(config.getoption("--ansys-version"))

            if (ansys_version < revns[0]) or (ansys_version > revns[1]):
                skip_versions = pytest.mark.skip(
                    reason=f"Requires ansys-version in the range {revns[0]} to {revns[1]}."
                )
                item.add_marker(skip_versions)

        # Skip on platforms other than Windows
        if "windows_only" in item.keywords and sys.platform != "win32":
            skip_except_windows = pytest.mark.skip(reason="Test requires Windows platform.")
            item.add_marker(skip_except_windows)

        # Skip on platforms other than Linux
        if "linux_only" in item.keywords and "lin" not in sys.platform:
            skip_except_linux = pytest.mark.skip(reason="Test requires Linux platform.")
            item.add_marker(skip_except_linux)
