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

""".. _ref_results:

Results
-------

This section has helper scripts for Results.
"""

# sphinx_gallery_start_ignore
import os

# Import Mechanical API core and example utilities
from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

# Download an example Mechanical database (.mechdat file)
mechdat_path = download_file("example_03_simple_bolt_new.mechdat", "pymechanical", "00_basic")

# Launch Mechanical and open the example database
app = App(db_file=mechdat_path, globals=globals())
print(app)


# sphinx_gallery_end_ignore


# Plot the geometry of the model
app.plot()

# Print the Mechanical tree structure
app.print_tree()

# %%
# Solve
# ~~~~~
# Access the first analysis system (Static Structural)
static_struct = app.DataModel.AnalysisList[0]

# Clear any previously generated solution data
static_struct.Solution.ClearGeneratedData()
print("Solution Status:", static_struct.Solution.Status)

# Run the solver
static_struct.Solution.Solve()
print("Solution Status:", static_struct.Solution.Status)


# %%
# Results that are accessible for GetResult
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# List names of results already available in the solution
result_names = static_struct.GetResultsData().ResultNames
print("Available Results:", ", ".join(result_names))


# %%
# List Result Objects that can be added
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Show all available result objects that can be inserted into the solution
all_results = [x for x in dir(static_struct) if str(x)[:3] == "Add"]
print(all_results)

# %%
# Insert a Result
# ~~~~~~~~~~~~~~~

# Add a Total Deformation result and evaluate it
total_deformation = static_struct.Solution.AddTotalDeformation()
total_deformation.EvaluateAllResults()


# %% Access max and min of a result
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Retrieve the minimum and maximum values for total deformation
minimum_deformation = total_deformation.Minimum
maximum_deformation = total_deformation.Maximum
print(f"Minimum Deformation: {minimum_deformation}")
print(f"Maximum Deformation: {maximum_deformation}")

# %%
# Get Results by Node Number
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Extract displacement ("U") results for a specific node ID
node_number = 2000
result_data = static_struct.GetResultsData()
node_values = result_data.GetResult("U").GetNodeValues(node_number)
print(f"Node {node_number} Values:", node_values)

# %%
# Access other results
# ~~~~~~~~~~~~~~~~~~~~


# Insert a command snippet into the solution (for custom APDL/commands)
cs = static_struct.Solution.AddCommandSnippet()

# %%
# Fatigue Results
# ~~~~~~~~~~~~~~~
# Add a Fatigue Tool to the solution

solution = static_struct.Solution
fatigue_tool = solution.AddFatigueTool()

# Insert a Safety Factor calculation under the fatigue tool
safety_factor = fatigue_tool.AddSafetyFactor()

# Scope safety factor evaluation to specific mesh nodes
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.MeshNodes)
selection.Ids = [1, 2]
safety_factor.Location = selection

# Get the minimum safety factor value
minimum = safety_factor.Minimum
print("Safety Factor Minimum:", minimum)

# Export safety factor results to a text file
fname = "safety_factor_results.txt"
safety_factor.ExportToTextFile(True, fname)

# %%
# User-defined Result
# ~~~~~~~~~~~~~~~~~~~
# Insert a User-Defined Result object
user_result = static_struct.Solution.AddUserDefinedResult()
print("User-defined Result Added:", user_result)

# %%
# Get number of result sets
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Retrieve the number of available result sets (time/frequency steps)

reader = static_struct.GetResultsData()
result_set_count = reader.ListTimeFreq.Count
print("Number of Result Sets:", result_set_count)


# %%
# Export all results in the tree to PNG (2D image) files
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Iterate over all result objects and export each one to an image
results = DataModel.GetObjectsByType(DataModelObjectCategory.Result)
for result in results:
    result.Activate()
    Graphics.Camera.SetSpecificViewOrientation(ViewOrientationType.Front)
    image_path = os.path.join(os.getcwd(), "out", result.Name + ".png")
    Graphics.ExportImage(
        str(image_path),
        GraphicsImageExportFormat.PNG,
        Ansys.Mechanical.Graphics.GraphicsImageExportSettings(),
    )
print("Done with Exporting Results")


# sphinx_gallery_start_ignore
# Save the project as a .mechdat file
from pathlib import Path

output_path = Path.cwd() / "out"
test_mechdat_path = str(output_path / "test.mechdat")
# app.save_as(test_mechdat_path, overwrite=True)


# Close Mechanical application

app.close()
# Delete the downloaded files
delete_downloads()
# sphinx_gallery_end_ignore
