""".. _ref_connections:

Connections
-----------

This section has helper scripts for Connections.
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
# sphinx_gallery_end_ignore

app.plot()


# %%
# Get information about all Contacts Defined
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
all_contacts = ExtAPI.DataModel.Project.Model.Connections.GetChildren(
    DataModelObjectCategory.ContactRegion, True
)
for contact in all_contacts:
    print(
        f"\n{contact.Parent.Name} > {contact.Name} : {contact.ContactType} : {contact.Suppressed} : {contact.ContactFormulation}"
    )
    print("Contact: ", contact.ContactBodies, list(contact.SourceLocation.Ids))
    print("Target: ", contact.TargetBodies, list(contact.TargetLocation.Ids))

# %%
# Insert a Joint using face IDs
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
face1 = 44
face2 = 251

model = ExtAPI.DataModel.Project.Model
j = model.Connections.AddJoint()

reference_scoping = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
reference_scoping.Ids = [face1]
j.ReferenceLocation = reference_scoping

mobile_scoping = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
mobile_scoping.Ids = [face2]
j.MobileLocation = mobile_scoping

# %%
# Create Automatic Connections on a chosen named selection
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
contactgroup = ExtAPI.DataModel.Project.Model.Connections.AddConnectionGroup()
contactgroup.FaceFace = True
contactgroup.FaceEdge = contactgroup.FaceEdge.No
contactgroup.GroupBy = contactgroup.GroupBy.Faces
contactgroup.Priority = contactgroup.Priority.FaceOverEdge
contactgroup.InternalObject.DetectCylindricalFacesType = 1

NSall = ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[
    Ansys.ACT.Automation.Mechanical.NamedSelection
](True)
my_nsel = [i for i in NSall if i.Name == "bodies3"][0]

contactgroup.Location = my_nsel
contactgroup.CreateAutomaticConnections()

mytree = ExtAPI.DataModel.Tree
mytree.Refresh()

# %%
# Create a Contact region using face named selections
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c = ExtAPI.DataModel.Project.Model.Connections
c1 = c.AddContactRegion()
NSall = ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[
    Ansys.ACT.Automation.Mechanical.NamedSelection
](True)
a = [i for i in NSall if i.Name == "faces_tube"][0]
c1.TargetLocation = a
a = [i for i in NSall if i.Name == "faces_bracket"][0]
c1.SourceLocation = a

# %%
# Define a Bearing
# ~~~~~~~~~~~~~~~~
brg = ExtAPI.DataModel.Project.Model.Connections.AddBearing()
brg.ReferenceRotationPlane = RotationPlane.XY
brg.StiffnessK11.Output.DiscreteValues = [Quantity("11 [N/m]")]
brg.StiffnessK22.Output.DiscreteValues = [Quantity("22 [N/m]")]
brg.StiffnessK21.Output.DiscreteValues = [Quantity("21 [N/m]")]
brg.StiffnessK12.Output.DiscreteValues = [Quantity("12 [N/m]")]

brg.DampingC11.Output.DiscreteValues = [Quantity("111 [N sec m^-1]")]
brg.DampingC22.Output.DiscreteValues = [Quantity("122 [N sec m^-1]")]
brg.DampingC12.Output.DiscreteValues = [Quantity("112 [N sec m^-1]")]
brg.DampingC21.Output.DiscreteValues = [Quantity("121 [N sec m^-1]")]

NSall = ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[
    Ansys.ACT.Automation.Mechanical.NamedSelection
](True)
brg.ReferenceLocation = [i for i in NSall if i.Name == "f1"][0]
brg.MobileLocation = [i for i in NSall if i.Name == "f2"][0]


# sphinx_gallery_start_ignore
# Close the app
app.close()
# Delete the downloaded files
delete_downloads()
# sphinx_gallery_end_ignore
