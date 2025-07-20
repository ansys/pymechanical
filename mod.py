import ansys.mechanical.core as mech
from ansys.mechanical.core.embedding.rpc import remote_method


def change_project_name(app: mech.App, name: str):
    """Change the project name of `app` to `name`."""
    app.DataModel.Project.Name = name


def get_project_name(app: mech.App):
    return app.DataModel.Project.Name


def get_model_name(app):
    return app.Model.Name

class ServiceMethods:
    def __init__(self, app):
        self._app = app

    def __repr__(self):
        return '"ServiceMethods instance"'

    @remote_method
    def get_model_name(self):
        return self._app.Model.Name

    @remote_method
    def change_project_name(self, name: str):
        self._app.DataModel.Project.Name = name


    @remote_method
    def get_project_name(self) -> str:
        return self._helper_func()

    def _helper_func(self) -> str:
        return self._app.DataModel.Project.Name
