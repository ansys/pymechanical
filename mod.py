import ansys.mechanical.core as mech

from server_global_poster import remote_method, get_remote_methods

def change_project_name(app: mech.App, name: str):
    """Change the project name of `app` to `name`."""
    app.DataModel.Project.Name = name

def get_project_name(app: mech.App):
    return app.DataModel.Project.Name

def get_model_name(app):
    return app.Model.Name

# option B
class ServiceMethods:
    def __init__(self, app):
        self._app = app
    def __repr__(self):
        return "\"ServiceMethods instance\""
    @remote_method
    def get_model_name(self):
        return self._app.Model.Name
    @remote_method
    def change_project_name(self, name: str):
        """Change the project name of `app` to `name`."""
        self._app.DataModel.Project.Name = name
    @remote_method
    def get_project_name(self):
        print(self)
        return self.helper_func()
        #return app.DataModel.Project.Name
    def helper_func(self):
        return self._app.DataModel.Project.Name

if __name__ == "__main__":
    @remote_method
    def foo():
        print('foo')
        return 2
    print(foo())
    print("\n\n")
    class monkeyz:
        def __repr__(self):
            return '"Monkeys!"'
        @remote_method
        def laugh(self):
            print("ooh ooh")
            return 5
        def jump(self):
            print("aah aah")
        @remote_method
        def eat(self):
            print("banana!")
    m = monkeyz()
    print(m.laugh())
    def print_deco_methods(obj):
        for methodname, method in get_remote_methods(obj):
            print(f"{methodname} is remote!")

    print_deco_methods(m)

