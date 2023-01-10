"""Main application class for embedded Mechanical."""
import os

from ansys.mechanical.core.embedding import initializer
from ansys.mechanical.core.embedding import loader

INITIALIZED = False


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


class App:
    """Mechanical embedding Application."""

    def __init__(self, db_file=None, **kwargs):
        """Construct an instance of the mechanical Application.

        db_file is an optional path to a mechanical database file (.mechdat or .mechdb)
        you may set a version number with the `version` keyword argument.
        """
        global INITIALIZED
        if INITIALIZED:
            raise Exception("Cannot initialize embedded mechanical more than once")
        version = kwargs.get("version")
        if version == None:
            version = _get_default_version()
        initializer.initialize(version)
        import clr
        clr.AddReference("Ansys.Mechanical.Embedding")
        import Ansys

        self._app = Ansys.Mechanical.Embedding.Application(db_file)
        if version >= 231 and not loader.is_pythonnet_3():
            # TODO - support InitializeRuntime for pythonnet3 (or maybe it isn't needed anymore?)
            clr.AddReference("Ansys.Mechanical.CPython")
            Ansys.Mechanical.CPython.CPythonEngine.InitializeRuntime()
        INITIALIZED = True

    def __enter__(self):
        """Enter the scope."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the scope."""
        self._app.Dispose()

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
