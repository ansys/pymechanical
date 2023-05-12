import datetime
import os
import platform

import ansys.tools.path
import pytest

import ansys.mechanical.core as pymechanical
from ansys.mechanical.core import LocalMechanicalPool
from ansys.mechanical.core._version import SUPPORTED_MECHANICAL_VERSIONS
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
    skip_embedding = pytest.mark.skip(
        reason="embedding not selected for pytest run (`pytest -m embedding`).  Skip by default"
    )
    [item.add_marker(skip_embedding) for item in items if "embedding" in item.keywords]


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


def start_embedding_app() -> datetime.timedelta:
    from ansys.mechanical.core import App

    global EMBEDDED_APP
    ensure_embedding()
    start = datetime.datetime.now()
    EMBEDDED_APP = App(version=232)
    startup_time = (datetime.datetime.now() - start).total_seconds()
    num_cores = os.environ.get("NUM_CORES", None)
    if num_cores != None:
        num_cores = int(num_cores)
        config = EMBEDDED_APP.ExtAPI.Application.SolveConfigurations["My Computer"]
        config.SolveProcessSettings.MaxNumberOfCores = 2
    return startup_time


EMBEDDED_APP = None


@pytest.fixture(scope="session")
def embedded_app(request):
    global EMBEDDED_APP
    startup_time = start_embedding_app()
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
