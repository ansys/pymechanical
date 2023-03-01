"""NOTE : All workflows will not be recorded, as recording is under development."""
import json

part_file_path = r"C:\temp\pytest\pymechanical-test\parts\hsec.x_t"
mechdb_open_path = r"C:\temp\pytest\pymechanical-test\parts\test1.mechdb"
mechdb_save_path = r"C:\temp\pytest\pymechanical-test\parts\test1.mechdb"


def attach_mesh_add_bc_results():
    # region Context Menu Action
    geometry_import_group_11 = Model.GeometryImportGroup
    geometry_import_19 = geometry_import_group_11.AddGeometryImport()
    # endregion

    # region Context Menu Action
    geometry_import_19_format = (
        Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
    )
    geometry_import_19_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
    geometry_import_19.Import(
        part_file_path, geometry_import_19_format, geometry_import_19_preferences
    )
    # endregion

    # region Context Menu Action
    mesh_13 = Model.Mesh
    mesh_13.GenerateMesh()
    # endregion

    # region Toolbar Action
    model_10 = Model
    analysis_39 = model_10.AddStaticStructuralAnalysis()
    # endregion

    # region Context Menu Action
    fixed_support_43 = analysis_39.AddFixedSupport()

    selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    selection.Ids = [82]
    fixed_support_43.Location = selection
    # endregion

    # region Context Menu Action
    pressure_45 = analysis_39.AddPressure()

    selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    selection.Ids = [55]
    pressure_45.Location = selection
    # endregion

    # region Details View Action
    pressure_45.Magnitude.Output.SetDiscreteValue(0, Quantity(1000, "Pa"))
    # endregion

    # region Context Menu Action
    total_deformation_47 = analysis_39.Solution.AddTotalDeformation()

    # endregion


def open_mechdb(file_path):
    file_path_modified = file_path.replace("\\", "\\\\")
    # we are working with iron python 2.7 on mechanical side
    # use python 2.7 style formatting
    script = "%s" % file_path_modified
    script = 'DS.Script.doStandaloneFileOpen("%s");' % script
    print(script)
    ExtAPI.Application.ScriptByName("jscript").ExecuteCommand(script)


def save_mechdb(file_path):
    file_path_modified = file_path.replace("\\", "\\\\")
    # we are working with iron python 2.7 on mechanical side
    # use python 2.7 style formatting
    script = "%s" % file_path_modified
    script = 'DS.Script.doStandaloneFileSaveAs("%s");' % script
    print(script)
    ExtAPI.Application.ScriptByName("jscript").ExecuteCommand(script)


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


attach_mesh_add_bc_results()
# open_mechdb(mechdb_open_path)
# change_mesh_element_size(0.02)
# return_mesh_statistics()
change_pressure_value(3000)
solve_model()
# save_mechdb(mechdb_save_path)
return_total_deformation()
