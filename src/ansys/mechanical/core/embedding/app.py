import clr
import os
from . import initializer

INITIALIZED = False


def _get_available_versions():
    supported_versions = [222, 231, 232]
    if os.name == "nt":
        awp_roots = {ver: os.environ.get(f"AWP_ROOT{ver}", "") for ver in supported_versions}
        installed_versions = {
            ver: path for ver, path in awp_roots.items() if path and os.path.isdir(path)
        }
        return installed_versions
    else:
        raise Exception("TODO - Support linux")


def _get_default_version():
    vers = _get_available_versions()
    if not vers:
        raise Exception(
            "Appropriate version of Ansys Mechanical is not installed. Must be at least v222"
        )
    return max(vers.keys())


class App:
    def __init__(self, db_file=None, **kwargs):
        global INITIALIZED
        if INITIALIZED:
            raise Exception("Cannot initialize embedded mechanical more than once")
        version = kwargs.get("version")
        if version == None:
            version = _get_default_version()
        initializer.initialize(version)
        clr.AddReference("Ansys.Mechanical.Embedding")
        if version >= 231:
            clr.AddReference("Ansys.Mechanical.CPython")
        import Ansys

        self._app = Ansys.Mechanical.Embedding.Application(db_file)
        if version >= 231:
            Ansys.Mechanical.CPython.CPythonEngine.InitializeRuntime()
        INITIALIZED = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._app.Dispose()

    def open(self, db_file):
        self.DataModel.Project.Open(db_file)

    def save(self, path=None):
        self.DataModel.Project.Save(path)

    def save_as(self, path):
        self.DataModel.Project.SaveAs(path)

    def new(self):
        self.DataModel.Project.New()

    def close(self):
        self.ExtAPI.Application.Close()

    @property
    def DataModel(self):
        return self._app.DataModel

    @property
    def ExtAPI(self):
        return self._app.ExtAPI
