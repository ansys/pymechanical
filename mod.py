import ansys.mechanical.core as mech
from ansys.mechanical.core.embedding.rpc.utils import remote_method, q

q.BAR

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

    @remote_method[str]
    def get_model_name(self):
        return self._app.Model.Name

    @remote_method[str, str]
    def change_project_name(self, name: str):
        self._app.DataModel.Project.Name = name

    @remote_method[str, str]
    def analysis_name(self, name: str):
        self._app.Model.Analyses[0].Name

    @remote_method[str]
    def get_project_name(self) -> str:
        return self._helper_func()

    def _helper_func(self) -> str:
        return self._app.DataModel.Project.Name
