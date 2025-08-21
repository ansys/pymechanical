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

""".. _ref_named_selections:

Named Selections
----------------

This section has helper scripts for Named Selections.
"""

# sphinx_gallery_start_ignore
from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

app = App(globals=globals())
geom_file_path = download_file("example_05_td26_Rubber_Boot_Seal.agdb", "pymechanical", "00_basic")
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessLines = True
geometry_import_preferences.NamedSelectionKey = ""
geometry_import_preferences.ProcessNamedSelections = True
geometry_import_preferences.ProcessMaterialProperties = True
geometry_import.Import(geom_file_path, geometry_import_format, geometry_import_preferences)
# sphinx_gallery_end_ignore

# Plot
app.plot()

# Print the tree
app.print_tree()


# %%
# Fetch all Named Selections
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ALL NAMED SELECTIONS
nsall = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.NamedSelections.NamedSelection)

# %%
# Delete a named selection
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
NSall = ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[
    Ansys.ACT.Automation.Mechanical.NamedSelection
](True)

# Delete a named selection by name
a = [i for i in NSall if i.Name == "Top_Face"][0]
a.Delete()

# Alternative way to delete by name
b = ExtAPI.DataModel.GetObjectsByName("Bottom_Face")[0]
b.Delete()

# %%
# Create a named selection
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
selection_manager = ExtAPI.SelectionManager
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
selection.Ids = [216, 221, 224]

model = ExtAPI.DataModel.Project.Model
ns2 = model.AddNamedSelection()
ns2.Name = "faces"
ns2.Location = selection
selection_manager.ClearSelection()

# %%
# Create a Named Selection by Worksheet
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
NS1 = DataModel.Project.Model.AddNamedSelection()
NS1.ScopingMethod = GeometryDefineByType.Worksheet
GenerationCriteria = NS1.GenerationCriteria

Criterion1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
Criterion1.Action = SelectionActionType.Add
Criterion1.EntityType = SelectionType.GeoFace
Criterion1.Criterion = SelectionCriterionType.LocationY
Criterion1.Operator = SelectionOperatorType.Equal
Criterion1.Value = Quantity("0 [m]")
GenerationCriteria.Add(Criterion1)

Criterion2 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
Criterion2.Action = SelectionActionType.Add
Criterion2.EntityType = SelectionType.GeoFace
Criterion2.Criterion = SelectionCriterionType.LocationZ
Criterion2.Operator = SelectionOperatorType.Equal
Criterion2.Value = Quantity("0 [m]")
GenerationCriteria.Add(Criterion2)

NS1.Generate()

# %%
# Find a Named Selection
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
NSall = ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[
    Ansys.ACT.Automation.Mechanical.NamedSelection
](True)

# Find a named selection by name
a = [i for i in NSall if i.Name == "Rubber_Bodies30"][0]

# Access entities in the named selection
entities = a.Entities
print(entities[0].Volume)

# %%
# Identify Named Selections based on Name and Type
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
NSall = ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[
    Ansys.ACT.Automation.Mechanical.NamedSelection
](True)

# Filter named selections based on keywords in their names
keywords = ["Rubber_Bodies30", "Inner_Faces30", "Outer_Faces30"]
ns1 = [i for i in NSall if keywords[0] in i.Name]
ns2 = [i for i in NSall if keywords[1] in i.Name]
ns3 = [i for i in NSall if keywords[2] in i.Name]
filtered = ns1 + ns2 + ns3

# Further filter based on entity type
FaceNsels = [
    i for i in filtered if str(ExtAPI.DataModel.GeoData.GeoEntityById(i.Ids[0]).Type) == "GeoFace"
]


# sphinx_gallery_start_ignore
# Save the mechdat
from pathlib import Path

output_path = Path.cwd() / "out"
test_mechdat_path = str(output_path / "test.mechdat")
app.save_as(test_mechdat_path, overwrite=True)


# Close the app
app.close()
# Delete the downloaded files
delete_downloads()
# sphinx_gallery_end_ignore
