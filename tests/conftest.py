import datetime
import os
import platform

import pytest

import ansys.mechanical.core as pymechanical
from ansys.mechanical.core.errors import MechanicalExitedError

# connect to an existing instance
# @pytest.fixture(scope="session")
# def mechanical():
#     from ansys.mechanical import core as pymechanical
#     mechanical = pymechanical.Mechanical()
#     yield mechanical
#
#     mechanical.exit(force=True)
#     assert mechanical.exited
#     assert "Mechanical exited" in str(mechanical)
#     with pytest.raises(MechanicalExitedError):
#         mechanical.run_python_script("3+4")


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
            ids = System.Collections.Generic.List[System.Int32]()
            [ids.Add(item) for item in input]
            new_selection.Ids = ids
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


@pytest.fixture(scope="session")
def mechanical():
    print("current working directory: ", os.getcwd())

    if not pymechanical.mechanical.get_start_instance():
        hostname = platform.uname().node  # your machine name
        print(f"get_start_instance() returned False. connecting to {hostname}.")
        # ip needs to be passed or start instance takes precedence
        # typical for container scenarios use connect
        # and needs to be treated as remote scenarios
        mechanical = pymechanical.launch_mechanical(
            ip=hostname, clear_on_connect=False, cleanup_on_exit=False
        )
    else:
        mechanical = pymechanical.launch_mechanical()

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
