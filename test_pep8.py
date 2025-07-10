
from ansys.mechanical.core import App

app = App()
app.update_globals(globals())
print(app)

# CamelCase
geometry_import = Model.GeometryImportGroup.AddGeometryImport()

# pep8 formatting
geometry_import = Model.geometry_import_group.add_geometry_import()
app.print_tree()


# from Python.Runtime import BindingManager, BindingOptions
# binding_options = BindingOptions()
# binding_options.AllowExplicitInterfaceImplementation = True
# binding_options.Pep8Aliases = True