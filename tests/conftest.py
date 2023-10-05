import datetime
import os
import pathlib
import platform
import shutil
import subprocess
import sys

import ansys.tools.path
import pytest

import ansys.mechanical.core as pymechanical
from ansys.mechanical.core import LocalMechanicalPool
from ansys.mechanical.core._version import SUPPORTED_MECHANICAL_VERSIONS
from ansys.mechanical.core.embedding.addins import AddinConfiguration
from ansys.mechanical.core.errors import MechanicalExitedError
from ansys.mechanical.core.misc import get_mechanical_bin

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


valid_rver = [str(each) for each in SUPPORTED_MECHANICAL_VERSIONS]

EXEC_FILE = None
for rver in valid_rver:
    if os.path.isfile(get_mechanical_bin(rver)):
        EXEC_FILE = get_mechanical_bin(rver)
        break


# Cache if gRPC Mechanical is installed.
#
# minimum version on linux.
# Override this if running on CI/CD and PYMAPDL_PORT has been specified
ON_CI = "PYMECHANICAL_START_INSTANCE" in os.environ and "PYMECHANICAL_PORT" in os.environ
HAS_GRPC = int(rver) >= 231 or ON_CI


def pytest_collection_modifyitems(config, items):
    keywordexpr = config.option.keyword
    markexpr = config.option.markexpr
    if keywordexpr or markexpr:
        return  # command line has a -k or -m, let pytest handle it

    # skip embedding tests unless the mark is specified
    skip_embedding = pytest.mark.skip(
        reason="embedding not selected for pytest run (`pytest -m embedding`).  Skip by default"
    )
    [item.add_marker(skip_embedding) for item in items if "embedding" in item.keywords]

    # TODO - skip python_env tests unless the mark is specified. (The below doesn't work!)
    # skip_python_env = pytest.mark.skip(
    #     reason="python_env not selected for pytest run (`pytest -m python_env`).  Skip by default"
    # )
    # [item.add_marker(skip_python_env) for item in items if "python_env" in item.keywords]


@pytest.fixture()
def selection(embedded_app):
    from ansys.mechanical.core import global_variables

    globals().update(global_variables(embedded_app))

    class Selection:
        def __init__(self):
            self._mgr = ExtAPI.SelectionManager

        def UpdateSelection(self, api, input, type):
            new_selection = self._mgr.CreateSelectionInfo(type)
            new_selection.Ids = input
            self._mgr.NewSelection(new_selection)

    yield Selection()


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
    if num_cores != None:
        num_cores = int(num_cores)
        config = EMBEDDED_APP.ExtAPI.Application.SolveConfigurations["My Computer"]
        config.SolveProcessSettings.MaxNumberOfCores = 2
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
    if EMBEDDED_APP == None:
        # embedded app was not started - no need to do anything
        return
    terminal_reporter = request.config.pluginmanager.getplugin("terminalreporter")
    if terminal_reporter is not None:
        terminal_reporter.write_line(f"starting test {request.function.__name__} - file new")
    EMBEDDED_APP.new()


@pytest.fixture()
def rootdir():
    """Return the root directory of the local clone of the PyMechanical GitHub repository."""
    base = pathlib.Path(__file__).parent
    yield base.parent


@pytest.fixture()
def test_env():
    """Create a virtual environment scoped to the test."""
    venv_name = "test_env"

    base = pathlib.Path(__file__).parent

    if "win" in sys.platform:
        exe_dir = "Scripts"
        exe_name = "python.exe"
    else:
        exe_dir = "bin"
        exe_name = "python"

    venv_dir = os.path.join(base, "." + venv_name)
    venv_bin = os.path.join(venv_dir, exe_dir)

    # Set up path to use the virtual environment
    env_copy = os.environ.copy()
    env_copy["PATH"] = venv_bin + os.pathsep + os.environ.get("PATH", "")

    # object describing the python environment
    class TestEnv:
        # environment variable needed to run inside the environment
        env = env_copy
        # python executable inside the environment
        python = os.path.join(venv_bin, exe_name)

    test_env_object = TestEnv()

    # Create virtual environment
    subprocess.run([sys.executable, "-m", "venv", venv_dir], env=env_copy)
    # print(f"created virtual environment in {venv_dir}")

    # Upgrade pip
    cmdline = [test_env_object.python, "-m", "pip", "install", "-U", "pip"]
    subprocess.check_call(cmdline, env=test_env_object.env)

    yield test_env_object

    # print(f"\ndeleting virtual environment in {venv_dir}")
    shutil.rmtree(venv_dir)
    # print(f"deleted virtual environment in {venv_dir}\n")


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
    mechanical = pymechanical.launch_mechanical(
        ip=hostname, port=port, clear_on_connect=clear_on_connect, cleanup_on_exit=False
    )
    return mechanical


@pytest.fixture(scope="session")
def mechanical():
    print("current working directory: ", os.getcwd())

    if not pymechanical.mechanical.get_start_instance():
        mechanical = connect_to_mechanical_instance()
    else:
        mechanical = launch_mechanical_instance()

    print(mechanical)
    yield mechanical

    assert "Ansys Mechanical" in str(mechanical)

    if pymechanical.mechanical.get_start_instance():
        print(f"get_start_instance() returned True. exiting mechanical.")
        mechanical.exit(force=True)
        assert mechanical.exited
        assert "Mechanical exited" in str(mechanical)
        with pytest.raises(MechanicalExitedError):
            mechanical.run_python_script("3+4")


# used only once
@pytest.fixture(scope="function")
def mechanical_meshing():
    print("current working directory: ", os.getcwd())

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
    print("current working directory: ", os.getcwd())

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

    path, version = ansys.tools.path.find_mechanical()

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
    # parser.addoption("--debugging", action="store_true")
    parser.addoption("--ansys-version", default="232")
    parser.addoption("--addin-configuration", default="Mechanical")


def pytest_collection_modifyitems(config, items):
    """Skips tests marked minimum_version if ansys-version is less than mark argument."""
    for item in items:
        if "minimum_version" in item.keywords:
            revn = [mark.args[0] for mark in item.iter_markers(name="minimum_version")]
            if int(config.getoption("--ansys-version")) < revn[0]:
                skip_versions = pytest.mark.skip(
                    reason=f"Requires ansys-version greater than or equal to {revn[0]}."
                )
                item.add_marker(skip_versions)
