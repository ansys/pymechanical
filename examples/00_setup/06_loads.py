# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""".. _ref_loads:

Loads and BCs
-------------

This script contains helper examples for applying loads and boundary
conditions in Ansys Mechanical. Analysis Settings too are covered here.
"""

# sphinx_gallery_start_ignore

from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

app = App(globals=globals())
geom_file_path = download_file("example_06_bolt_pret_geom.agdb", "pymechanical", "00_basic")
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessLines = True
geometry_import_preferences.NamedSelectionKey = ""
geometry_import_preferences.ProcessNamedSelections = True
geometry_import_preferences.ProcessMaterialProperties = True
geometry_import.Import(geom_file_path, geometry_import_format, geometry_import_preferences)

# Generate mesh for the imported geometry
Model.Mesh.GenerateMesh()

# Create named selections for fixed support and force application
selection_manager = ExtAPI.SelectionManager
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
selection.Ids = [30]

ns2 = Model.AddNamedSelection()
ns2.Name = "fixed"
ns2.Location = selection
selection_manager.ClearSelection()

selection_manager = ExtAPI.SelectionManager
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
selection.Ids = [94]

ns2 = Model.AddNamedSelection()
ns2.Name = "force"
ns2.Location = selection
selection_manager.ClearSelection()

# sphinx_gallery_end_ignore

# Plot
app.plot()

# Print the tree
app.print_tree()

# %%
# Add an Analysis
# ~~~~~~~~~~~~~~~
# Create a static structural analysis
analysis = Model.AddStaticStructuralAnalysis()

# %% Apply Bolt Pretension by Face ID
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
analysis_settings = Model.Analyses[0].AnalysisSettings
analysis_settings.NumberOfSteps = 6

# Define coordinate system at face ID = 39
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
selection.Ids = [39]
csys1 = Model.CoordinateSystems.AddCoordinateSystem()
csys1.OriginLocation = selection
csys1.Name = "cyl"

# Apply bolt pretension load
pretension = Model.Analyses[0].AddBoltPretension()
pretension.Location = selection
pretension.CoordinateSystem = csys1
pretension.SetDefineBy(1, BoltLoadDefineBy.Load)
pretension.Preload.Output.SetDiscreteValue(0, Quantity("1500[N]"))
# Lock the bolt for remaining steps
for i in range(2, analysis_settings.NumberOfSteps + 1):
    pretension.SetDefineBy(int(i), BoltLoadDefineBy.Lock)

# %%
# Apply a Fixed Support
# ~~~~~~~~~~~~~~~~~~~~~
# Define a fixed support boundary condition on a specific geometry entity.

support = Model.Analyses[0].AddFixedSupport()
support_scoping = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
support_scoping.Ids = [30]
support.Location = support_scoping

# %%
# Apply a Pressure on the First Face of the First Body
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pressure = Model.Analyses[0].AddPressure()
part1 = Model.Geometry.Children[0]
body1 = part1.Children[0]
face1 = body1.GetGeoBody().Faces[0]  # First face of first body
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
selection.Entities = [face1]
pressure.Location = selection
pressure.Magnitude.Inputs[0].DiscreteValues = [Quantity("0 [s]"), Quantity("1 [s]")]
pressure.Magnitude.Output.DiscreteValues = [Quantity("10 [Pa]"), Quantity("20 [Pa]")]

# %%
# Apply a Pressure as a Formula
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pressure = Model.Analyses[0].AddPressure()
pressure_scoping = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
pressure_scoping.Ids = [95]
pressure.Location = pressure_scoping
pressure.Magnitude.Output.Formula = "10*time"

# %%
# Apply a Force
# ~~~~~~~~~~~~~
force = Model.Analyses[0].AddForce()
force_scoping = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
force_scoping.Ids = [63]
force.Location = force_scoping
force.Magnitude.Output.DiscreteValues = [Quantity("11.3 [N]"), Quantity("12.85 [N]")]

# %%
# Apply Force by Components
# ~~~~~~~~~~~~~~~~~~~~~~~~~
force = Model.Analyses[0].AddForce()
force_scoping = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
force_scoping.Ids = [63]
force.Location = force_scoping
force.DefineBy = LoadDefineBy.Components
force.ZComponent.Output.DiscreteValues = [Quantity("0 [N]"), Quantity("-9 [N]")]

# %%
# Add a remote displacement with 6 degrees of freedom fixed
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
remote_disp = analysis.AddRemoteDisplacement()
remote_disp.XComponent.Output.DiscreteValues = [Quantity("0 [mm]")]
remote_disp.YComponent.Output.DiscreteValues = [Quantity("0 [mm]")]
remote_disp.ZComponent.Output.DiscreteValues = [Quantity("0 [mm]")]
remote_disp.RotationX.Output.DiscreteValues = [Quantity("0 [deg]")]
remote_disp.RotationY.Output.DiscreteValues = [Quantity("0 [deg]")]
remote_disp.RotationZ.Output.DiscreteValues = [Quantity("0 [deg]")]


# %%
# Apply Nodal Forces by Components
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
nodes_list = [16, 2329]
force_quantities_list = ["100 [N]", "-200 [N]"]

# Loop through nodes and apply nodal force
for i in range(len(nodes_list)):
    N1 = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.MeshNodes)
    N1.Ids = [nodes_list[i]]
    ExtAPI.SelectionManager.NewSelection(N1)

    NS = Model.AddNamedSelection()
    NS.Name = "Node_" + str(nodes_list[i])

    Force1 = Model.Analyses[0].AddNodalForce()
    Force1.Location = NS
    Force1.Name = "NodeAtNode_" + str(nodes_list[i])
    Force1.YComponent.Output.DiscreteValues = [Quantity(force_quantities_list[i])]
    Force1.DivideLoadByNodes = False

# %%
# Apply Force and Fixed Support using Named Selections
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create named selections for force and fixed support
selection_manager = ExtAPI.SelectionManager
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
selection.Ids = [65]

ns2 = Model.AddNamedSelection()
ns2.Name = "fixed"
ns2.Location = selection
selection_manager.ClearSelection()

selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
selection.Ids = [65]

ns2 = Model.AddNamedSelection()
ns2.Name = "force"
ns2.Location = selection
selection_manager.ClearSelection()

# Retrieve named selections
NSall = Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
for_fixed_supp = [i for i in NSall if i.Name.startswith("fixed")][0]
for_force = [i for i in NSall if i.Name.startswith("force")][0]

# Apply load and support via named selections
f = Model.Analyses[0].AddForce()
f.Location = for_force
f.Name = "Force1"
f.Magnitude.Output.DiscreteValues = [Quantity("10 [N]")]

fs = Model.Analyses[0].AddFixedSupport()
fs.Location = for_fixed_supp
fs.Name = "FixedSupport1"

# %%
# Apply Radiation - Thermal Analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
analysis2 = Model.AddSteadyStateThermalAnalysis()
radn = analysis2.AddRadiation()

e = radn.Emissivity
e.Output.DiscreteValues = [Quantity("0.36")]

t = radn.AmbientTemperature
t.Inputs[0].DiscreteValues = [Quantity("0 [sec]"), Quantity("1 [sec]")]
t.Output.DiscreteValues = [Quantity("22 [C]"), Quantity("2302 [C]")]

# %%
# Add a temperature load applied to a named selection
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
temp_bc = analysis2.AddTemperature()
temp_bc.Location = app.DataModel.GetObjectsByName("fixed")[0]
temp_bc.Magnitude.Output.DiscreteValues = [Quantity("22[C]"), Quantity("60[C]")]
temp_bc.Magnitude.Inputs[0].DiscreteValues = [
    Quantity("0 [sec]"),
    Quantity("1 [sec]"),
    Quantity("2 [sec]"),
]
temp_bc.Magnitude.Output.DiscreteValues = [Quantity("22[C]"), Quantity("50[C]"), Quantity("80[C]")]


# %%
# # %%
# Create a convection load
# ~~~~~~~~~~~~~~~~~~~~~~~~
# analysis = app.Model.AddSteadyStateThermalAnalysis()
try:
    named_sel = app.Model.NamedSelections.Children[0]
except:
    print("Named Selection not found")

convection = Model.Analyses[0].AddConvection()
if named_sel != None:
    convection.Location = named_sel

convection.AmbientTemperature.Inputs[0].DiscreteValues = [
    Quantity("0 [s]"),
    Quantity("1 [s]"),
]  # Set the time values
convection.AmbientTemperature.Output.DiscreteValues = [
    Quantity("760  [C]"),
    Quantity("800  [C]"),
]  # Set the Ambient Temperature values
convection.FilmCoefficient.Inputs[0].DiscreteValues = [
    Quantity("0 [s]"),
    Quantity("1 [s]"),
]  # Set the time values
convection.FilmCoefficient.Output.DiscreteValues = [
    Quantity("100 [W m^-1 m^-1 K^-1]"),
    Quantity("150  [W m^-1 m^-1 K^-1]"),
]  # Set the HTC values


# %%
# Apply Tabular Pressure for 5 Load Steps
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pressureLoad = Model.Analyses[0].AddPressure()
pressureLoad.Magnitude.Inputs[0].DiscreteValues = [
    Quantity("0 [sec]"),
    Quantity("1 [sec]"),
    Quantity("2 [sec]"),
    Quantity("3 [sec]"),
    Quantity("4 [sec]"),
    Quantity("5 [sec]"),
]
pressureLoad.Magnitude.Output.DiscreteValues = [
    Quantity("0 [MPa]"),
    Quantity("10 [MPa]"),
    Quantity("30 [MPa]"),
    Quantity("25 [MPa]"),
    Quantity("-30 [MPa]"),
    Quantity("100 [MPa]"),
]

# %%
# Applying Direct FE Type Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Retrieve coordinate system named "cyl" and named selection "force"
CSall = Model.CoordinateSystems.GetChildren[Ansys.ACT.Automation.Mechanical.CoordinateSystem](True)
a = [i for i in CSall if i.Name == "cyl"][0]
NSall = Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
n = [i for i in NSall if i.Name == "force"][0]

# Nodal Force
nf = Model.Analyses[0].AddNodalForce()
nf.Location = n
nf.YComponent.Inputs[0].DiscreteValues = [Quantity("0 [sec]"), Quantity("1 [sec]")]
nf.IndependentVariable = LoadVariableVariationType.YValue
nf.XYZFunctionCoordinateSystem = a
nf.YComponent.Output.DiscreteValues = [Quantity("0 [N]"), Quantity("100[N]")]

# Nodal Displacement
nodal_displacement = Model.Analyses[0].AddNodalDisplacement()
nodal_displacement.Location = n
nodal_displacement.YComponent.Inputs[0].DiscreteValues = [Quantity("0 [sec]"), Quantity("1 [sec]")]
nodal_displacement.IndependentVariable = LoadVariableVariationType.YValue
nodal_displacement.XYZFunctionCoordinateSystem = a
nodal_displacement.YComponent.Output.DiscreteValues = [Quantity("0 [mm]"), Quantity("100[mm]")]

# Nodal Pressure
nodal_pressure = Model.Analyses[0].AddNodalPressure()
nodal_pressure.Location = n
nodal_pressure.Magnitude.Inputs[0].DiscreteValues = [Quantity("0 [sec]"), Quantity("1 [sec]")]
nodal_pressure.IndependentVariable = LoadVariableVariationType.YValue
nodal_pressure.XYZFunctionCoordinateSystem = a
nodal_pressure.Magnitude.Output.DiscreteValues = [Quantity("0 [Pa]"), Quantity("100[Pa]")]


# %%
# Set Automatic Time Stepping setting for a specific Load Step
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
analysis_settings = Model.Analyses[0].AnalysisSettings
analysis_settings.CurrentStepNumber = 1
print(analysis_settings.AutomaticTimeStepping)


# %%
# Set Step end time
# ~~~~~~~~~~~~~~~~~
analysis_settings.CurrentStepNumber = 5
analysis_settings.StepEndTime = Quantity("0.1 [sec]")

# %%
# Define Load steps with end times
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
analysis_settings.NumberOfSteps = 3

analysis_settings.CurrentStepNumber = 1
analysis_settings.StepEndTime = Quantity("1.0 [sec]")

analysis_settings.CurrentStepNumber = 2
analysis_settings.StepEndTime = Quantity("10.0 [sec]")

analysis_settings.CurrentStepNumber = 3
analysis_settings.StepEndTime = Quantity("100.0 [sec]")


# %%
# Define substep sizing using times
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
analysis_settings.CurrentStepNumber = 1
analysis_settings.StepEndTime = Quantity("0.1 [sec]")
analysis_settings.AutomaticTimeStepping = analysis_settings.AutomaticTimeStepping.On
analysis_settings.DefineBy = analysis_settings.DefineBy.Time
analysis_settings.InitialTimeStep = Quantity("0.005 [s]")
analysis_settings.MaximumTimeStep = Quantity("0.5 [s]")
analysis_settings.MinimumTimeStep = Quantity("0.0005 [s]")


# %%
# Define substep sizing using steps
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
analysis_settings.CurrentStepNumber = 1
analysis_settings.StepEndTime = Quantity("0.1 [sec]")
analysis_settings.AutomaticTimeStepping = analysis_settings.AutomaticTimeStepping.On
analysis_settings.DefineBy = analysis_settings.DefineBy.Substeps
analysis_settings.InitialSubsteps = 15
analysis_settings.MinimumSubsteps = 5
analysis_settings.MaximumSubsteps = 50

# %%
# Set Iterative solver type for solution
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
analysis_settings.SolverType = SolverType.Iterative

# other options from dir(SolverType) :
# analysis_settings.SolverType = SolverType.Direct
# analysis_settings.SolverType = SolverType.FullDamped
# analysis_settings.SolverType=SolverType.ProgramControlled
# analysis_settings.SolverType=SolverType.ReducedDamped
# analysis_settings.SolverType=SolverType.Subspace
# analysis_settings.SolverType=SolverType.Supernode
# analysis_settings.SolverType=SolverType.Unsymmetric


# %%
# Change the solver unit system
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
analysis_settings.SolverUnits = SolverUnitsControlType.Manual
analysis_settings.SolverUnitSystem = WBUnitSystemType.ConsistentMKS

# %%
# Get path to the Solver files directory
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
solve_dir = analysis_settings.ScratchSolverFilesDirectory
print(solve_dir)

# To get path to the scratch Solver files directory for an unsaved file
# solve_dir = analysis_settings.SolverFilesDirectory


# %%
# Solve an analysis
# ~~~~~~~~~~~~~~~~~
Model.Analyses[0].Solution.Activate()
Model.Analyses[0].Solution.Solve(True)


# %%
# Set the step end time and time steps in Transient structural analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# analysis = app.Model.AddTransientStructuralAnalysis()
analysis_settings = analysis.AnalysisSettings
analysis_settings.SetStepEndTime(1, Quantity("0.4 [s]"))
analysis_settings.SetInitialTimeStep(1, Quantity("0.0001 [s]"))
analysis_settings.SetMinimumTimeStep(1, Quantity("0.0000001 [s]"))
analysis_settings.SetMaximumTimeStep(1, Quantity("0.01 [s]"))


# sphinx_gallery_start_ignore
# Save the project as a mechdat file (currently commented out)

from pathlib import Path

output_path = Path.cwd() / "out"
test_mechdat_path = str(output_path / "test_loads.mechdat")
# app.save_as(test_mechdat_path, overwrite=True)

# Close Mechanical application
app.close()
# Delete downloaded files
delete_downloads()
# sphinx_gallery_end_ignore
