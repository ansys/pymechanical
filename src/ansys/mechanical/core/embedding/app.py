# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

"""Main application class for embedded Mechanical."""
import atexit
import os
import typing
import warnings

from ansys.mechanical.core.embedding import initializer, runtime
from ansys.mechanical.core.embedding.addins import AddinConfiguration
from ansys.mechanical.core.embedding.appdata import UniqueUserProfile
from ansys.mechanical.core.embedding.imports import global_entry_points, global_variables
from ansys.mechanical.core.embedding.poster import Poster
from ansys.mechanical.core.embedding.warnings import connect_warnings, disconnect_warnings

try:
    import ansys.tools.visualization_interface  # noqa: F401

    HAS_ANSYS_VIZ = True
    """Whether or not PyVista exists."""
except:

    HAS_ANSYS_VIZ = False


def _get_default_addin_configuration() -> AddinConfiguration:
    configuration = AddinConfiguration()
    return configuration


INSTANCES = []
"""List of instances."""


def _dispose_embedded_app(instances):  # pragma: nocover
    if len(instances) > 0:
        instance = instances[0]
        instance._dispose()


def _cleanup_private_appdata(profile: UniqueUserProfile):
    profile.cleanup()


def _start_application(configuration: AddinConfiguration, version, db_file) -> "App":
    import clr

    clr.AddReference("Ansys.Mechanical.Embedding")
    import Ansys

    if configuration.no_act_addins:
        os.environ["ANSYS_MECHANICAL_STANDALONE_NO_ACT_EXTENSIONS"] = "1"

    addin_configuration_name = configuration.addin_configuration
    # Starting with version 241 we can pass a configuration name to the constructor
    # of Application
    if int(version) >= 241:
        return Ansys.Mechanical.Embedding.Application(db_file, addin_configuration_name)
    else:
        return Ansys.Mechanical.Embedding.Application(db_file)


class GetterWrapper(object):
    """Wrapper class around an attribute of an object."""

    def __init__(self, obj, getter):
        """Create a new instance of GetterWrapper."""
        # immortal class which provides wrapped object
        self.__dict__["_immortal_object"] = obj
        # function to get the wrapped object from the immortal class
        self.__dict__["_get_wrapped_object"] = getter

    def __getattr__(self, attr):
        """Wrap getters to the wrapped object."""
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._get_wrapped_object(self._immortal_object), attr)

    def __setattr__(self, attr, value):
        """Wrap setters to the wrapped object."""
        if attr in self.__dict__:
            setattr(self, attr, value)
        setattr(self._get_wrapped_object(self._immortal_object), attr, value)


