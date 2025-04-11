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

""".. _ref_embedding_remote:

Remote & Embedding Example
--------------------------
This code, which uses the same example, first demonstrates how to use
a remote session and then demonstrates how to use an embedding instance.

"""


###############################################################################
# Download the geometry file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Download Valve.pmdb.

import os

from ansys.mechanical.core import App
from ansys.mechanical.core.examples import download_file

geometry_path = download_file("Valve.pmdb", "pymechanical", "embedding")
print(f"Downloaded the geometry file to: {geometry_path}")


###############################################################################
# Embed Mechanical and set global variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Find the mechanical installation path & version.
# Open an embedded instance of Mechanical and set global variables.

app = App()
app.update_globals(globals())
print(app)


###############################################################################
# Add Static Analysis
# ~~~~~~~~~~~~~~~~~~~
# Add static analysis to the Model.

analysis = Model.AddStaticStructuralAnalysis()


###############################################################################
# Import geometry
# ~~~~~~~~~~~~~~~

geometry_file = geometry_path
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessNamedSelections = True
geometry_import.Import(geometry_file, geometry_import_format, geometry_import_preferences)
app.plot()

###############################################################################
# Assign material
# ~~~~~~~~~~~~~~~

matAssignment = Model.Materials.AddMaterialAssignment()
tempSel = ExtAPI.SelectionManager.CreateSelectionInfo(
    Ansys.ACT.Interfaces.Common.SelectionTypeEnum.GeometryEntities
)
bodies = [
    body
    for body in ExtAPI.DataModel.Project.Model.Geometry.GetChildren(
        Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Body, True
    )
]
geobodies = [body.GetGeoBody() for body in bodies]
ids = System.Collections.Generic.List[System.Int32]()
[ids.Add(item.Id) for item in geobodies]
tempSel.Ids = ids
matAssignment.Location = tempSel
matAssignment.Material = "Structural Steel"


###############################################################################
# Define mesh settings
# ~~~~~~~~~~~~~~~~~~~~

mesh = Model.Mesh
mesh.ElementSize = Quantity("25 [mm]")
mesh.GenerateMesh()


###############################################################################
# Define boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~

fixedSupport = analysis.AddFixedSupport()
fixedSupport.Location = ExtAPI.DataModel.GetObjectsByName("NSFixedSupportFaces")[0]

frictionlessSupport = analysis.AddFrictionlessSupport()
frictionlessSupport.Location = ExtAPI.DataModel.GetObjectsByName("NSFrictionlessSupportFaces")[0]

pressure = analysis.AddPressure()
pressure.Location = ExtAPI.DataModel.GetObjectsByName("NSInsideFaces")[0]

inputs_quantities = [Quantity("0 [s]"), Quantity("1 [s]")]
output_quantities = [Quantity("0 [Pa]"), Quantity("15 [MPa]")]

inputs_quantities_2 = System.Collections.Generic.List[Ansys.Core.Units.Quantity]()
[inputs_quantities_2.Add(item) for item in inputs_quantities]

output_quantities_2 = System.Collections.Generic.List[Ansys.Core.Units.Quantity]()
[output_quantities_2.Add(item) for item in output_quantities]

pressure.Magnitude.Inputs[0].DiscreteValues = inputs_quantities_2
pressure.Magnitude.Output.DiscreteValues = output_quantities_2


###############################################################################
# Solve model
# ~~~~~~~~~~~

Model.Solve(True)
solution = analysis.Solution

assert solution.Status == SolutionStatusType.Done

###############################################################################
# Add results
# ~~~~~~~~~~~

solution.AddTotalDeformation()
solution.AddEquivalentStress()
solution.EvaluateAllResults()


###############################################################################
# Save model
# ~~~~~~~~~~

project_directory = ExtAPI.DataModel.Project.ProjectDirectory
print(f"project directory = {project_directory}")
ExtAPI.DataModel.Project.SaveAs(os.path.join(project_directory, "file.mechdb"))


###############################################################################
# Export result values to a text file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fileExtension = r".txt"
results = solution.GetChildren(
    Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Result, True
)

for result in results:
    fileName = str(result.Name)
    print(f"filename: {fileName}")
    path = os.path.join(project_directory, fileName + fileExtension)
    print(path)
    result.ExportToTextFile(f"{path}")
    print("Exported Text file Contents", path)
    try:
        write_file_contents_to_console(path, number_lines=20)
    except:
        print(os.listdir(project_directory))

app.close()
