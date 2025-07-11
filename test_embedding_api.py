
from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

app = App()
app.update_globals(globals())
print(app)


from ansys.mechanical.core.embedding.global_importer import Quantity
from ansys.mechanical.core.embedding.transaction import Transaction


model = app.Model

# Create a geometry import group for the model
geometry_import_group = model.GeometryImportGroup
# Add the geometry import to the group
geometry_import = geometry_import_group.AddGeometryImport()
# Set the geometry import format
geometry_import_format = (
    Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
)
# Set the geometry import preferences
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessNamedSelections = True

geometry_path = download_file(
    "example_06_bolt_pret_geom.agdb", "pymechanical", "00_basic"
)


# This wont work
geometry_import.import(
    geometry_path, Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic, geometry_import_preferences
)