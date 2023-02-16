import pathlib

import ansys.mechanical.core as mech

ASSETS_FOLDER = pathlib.Path(__file__).parent.parent / "tests" / "embedding" / "assets"

app = mech.App(version=232)
globals().update(mech.global_variables(app))


geometry_file = str(ASSETS_FOLDER / "Eng157.x_t")

stat_struc = Model.AddStaticStructuralAnalysis()
buckl = Model.AddEigenvalueBucklingAnalysis()
Model.Analyses[1].InitialConditions[0].PreStressICEnvironment = Model.Analyses[0]
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import.Import(geometry_file)
materials = DataModel.GetObjectsByType(
    Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Material
)

ExtAPI.Application.ActiveUnitSystem = Ansys.ACT.Interfaces.Common.MechanicalUnitSystem.StandardBIN
Model.Geometry.ElementControl = Ansys.Mechanical.DataModel.Enums.ElementControl.Manual

new_selection = ExtAPI.SelectionManager.CreateSelectionInfo(
    Ansys.ACT.Interfaces.Common.SelectionTypeEnum.GeometryEntities
)
new_selection.Ids = [26]
ExtAPI.SelectionManager.NewSelection(new_selection)

stat_struc.AddFixedSupport()
new_selection.Ids = [25]
ExtAPI.SelectionManager.NewSelection(new_selection)
force = stat_struc.AddForce()
force.DefineBy = Ansys.Mechanical.DataModel.Enums.LoadDefineBy.Components
force.ZComponent.Output.SetDiscreteValue(0, Quantity("-1 [lbf]"))

buckl.AnalysisSettings.MaximumModesToFind = 6
buckl.AnalysisSettings.Stress = True
buckl.AnalysisSettings.Strain = True
tot_def_1 = buckl.Solution.AddTotalDeformation()
tot_def_1.Mode = 1
buckl.Solution.AddTotalDeformation().Mode = 2
buckl.Solution.AddTotalDeformation().Mode = 3
buckl.Solution.AddTotalDeformation().Mode = 4
buckl.Solution.AddTotalDeformation().Mode = 5
buckl.Solution.AddTotalDeformation().Mode = 6
equivelent_stress = buckl.Solution.AddEquivalentStress()
equivelent_stress.Mode = 6


Model.Solve(True)
assert stat_struc.Solution.ObjectState == Ansys.Mechanical.DataModel.Enums.ObjectState.Solved
assert buckl.Solution.ObjectState == Ansys.Mechanical.DataModel.Enums.ObjectState.Solved

tot_def_1.Activate()
d1_mode1 = tot_def_1.TabularData["LoadMultiplier"].get_Item(0)
d1_mode3 = tot_def_1.TabularData["LoadMultiplier"].get_Item(2)
d1_mode5 = tot_def_1.TabularData["LoadMultiplier"].get_Item(4)
print(d1_mode1, d1_mode3, d1_mode5)
equivelent_stress.Activate()
s6_mode6 = equivelent_stress.TabularData["LoadMultiplier"].get_Item(5)
print(s6_mode6)
