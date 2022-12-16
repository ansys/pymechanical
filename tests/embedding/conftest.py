import datetime
import pathlib
import pytest

start = datetime.datetime.now()
import ansys.mechanical.embedding as mke

# Done here rather than in a fixture because the subsequent imports only work after the mke App initializes.
#TODO - figure out how to write to pytest stdout at this stage (to report time taken to start mechanical)
APP = mke.App(version=232)
_startup_duration = (datetime.datetime.now()-start).total_seconds()


'''region imports module'''
globals().update(mke.global_variables(APP))

class Selection:
    def __init__(self):
        self._mgr = ExtAPI.SelectionManager
    def UpdateSelection(self, api, input, type):
        new_selection = self._mgr.CreateSelectionInfo(type)
        ids = System.Collections.Generic.List[System.Int32]()
        [ids.Add(item) for item in input]
        new_selection.Ids = ids
        self._mgr.NewSelection(new_selection)

# TODO - in the imports file, add the path to DSPages/python so this is not needed
selection = Selection()

'''end region imports module'''

ROOT_FOLDER = pathlib.Path(__file__).parent

def get_assets_folder():
    return ROOT_FOLDER / "assets"

@pytest.fixture(scope="session", autouse=True)
def report_startup_time(request):
    terminal_reporter = request.config.pluginmanager.getplugin("terminalreporter")
    if terminal_reporter is not None:
        terminal_reporter.write_line(f"\t{_startup_duration}\tStarting Mechanical")

@pytest.fixture(autouse=True)
def mke_app_reset(request):
    terminal_reporter = request.config.pluginmanager.getplugin("terminalreporter")
    if terminal_reporter is not None:
        terminal_reporter.write_line(f"starting test {request.function} - file new")
    APP.new()
