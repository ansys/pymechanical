""".. _ref_tree_objects:

Tree Objects
------------

This section has helper scripts for Tree Objects.
"""



# sphinx_gallery_start_ignore
from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file
app = App(globals=globals())
geom_file_path = download_file("Valve.pmdb", "pymechanical", "embedding")
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
# Accessing Geometry
# ~~~~~~~~~~~~~~~~~~
# Example of accessing geometry by ID.

body = ExtAPI.DataModel.GeoData.GeoEntityById(312)

# %%
# Accessing Mesh Data
# ~~~~~~~~~~~~~~~~~~~~~~
# Example of accessing mesh data by name.

node = ExtAPI.DataModel.MeshDataByName("Global").NodeById(555)
element = ExtAPI.DataModel.MeshDataByName("Global").ElementById(444)

# %%
# Accessing All Objects and Child Objects
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Examples of accessing all objects, bodies, named selections, and contact regions.

# All tree objects
AllObj = ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.DataModelObject, True)

# All bodies
all_bodies = ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.Body, True)

# All named selections
ns_all = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.NamedSelections.NamedSelection)

# All contact regions
abc = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.ContactRegion)
all_contacts = ExtAPI.DataModel.Project.Model.Connections.GetChildren(DataModelObjectCategory.ContactRegion, True)

# A specific contact region
my_contact = [contact for contact in all_contacts if contact.Name == "Contact Region"][0]

# All result objects of a specific type
all_norm_stress = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.Result.NormalStress)

# Other examples
all_remote_points = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.RemotePoint)
ana = ExtAPI.DataModel.Tree.GetObjectsByType(DataModelObjectCategory.Analysis)

# Using ACT Automation API
all_contacts2 = ExtAPI.DataModel.Project.Model.Connections.GetChildren[Ansys.ACT.Automation.Mechanical.Connections.ContactRegion](True)
all_remote_points2 = ExtAPI.DataModel.Project.Model.GetChildren[Ansys.ACT.Automation.Mechanical.RemotePoint](True)
all_folders = ExtAPI.DataModel.Project.Model.GetChildren[Ansys.ACT.Automation.Mechanical.TreeGroupingFolder](True)

# %%
# Finding Duplicate Objects by Name
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Example of finding duplicate objects by name.

import collections

AllObj = ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.DataModelObject, True)
AllObjNames = [x.Name for x in AllObj]
duplicates_by_name = [item for item, count in collections.Counter(AllObjNames).items() if count > 1]
print(duplicates_by_name)

# %%
# Using DataObjects and GetByName
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Example of using DataObjects and GetByName.

c1 = 'Solution'
c2 = 'Far-field Sound Power Level Waterfall Diagram'
c = ExtAPI.DataModel.AnalysisList[0].DataObjects.GetByName(c1).DataObjects.GetByName(c2)

# %%
# Using DataObjects, NamesByType, and GetByName
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Example of using DataObjects, NamesByType, and GetByName.

new_contact_list = []
dataobjects = ExtAPI.DataModel.AnalysisList[0].DataObjects
for group in dataobjects:
    print(group.Type)
names = dataobjects.NamesByType('ContactGroup')
for name in names:
    connet_data_objects = dataobjects.GetByName(name).DataObjects
    c_names = connet_data_objects.Names
    for c_name in c_names:
        type_c = connet_data_objects.GetByName(c_name).Type
        if type_c == 'ConnectionGroup':
            contacts_list = connet_data_objects.GetByName(c_name).DataObjects.NamesByType('ContactRegion')
            for contact in contacts_list:
                contact_type = connet_data_objects.GetByName(c_name).DataObjects.GetByName(contact).PropertyValue('ContactType')
                contact_state = connet_data_objects.GetByName(c_name).DataObjects.GetByName(contact).PropertyValue("Suppressed")
                if contact_state == 0 and contact_type == 1:
                    new_contact_list.append(contact)
print(new_contact_list)

# %%
# Using GetObjectsByName
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Example of using GetObjectsByName.

bb = ExtAPI.DataModel.GetObjectsByName("Gray Cast Iron")[0]

# %%
# Accessing a Named Selection
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Example of accessing a named selection.

NSall = ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
my_nsel = [i for i in NSall if i.Name.startswith("b")][0]
my_nsel2 = [i for i in NSall if i.Name == "aaa"][0]

# %%
# Get All Unsuppressed Bodies and Point Masses
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Example of getting all unsuppressed bodies and point masses.

all_bodies = ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.Body, True)
all_bodies = [i for i in all_bodies if not i.Suppressed]
print(len(all_bodies))

all_pm = ExtAPI.DataModel.Project.Model.GetChildren(DataModelObjectCategory.PointMass, True)
all_pm = [i for i in all_pm if not i.Suppressed]




# sphinx_gallery_start_ignore
# Save the mechdat
from pathlib import Path

output_path = Path.cwd() / "out"
test_mechdat_path = str(output_path / "test.mechdat")
# app.save_as(test_mechdat_path, overwrite=True)


# Close the app
app.close()
# Delete the downloaded files
delete_downloads()
# sphinx_gallery_end_ignore
