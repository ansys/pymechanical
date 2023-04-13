import json


def attach_geometry(part_file_path):
    geometry_import_group = Model.GeometryImportGroup
    geometry_import = geometry_import_group.AddGeometryImport()

    geometry_import_format = (
        Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
    )
    geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
    geometry_import.Import(part_file_path, geometry_import_format, geometry_import_preferences)

    return "success"


def generate_mesh():
    Model.Mesh.GenerateMesh()

    return "success"


def add_static_structural_analysis_bc_results():
    analysis = Model.AddStaticStructuralAnalysis()

    fixed_support = analysis.AddFixedSupport()

    selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    selection.Ids = [82]
    fixed_support.Location = selection

    pressure = analysis.AddPressure()

    selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    selection.Ids = [55]
    pressure.Location = selection

    pressure.Magnitude.Output.SetDiscreteValue(0, Quantity(1000, "Pa"))

    # region Context Menu Action
    total_deformation = analysis.Solution.AddTotalDeformation()

    return "success"


def get_ProjectDirectory():
    return ExtAPI.DataModel.Project.ProjectDirectory


def change_mesh_element_size(value):
    mesh = Model.Mesh
    mesh.ElementSize = Quantity(value, "m")
    mesh.GenerateMesh()


def change_pressure_value(value):
    pressure = DataModel.GetObjectsByName("Pressure")[0]
    pressure.Magnitude.Output.SetDiscreteValue(0, Quantity(value, "Pa"))


def return_mesh_statistics():
    mesh = Model.Mesh
    mesh_details = {"Nodes": mesh.Nodes, "Elements": mesh.Elements}
    json_text = json.dumps(mesh_details)
    return json_text


def solve_model():
    Model.Solve(True, "My Computer")


def return_total_deformation():
    td = DataModel.GetObjectsByName("Total Deformation")[0]
    total_deformation_details = {
        "Minimum": str(td.Minimum),
        "Maximum": str(td.Maximum),
        "Average": str(td.Average),
    }
    json_text = json.dumps(total_deformation_details)
    return json_text
