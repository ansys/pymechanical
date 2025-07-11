
from statistics import mode
from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

app = App()
app.update_globals(globals())
print(app)

all_input_files = {
    "geometry_file_name": "example_09_pcb.agdb",
    "def_file": "example_09_edb.def",
    "copper_alloy_material_file": "example_09_mat_copper_alloy.xml",
    "fr4_material_file": "example_09_mat_fr4.xml",
}
downloaded_file_paths = {}
for file_type, file_name in all_input_files.items():
    downloaded_file_paths[file_type] = download_file(file_name, "pymechanical", "00_basic")


# CamelCase
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
# pep8 formatting
geometry_import = model.geometry_import_group.add_geometry_import()

geometry_import_format = (
    Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
)
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.process_named_selections = True
geometry_import_preferences.named_selection_key = "NS"
geometry_import.Import(
    downloaded_file_paths["geometry_file_name"], geometry_import_format, geometry_import_preferences
)


# Insert a Static Structural Analysis

analysis = app.model.add_static_structural_analysis()
print(analysis.name)

#ExtAPI.DataModel.Project.UnitSystem = UserUnitSystemType.StandardNMM
extapi.data_model.project.unit_system = UserUnitSystemType.StandardNMM
# Import Materials

materials = app.model.materials #ExtAPI.DataModel.Project.Model.Materials
materials.Import(downloaded_file_paths["copper_alloy_material_file"])
materials.Import(downloaded_file_paths["fr4_material_file"])


# create lists of body ids to create named selections later

board_bodyids = []
component_bodyids = []
geo = extapi.data_model.geo_data #  ExtAPI.DataModel.GeoData
mesh = model.mesh
for asm in geo.Assemblies:
    for part in asm.Parts:
        for body in part.Bodies:
            if body.Name[:9] != "Component":
                board_bodyids.append(body.Id)
            else:
                component_bodyids.append(body.Id)

# Assign  Materials based on Body Names

parts = model.children #ExtAPI.DataModel.Project.Model.Geometry.Children  # list of parts
for part in parts:
    for body in part.Children:
        body.Material = "Copper Alloy" if body.Name[:9] == "Component" else "FR-4"


# Function to create named selection from list of body ids

def create_named_selection_from_id_list(ns_name, list_of_body_ids):

    selection_manager = extapi.selection_manager# ExtAPI.SelectionManager
    selection = extapi.selection_manager.create_selection_info(
        SelectionTypeEnum.GeometryEntities
    )
    selection.ids = list_of_body_ids
    selection_manager.new_selection(selection)
    named_sel = model.add_named_selection()
    named_sel.name = ns_name
    named_sel.location = selection
    selection_manager.clear_selection()


create_named_selection_from_id_list("board_layers", board_bodyids)
create_named_selection_from_id_list("components", component_bodyids)

# make a selection to be used with mesh methods

selection_manager = extapi.selection_manager# ExtAPI.SelectionManager
selection = ExtAPI.SelectionManager.CreateSelectionInfo(
    SelectionTypeEnum.GeometryEntities
)
selection.ids = board_bodyids
selection_manager.new_selection(selection)

mesh = model.mesh

mesh_method = mesh.add_automatic_method()
mesh_method.location = selection
mesh_method.method = MethodType.Sweep
mesh_method.element_order = ElementOrder.Linear
mesh_method.sweep_number_divisions = 1

mesh_sizing = mesh.add_sizing()
mesh_sizing.element_size = Quantity("0.25 [mm]")
mesh.generate_mesh()


# Defining External Data Object  for Importing Trace

external_data_files = Ansys.Mechanical.ExternalData.ExternalDataFileCollection()
external_data_files.save_files_with_project = True
external_data_file = Ansys.Mechanical.ExternalData.ExternalDataFile()
external_data_files.add(external_data_file)  # Single File
external_data_file.identifier = "edb"
external_data_file.description = ""
external_data_file.is_main_file = False
external_data_file.file_path = downloaded_file_paths["def_file"]
external_data_file.import_settings = (
    Ansys.Mechanical.ExternalData.ImportSettingsFactory.GetSettingsForFormat(
        Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.ImportFormat.ECAD
    )
)
import_settings = external_data_file.ImportSettings
import_settings.UseDummyNetData = False
imported_trace_group = Model.Materials.AddImportedTraceExternalData()
imported_trace_group.ImportExternalDataFiles(external_data_files)

allImpTraces = ExtAPI.DataModel.GetObjectsByType(
    Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.ImportedTrace
)

imp_trace = [
    x for x in allImpTraces if x.Parent.ObjectId == imported_trace_group.ObjectId
][0]
imp_trace.Activate()
# imp_trace.InternalObject.GeometryDefineBy = 1

NSall = model.named_selections.get_children[
    Ansys.ACT.Automation.Mechanical.NamedSelection
](True)
ns_object = [i for i in NSall if i.Name == "board_layers"][0]
imp_trace.location = ns_object
imp_trace.PropertyByName("PROPID_ExternalData").InternalValue = 1


layers = imp_trace.layers
num_layers = layers.count
for layer in layers:
    layer["Trace Material"] = "Copper Alloy"
vias = imp_trace.vias
num_vias = vias.count
for via in vias:
    via["Plating Material"] = "Copper Alloy"
imp_trace.Import()


# Exporting trace map snapshot to a png file
import os
out = os.path.join(os.getcwd(), "trace_map_snapshot.png")
graphics.camera.set_fit()
set2d = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
set2d.CurrentGraphicsDisplay = False
graphics.export_image(out, GraphicsImageExportFormat.PNG, set2d)

app.print_tree()
app.close()
delete_downloads()