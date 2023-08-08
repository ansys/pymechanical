"""Main application class for embedded Mechanical."""
import atexit
import os
import shutil

from ansys.mechanical.core.embedding import initializer, runtime
from ansys.mechanical.core.embedding.addins import AddinConfiguration


def _get_default_addin_configuration() -> AddinConfiguration:
    configuration = AddinConfiguration()
    return configuration


INSTANCES = []


def _dispose_embedded_app(instances):  # pragma: nocover
    if len(instances) > 0:
        instance = instances[0]
        instance._dispose()


def _cleanup_private_appdata(folder):
    shutil.rmtree(folder, ignore_errors=True)


def _start_application(configuration: AddinConfiguration, version, db_file) -> "App":
    import clr

    clr.AddReference("Ansys.Mechanical.Embedding")
    import Ansys

    if configuration.no_act_addins:
        os.environ["ANSYS_MECHANICAL_STANDALONE_NO_ACT_EXTENSIONS"] = "1"

    addin_configuration_name = configuration.addin_configuration
    # Starting with version 241 we can pass a configuration name to the constructor
    # of Application
    if version >= 241:
        return Ansys.Mechanical.Embedding.Application(db_file, addin_configuration_name)
    else:
        return Ansys.Mechanical.Embedding.Application(db_file)


class App:
    """Mechanical embedding Application."""

    def __init__(self, db_file=None, private_appdata=False, **kwargs):
        """Construct an instance of the mechanical Application.

        db_file is an optional path to a mechanical database file (.mechdat or .mechdb)
        you may set a version number with the `version` keyword argument.

        private_appdata is an optional setting for a temporary AppData directory.
        By default, private_appdata is False. This is beneficial for running parallel
        instances of mechanical.
        """
        global INSTANCES
        from ansys.mechanical.core import BUILDING_GALLERY

        if BUILDING_GALLERY:
            if len(INSTANCES) != 0:
                self._app = INSTANCES[0]
                self._app.new()
                self._version = self._app.version
                self._disposed = True
                return
        if len(INSTANCES) > 0:
            raise Exception("Cannot have more than one embedded mechanical instance")
        version = kwargs.get("version")
        self._version = initializer.initialize(version)

        configuration = kwargs.get("config", _get_default_addin_configuration())

        if private_appdata:
            self.pid = os.getpid()
            self.tmp_dir = initializer.set_private_appdata(self.pid)
            atexit.register(_cleanup_private_appdata, self.tmp_dir)

        self._app = _start_application(configuration, self._version, db_file)
        runtime.initialize()
        self._disposed = False
        atexit.register(_dispose_embedded_app, INSTANCES)
        INSTANCES.append(self)

    def __repr__(self):
        """Get the product info."""
        if self._version < 232:  # pragma: no cover
            return "Ansys Mechanical"
        import clr

        clr.AddReference("Ansys.Mechanical.Application")
        import Ansys

        return Ansys.Mechanical.Application.ProductInfo.ProductInfoAsString

    def __enter__(self):  # pragma: no cover
        """Enter the scope."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # pragma: no cover
        """Exit the scope."""
        self._dispose()

    def _dispose(self):
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
        """Close the active project."""
        # Call New() to remove the lock file of the
        # current project on close.
        self.DataModel.Project.New()

    def exit(self):
        """Exit the application."""
        self.ExtAPI.Application.Close()

    def execute_script(self, script: str):
        """Execute the given script with the internal IronPython engine."""
        SCRIPT_SCOPE = "pymechanical-internal"
        if not hasattr(self, "script_engine"):
            import clr

            clr.AddReference("Ansys.Mechanical.Scripting")
            import Ansys

            engine_type = Ansys.Mechanical.Scripting.ScriptEngineType.IronPython
            script_engine = Ansys.Mechanical.Scripting.EngineFactory.CreateEngine(engine_type)
            empty_scope = False
            debug_mode = False
            script_engine.CreateScope(SCRIPT_SCOPE, empty_scope, debug_mode)
            self.script_engine = script_engine
        light_mode = True
        args = None
        rets = None
        return self.script_engine.ExecuteCode(script, SCRIPT_SCOPE, light_mode, args, rets)

    @property
    def DataModel(self):
        """Return the DataModel."""
        return self._app.DataModel

    @property
    def ExtAPI(self):
        """Return the ExtAPI object."""
        return self._app.ExtAPI

    @property
    def version(self):
        """Returns the version of the app."""
        return self._version
