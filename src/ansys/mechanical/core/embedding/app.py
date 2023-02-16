"""Main application class for embedded Mechanical."""
import atexit
import os

from ansys.mechanical.core.embedding import initializer, runtime
from ansys.mechanical.core.embedding.config import Configuration, configure


def _get_available_versions():
    supported_versions = [222, 231, 232]
    if os.name == "nt":
        supported_versions = [222, 231, 232]
        awp_roots = {ver: os.environ.get(f"AWP_ROOT{ver}", "") for ver in supported_versions}
        installed_versions = {
            ver: path for ver, path in awp_roots.items() if path and os.path.isdir(path)
        }
        return installed_versions
    else:
        # TODO - this can't be hardcoded... see how pymapdl does this.
        os.environ["AWP_ROOT232"] = "/data/mkoubaa/ansys_inc/v232"
        return {232: os.environ["AWP_ROOT232"]}


def _get_default_version():
    vers = _get_available_versions()
    if not vers:
        raise Exception(
            "Appropriate version of Ansys Mechanical is not installed. Must be at least v222"
        )
    return max(vers.keys())


def _get_default_configuration():
    configuration = Configuration()
    if os.name != "nt":
        configuration.no_act_addins = True
    return configuration

INSTANCE = None

def _dispose_embedded_app():
    global INSTANCE
    if INSTANCE != None:
        INSTANCE._app.Dispose()

atexit.register(_dispose_embedded_app)

class App:
    """Mechanical embedding Application."""

    def __init__(self, db_file=None, **kwargs):
        """Construct an instance of the mechanical Application.

        db_file is an optional path to a mechanical database file (.mechdat or .mechdb)
        you may set a version number with the `version` keyword argument.
        """
        global INSTANCE
        if INSTANCE != None:
            raise Exception("Cannot have more than one embedded mechanical instance")
        version = kwargs.get("version")
        if version == None:
            version = _get_default_version()
        initializer.initialize(version)
        import clr

        clr.AddReference("Ansys.Mechanical.Embedding")
        import Ansys

        configuration = kwargs.get("config", _get_default_configuration())
        configure(configuration)
        self._app = Ansys.Mechanical.Embedding.Application(db_file)
        runtime.initialize(version)
        self._disposed = False
        INSTANCE = self

    def __enter__(self):
        """Enter the scope."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the scope."""
        if self._disposed:
            return
        self._app.Dispose()
        self._disposed = True

    def open(self, db_file):
        """Open the db file."""
        self.DataModel.Project.Open(db_file)

    def save(self, path=None):
        """Save the project."""
        self.DataModel.Project.Save(path)

    def save_as(self, path):
        """Save the project as."""
        self.DataModel.Project.SaveAs(path)

    def new(self):
        """Clear to a new application."""
        self.DataModel.Project.New()

    def close(self):
        """Close the application."""
        self.ExtAPI.Application.Close()

    @property
    def DataModel(self):
        """Return the DataModel."""
        return self._app.DataModel

    @property
    def ExtAPI(self):
        """Return the ExtAPI object."""
        return self._app.ExtAPI
