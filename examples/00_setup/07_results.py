""".. _ref_results:

Results
-------

This section has helper scripts for Results.
"""


# sphinx_gallery_start_ignore
import os
from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

mechdat_path = download_file("example_03_simple_bolt_new.mechdat", "pymechanical", "00_basic")
app = App(db_file = mechdat_path, globals=globals())
print(app)


# sphinx_gallery_end_ignore



# Plot
app.plot()

# Print the tree
app.print_tree()

# %%
# Solve
# ~~~~~
static_struct = app.DataModel.AnalysisList[0]
static_struct.Solution.ClearGeneratedData()
print("Solution Status:", static_struct.Solution.Status)

static_struct.Solution.Solve()
print("Solution Status:", static_struct.Solution.Status)


# %%
# Results that are accessible for GetResult
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

result_names = static_struct.GetResultsData().ResultNames
print("Available Results:", ", ".join(result_names))


# %%
# List Result Objects that can be added
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

all_results = [x for x in dir(static_struct) if str(x)[:3]=="Add"]
print(all_results)

# %%
# Insert a Result
# ~~~~~~~~~~~~~~~


total_deformation = static_struct.Solution.AddTotalDeformation()
total_deformation.EvaluateAllResults()


# %% Access max and min of a result
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
minimum_deformation = total_deformation.Minimum
maximum_deformation = total_deformation.Maximum
print(f"Minimum Deformation: {minimum_deformation}")
print(f"Maximum Deformation: {maximum_deformation}")

# %%
# Get Results by Node Number
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
node_number = 2000
result_data = static_struct.GetResultsData()
node_values = result_data.GetResult("U").GetNodeValues(node_number)
print(f"Node {node_number} Values:", node_values)

# %%
# Access other results
# ~~~~~~~~~~~~~~~~~~~~


# Insert a command object
cs = static_struct.Solution.AddCommandSnippet()

# %%
# Fatigue Results
# ~~~~~~~~~~~~~~~
solution = static_struct.Solution
fatigue_tool = solution.AddFatigueTool()

safety_factor = fatigue_tool.AddSafetyFactor()
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.MeshNodes)
selection.Ids = [1, 2]
safety_factor.Location = selection
minimum = safety_factor.Minimum
print("Safety Factor Minimum:", minimum)

# Export safety factor to a text file
fname = "safety_factor_results.txt"
safety_factor.ExportToTextFile(True, fname)

# %%
# User-defined Result
# ~~~~~~~~~~~~~~~~~~~
user_result = static_struct.Solution.AddUserDefinedResult()
print("User-defined Result Added:", user_result)

# %%
# Get number of result sets
# ~~~~~~~~~~~~~~~~~~~~~~~~~
reader = static_struct.GetResultsData()
result_set_count = reader.ListTimeFreq.Count
print("Number of Result Sets:", result_set_count)



# %%
# Export all results in the tree to PNG (2D image) files
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
results = DataModel.GetObjectsByType(DataModelObjectCategory.Result)
for result in results:
    result.Activate()
    Graphics.Camera.SetSpecificViewOrientation(ViewOrientationType.Front)
    image_path = os.path.join(os.getcwd(),"out",result.Name+".png")
    Graphics.ExportImage(str(image_path), GraphicsImageExportFormat.PNG, Ansys.Mechanical.Graphics.GraphicsImageExportSettings())
print("Done with Exporting Results")



# sphinx_gallery_start_ignore
# Save the mechdat
from pathlib import Path

output_path = Path.cwd() / "out"
test_mechdat_path = str(output_path / "test.mechdat")
# app.save_as(test_mechdat_path, overwrite=True)


# Close the app
app.close()
# Delete the downloaded files
# delete_downloads()
# sphinx_gallery_end_ignore
