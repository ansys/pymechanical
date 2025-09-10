# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

This script contains helper examples for applying loads and boundary conditions in Ansys Mechanical.
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
Model.Mesh.GenerateMesh()

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
analysis = Model.AddStaticStructuralAnalysis()

# %% Apply Bolt Pretension by Face ID
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
analysis_settings = Model.Analyses[0].AnalysisSettings
analysis_settings.NumberOfSteps = 6

selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
selection.Ids = [39]
csys1 = Model.CoordinateSystems.AddCoordinateSystem()
csys1.OriginLocation = selection
csys1.Name="cyl"

pretension = Model.Analyses[0].AddBoltPretension()
pretension.Location = selection
pretension.CoordinateSystem = csys1
pretension.SetDefineBy(1, BoltLoadDefineBy.Load)
pretension.Preload.Output.SetDiscreteValue(0, Quantity("1500[N]"))
for i in range(2, analysis_settings.NumberOfSteps + 1):
    pretension.SetDefineBy(int(i), BoltLoadDefineBy.Lock)

# %%
# Apply a Fixed Support
# ~~~~~~~~~~~~~~~~~~~~~
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
face1 = body1.GetGeoBody().Faces[0]  # Get the first face of the body.
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
# Apply Nodal Forces by Components
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
nodes_list = [16,2329]
force_quantities_list = ["100 [N]", "-200 [N]"]

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

NSall = Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
for_fixed_supp = [i for i in NSall if i.Name.startswith("fixed")][0]
for_force = [i for i in NSall if i.Name.startswith("force")][0]

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
CSall = Model.CoordinateSystems.GetChildren[Ansys.ACT.Automation.Mechanical.CoordinateSystem](True)
a = [i for i in CSall if i.Name == "cyl"][0]
NSall = Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
n = [i for i in NSall if i.Name == "force"][0]

nf = Model.Analyses[0].AddNodalForce()
nf.Location = n
nf.YComponent.Inputs[0].DiscreteValues = [Quantity("0 [sec]"), Quantity("1 [sec]")]
nf.IndependentVariable = LoadVariableVariationType.YValue
nf.XYZFunctionCoordinateSystem = a
nf.YComponent.Output.DiscreteValues = [Quantity("0 [N]"), Quantity("100[N]")]

nd = Model.Analyses[0].AddNodalDisplacement()
nd.Location = n
nd.YComponent.Inputs[0].DiscreteValues = [Quantity("0 [sec]"), Quantity("1 [sec]")]
nd.IndependentVariable = LoadVariableVariationType.YValue
nd.XYZFunctionCoordinateSystem = a
nd.YComponent.Output.DiscreteValues = [Quantity("0 [mm]"), Quantity("100[mm]")]

np = Model.Analyses[0].AddNodalPressure()
np.Location = n
np.Magnitude.Inputs[0].DiscreteValues = [Quantity("0 [sec]"), Quantity("1 [sec]")]
np.IndependentVariable = LoadVariableVariationType.YValue
np.XYZFunctionCoordinateSystem = a
np.Magnitude.Output.DiscreteValues = [Quantity("0 [Pa]"), Quantity("100[Pa]")]

# sphinx_gallery_start_ignore
# Save the mechdat
from pathlib import Path

output_path = Path.cwd() / "out"
test_mechdat_path = str(output_path / "test_loads.mechdat")
# app.save_as(test_mechdat_path, overwrite=True)

# Close the app
app.close()
# Delete the downloaded files
delete_downloads()
# sphinx_gallery_end_ignore
