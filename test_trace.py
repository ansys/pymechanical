from ansys.mechanical.core import launch_mechanical
from ansys.mechanical.core.api import Project
from ansys.mechanical.core.examples import delete_downloads, download_file

# Download the required files
# ---------------------------
all_input_files = {
    "geometry_file_name": "example_09_pcb.agdb",
    "def_file": "example_09_edb.def",
    "copper_alloy_material_file": "example_09_mat_copper_alloy.xml",
    "fr4_material_file": "example_09_mat_fr4.xml",
}
downloaded_file_paths = {}
for file_type, file_name in all_input_files.items():
    downloaded_file_paths[file_type] = download_file(file_name, "pymechanical", "00_basic")

# Launch the Mechanical application
# ---------------------------------
app = launch_mechanical(batch=False, cleanup_on_exit=False)
print(app)
project = Project(app)

# Import geometry
geo_group = project.model.add_geometry_group("geo_group")
geo_group.import_geometry(downloaded_file_paths["geometry_file_name"])

# Add analysis to the model
static_analysis = project.model.add_static_structural_analysis()
# steady_state_thermal_analysis = project.model.add_steady_state_thermal_analysis()

# setup the unit system
project.set_unit_system("StandardNMM")

# Import materials
project.materials.import_multiple(
    downloaded_file_paths["copper_alloy_material_file"], downloaded_file_paths["fr4_material_file"]
)

# Group geometry by ids
component_ids = project.geo.get_body_ids_by_prefix("Component")
board_bodyids = project.geo.get_body_ids_excluding_prefix("Component")
print(f"Component Body IDs: {component_ids}")
print(f"Board Body IDs: {board_bodyids}")

# Assign materials to geometry bodies based on their groups
project.geo.assign_materials_by_ids(component_ids, "Copper Alloy")
project.geo.assign_materials_by_ids(board_bodyids, "FR-4")

# Create named selections for the geometry bodies
project.namedselection.create_from_ids("components", component_ids)
project.namedselection.create_from_ids("board_layers", board_bodyids)
print(project.namedselection.list_all())

# Add mesh controls and generate the mesh
project.mesh.add_automatic_method(
    named_selection="board_layers", method="Sweep", element_order="Linear", sweep_divisions=1
)
project.mesh.add_sizing("board_layers", element_size_mm=0.25)
project.mesh.generate()


# Import trace
project.externaldata.import_ecad_trace(
    def_file=downloaded_file_paths["def_file"],
    identifier="edb",
    named_selection="board_layers",
    trace_material="Copper Alloy",
)

# Delete downloads to clean up
delete_downloads()


# Pros
# - UI support

# Cons
# - Unable to interact with objects in the UI
# - File transfer is complicated