class App:
    """Mechanical embedding Application."""

    def __init__(self, db_file=None, private_appdata=False, **kwargs):
        """Construct an instance of the mechanical Application.

        db_file is an optional path to a mechanical database file (.mechdat or .mechdb)
        you may set a version number with the `version` keyword argument.

        private_appdata is an optional setting for a temporary AppData directory.
        By default, private_appdata is False. This enables you to run parallel
        instances of Mechanical.
        """
        global INSTANCES
        from ansys.mechanical.core import BUILDING_GALLERY

        if BUILDING_GALLERY:
            if len(INSTANCES) != 0:
                instance: App = INSTANCES[0]
                instance._share(self)
                if db_file != None:
                    self.open(db_file)
                return
        if len(INSTANCES) > 0:
            raise Exception("Cannot have more than one embedded mechanical instance!")
        version = kwargs.get("version")
        self._version = initializer.initialize(version)
        configuration = kwargs.get("config", _get_default_addin_configuration())

        if private_appdata:
            new_profile_name = f"PyMechanical-{os.getpid()}"
            profile = UniqueUserProfile(new_profile_name)
            profile.update_environment(os.environ)
            atexit.register(_cleanup_private_appdata, profile)

        self._app = _start_application(configuration, self._version, db_file)
        runtime.initialize(self._version)
        connect_warnings(self)
        self._poster = None

        self._disposed = False
        atexit.register(_dispose_embedded_app, INSTANCES)
        INSTANCES.append(self)
        self._updated_scopes: typing.List[typing.Dict[str, typing.Any]] = []
        self._subscribe()

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
        self._unsubscribe()
        disconnect_warnings(self)
        self._app.Dispose()
        self._disposed = True

    def open(self, db_file):
        """Open the db file."""
        self.DataModel.Project.Open(db_file)

    def save(self, path=None):
        """Save the project."""
        if path is not None:
            self.DataModel.Project.Save(path)
        else:
            self.DataModel.Project.Save()

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
        self._unsubscribe()
        if self.version < 241:
            self.ExtAPI.Application.Close()
        else:
            self.ExtAPI.Application.Exit()

    def execute_script(self, script: str) -> typing.Any:
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

    def plotter(self) -> None:
        """Return ``ansys.tools.visualization_interface.Plotter`` object."""
        if not HAS_ANSYS_VIZ:
            warnings.warn(
                "Installation of viz option required! Use pip install ansys-mechanical-core[viz]"
            )
            return

        if self.version < 242:
            warnings.warn("Plotting is only supported with version 2024R2 and later!")
            return

        # TODO Check if anything loaded inside app or else show warning and return

        from ansys.mechanical.core.embedding.viz.embedding_plotter import to_plotter

        return to_plotter(self)

    def plot(self) -> None:
        """Visualize the model in 3d.

        Requires installation using the viz option. E.g.
        pip install ansys-mechanical-core[viz]
        """
        _plotter = self.plotter()

        if _plotter is None:
            return

        return _plotter.show()

    @property
    def poster(self) -> Poster:
        """Returns an instance of Poster."""
        if self._poster == None:
            self._poster = Poster()
        return self._poster

    @property
    def DataModel(self):
        """Return the DataModel."""
        return GetterWrapper(self._app, lambda app: app.DataModel)

    @property
    def ExtAPI(self):
        """Return the ExtAPI object."""
        return GetterWrapper(self._app, lambda app: app.ExtAPI)

    @property
    def Tree(self):
        """Return the Tree object."""
        return GetterWrapper(self._app, lambda app: app.DataModel.Tree)

    @property
    def Model(self):
        """Return the Model object."""
        return GetterWrapper(self._app, lambda app: app.DataModel.Project.Model)

    @property
    def Graphics(self):
        """Return the Graphics object."""
        return GetterWrapper(self._app, lambda app: app.ExtAPI.Graphics)

    @property
    def readonly(self):
        """Return whether the Mechanical object is read-only."""
        import Ansys

        return Ansys.ACT.Mechanical.MechanicalAPI.Instance.ReadOnlyMode

    @property
    def version(self):
        """Returns the version of the app."""
        return self._version

    def _share(self, other) -> None:
        """Shares the state of self with other.

        Other is another instance of App.
        This is used when the BUILDING_GALLERY flag is on.
        In that mode, multiple instance of App are used, but
        they all point to the same underlying application
        object. Because of that, special care needs to be
        taken to properly share the state. Other will be
        a "weak reference", which doesn't own anything.
        """
        # the other app is not expecting to have a project
        # already loaded
        self.new()

        # set up the type hint (typing.Self is python3.11+)
        other: App = other

        # copy `self` state to other.
        other._app = self._app
        other._version = self._version
        other._poster = self._poster
        other._updated_scopes = self._updated_scopes

        # all events will be handled by the original App instance
        other._subscribed = False

        # finally, set the other disposed flag to be true
        # so that the shutdown sequence isn't duplicated
        other._disposed = True

    def _subscribe(self):
        try:
            # This will throw an error when using pythonnet because
            # EventSource isn't defined on the IApplication interface
            self.ExtAPI.Application.EventSource.OnWorkbenchReady += self._on_workbench_ready
            self._subscribed = True
        except:
            self._subscribed = False

    def _unsubscribe(self):
        if not self._subscribed:
            return
        self._subscribed = False
        self.ExtAPI.Application.EventSource.OnWorkbenchReady -= self._on_workbench_ready

    def _on_workbench_ready(self, sender, args) -> None:
        self._update_all_globals()

    def update_globals(
        self, globals_dict: typing.Dict[str, typing.Any], enums: bool = True
    ) -> None:
        """Use to update globals variables.

        When scripting inside Mechanical, the Mechanical UI will automatically
        set global variables in python. PyMechanical can not do that automatically,
        but this method can be used.
        `app.update_globals(globals())`

        By default, all enums will be imported too. To avoid including enums, set
        the `enums` argument to False.
        """
        self._updated_scopes.append(globals_dict)
        globals_dict.update(global_variables(self, enums))

    def _update_all_globals(self) -> None:
        for scope in self._updated_scopes:
            scope.update(global_entry_points(self))

    def _print_tree(self, node, max_lines, lines_count, indentation):
        """Recursively print till provided maximum lines limit.

        Each object in the tree is expected to have the following attributes:
         - Name: The name of the object.
         - Suppressed : Print as suppressed, if object is suppressed.
         - Children: Checks if object have children.
           Each child node is expected to have the all these attributes.

        Parameters
        ----------
        lines_count: int, optional
            The current count of lines printed. Default is 0.
        indentation: str, optional
            The indentation string used for printing the tree structure. Default is "".
        """
        if lines_count >= max_lines and max_lines != -1:
            print(f"... truncating after {max_lines} lines")
            return lines_count

        if not hasattr(node, "Name"):
            raise AttributeError("Object must have a 'Name' attribute")

        node_name = node.Name
        if hasattr(node, "Suppressed") and node.Suppressed is True:
            node_name += " (Suppressed)"
        print(f"{indentation}├── {node_name}")
        lines_count += 1

        if lines_count >= max_lines and max_lines != -1:
            print(f"... truncating after {max_lines} lines")
            return lines_count

        if hasattr(node, "Children") and node.Children is not None and node.Children.Count > 0:
            for child in node.Children:
                lines_count = self._print_tree(child, max_lines, lines_count, indentation + "|  ")
                if lines_count >= max_lines and max_lines != -1:
                    break

        return lines_count

    def print_tree(self, node=None, max_lines=80, lines_count=0, indentation=""):
        """
        Print the hierarchical tree representation of the Mechanical project structure.

        Parameters
        ----------
        node: DataModel object, optional
            The starting object of the tree.
        max_lines: int, optional
            The maximum number of lines to print. Default is 80. If set to -1, no limit is applied.

        Raises
        ------
        AttributeError
            If the node does not have the required attributes.

        Examples
        --------
        >>> import ansys.mechanical.core as mech
        >>> app = mech.App()
        >>> app.update_globals(globals())
        >>> app.print_tree()
        ... ├── Project
        ... |  ├── Model
        ... |  |  ├── Geometry Imports
        ... |  |  ├── Geometry
        ... |  |  ├── Materials
        ... |  |  ├── Coordinate Systems
        ... |  |  |  ├── Global Coordinate System
        ... |  |  ├── Remote Points
        ... |  |  ├── Mesh

        >>> app.print_tree(Model, 3)
        ... ├── Model
        ... |  ├── Geometry Imports
        ... |  ├── Geometry
        ... ... truncating after 3 lines

        >>> app.print_tree(max_lines=2)
        ... ├── Project
        ... |  ├── Model
        ... ... truncating after 2 lines
        """
        if node is None:
            node = self.DataModel.Project

        self._print_tree(node, max_lines, lines_count, indentation)
