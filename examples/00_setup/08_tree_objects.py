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

""".. _ref_tree_objects:

Tree Objects
------------

This section has helper scripts for Tree Objects.
"""

# sphinx_gallery_start_ignore
from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

# Initialize the Mechanical application
app = App(globals=globals())

# Download and import the geometry file
geom_file_path = download_file("Valve.pmdb", "pymechanical", "embedding")
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic

# Define geometry import format and preferences
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessLines = True
geometry_import_preferences.NamedSelectionKey = ""
geometry_import_preferences.ProcessNamedSelections = True
geometry_import_preferences.ProcessMaterialProperties = True

# Import the geometry into the project
geometry_import.Import(geom_file_path, geometry_import_format, geometry_import_preferences)
# sphinx_gallery_end_ignore


# Plot the imported geometry
app.plot()

# Print the Mechanical tree structure
app.print_tree()


# %%
# Accessing Geometry
# ~~~~~~~~~~~~~~~~~~
# Access a specific geometry entity by its ID.

body = ExtAPI.DataModel.GeoData.GeoEntityById(312)

# %%
# Accessing Mesh Data
# ~~~~~~~~~~~~~~~~~~~~~~
# Access specific mesh data by name and ID.

node = ExtAPI.DataModel.MeshDataByName("Global").NodeById(555)
element = ExtAPI.DataModel.MeshDataByName("Global").ElementById(444)

# %%
# Accessing All Objects and Child Objects
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Examples of accessing all objects, bodies, named selections, and contact regions.

# Retrieve all objects in the  tree
AllObj = ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.DataModelObject, True)

# Retrieve all bodies
all_bodies = ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.Body, True)

# Retrieve all named selections
ns_all = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.NamedSelections.NamedSelection)

# Retrieve all contact regions
abc = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.ContactRegion)
all_contacts = ExtAPI.DataModel.Project.Model.Connections.GetChildren(
    DataModelObjectCategory.ContactRegion, True
)

# Access a specific contact region by name
my_contact = [contact for contact in all_contacts if contact.Name == "Contact Region"][0]

# Retrieve all result objects of a specific type (e.g., Normal Stress)
all_norm_stress = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.Result.NormalStress)

# Retrieve other objects such as remote points and analyses
all_remote_points = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.RemotePoint)
ana = ExtAPI.DataModel.Tree.GetObjectsByType(DataModelObjectCategory.Analysis)

# Using the ACT Automation API to retrieve specific objects
all_contacts2 = ExtAPI.DataModel.Project.Model.Connections.GetChildren[
    Ansys.ACT.Automation.Mechanical.Connections.ContactRegion
](True)
all_remote_points2 = ExtAPI.DataModel.Project.Model.GetChildren[
    Ansys.ACT.Automation.Mechanical.RemotePoint
](True)
all_folders = ExtAPI.DataModel.Project.Model.GetChildren[
    Ansys.ACT.Automation.Mechanical.TreeGroupingFolder
](True)

# %%
# Finding Duplicate Objects by Name
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Identify duplicate objects in the project tree based on their names.

import collections

# Retrieve all objects and their names
AllObj = ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.DataModelObject, True)
AllObjNames = [x.Name for x in AllObj]

# Find duplicate names
duplicates_by_name = [item for item, count in collections.Counter(AllObjNames).items() if count > 1]
print(duplicates_by_name)


# sphinx_gallery_start_ignore
# Add a static structural analysis and equivalent stress result for testing
static_struct = Model.AddStaticStructuralAnalysis()
static_struct.Solution.AddEquivalentStress()
# sphinx_gallery_end_ignore


# %%
# Using DataObjects and GetByName
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Access specific data objects by their names.
c1 = "Solution"
c2 = "Equivalent Stress"
c = DataModel.AnalysisList[0].DataObjects.GetByName(c1).DataObjects.GetByName(c2)

# %%
# Using DataObjects, NamesByType, and GetByName
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Access and filter contact regions based on their properties.

new_contact_list = []
dataobjects = ExtAPI.DataModel.AnalysisList[0].DataObjects
for group in dataobjects:
    print(group.Type)

# Retrieve names of all contact groups
names = dataobjects.NamesByType("ContactGroup")
for name in names:
    connet_data_objects = dataobjects.GetByName(name).DataObjects
    c_names = connet_data_objects.Names
    for c_name in c_names:
        type_c = connet_data_objects.GetByName(c_name).Type
        if type_c == "ConnectionGroup":
            contacts_list = connet_data_objects.GetByName(c_name).DataObjects.NamesByType(
                "ContactRegion"
            )
            for contact in contacts_list:
                contact_type = (
                    connet_data_objects.GetByName(c_name)
                    .DataObjects.GetByName(contact)
                    .PropertyValue("ContactType")
                )
                contact_state = (
                    connet_data_objects.GetByName(c_name)
                    .DataObjects.GetByName(contact)
                    .PropertyValue("Suppressed")
                )
                if contact_state == 0 and contact_type == 1:
                    new_contact_list.append(contact)
print(new_contact_list)

# %%
# Using GetObjectsByName
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Access a specific object by its name.
bb = ExtAPI.DataModel.GetObjectsByName("Connector\Solid1")[0]

# %%
# Accessing a Named Selection
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Access specific named selections by their names.

NSall = ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[
    Ansys.ACT.Automation.Mechanical.NamedSelection
](True)
my_nsel = [i for i in NSall if i.Name.startswith("NSF")][0]
my_nsel2 = [i for i in NSall if i.Name == "NSInsideFaces"][0]

# %%
# Get All Unsuppressed Bodies and Point Masses
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Example of getting all unsuppressed bodies and point masses.

# Retrieve all unsuppressed bodies
all_bodies = ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.Body, True)
all_bodies = [i for i in all_bodies if not i.Suppressed]
print(len(all_bodies))

# Retrieve all unsuppressed point masses
all_pm = ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.PointMass, True)
all_pm = [i for i in all_pm if not i.Suppressed]


# sphinx_gallery_start_ignore
# Save the Mechanical database file
from pathlib import Path

output_path = Path.cwd() / "out"
test_mechdat_path = str(output_path / "test.mechdat")
# app.save_as(test_mechdat_path, overwrite=True)


# Close the application and delete downloaded files
app.close()
# delete_downloads()
# sphinx_gallery_end_ignore
