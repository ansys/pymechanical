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

""".. _ref_connections:

Connections
-----------

This section has helper scripts for Connections.
"""

# sphinx_gallery_start_ignore
from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

app = App(globals=globals())

# Download the geometry file for the example
geom_file_path = download_file("example_06_bolt_pret_geom.agdb", "pymechanical", "00_basic")

# Import the geometry into the Mechanical model
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()

# Set preferences for geometry import
geometry_import_preferences.ProcessLines = True
geometry_import_preferences.NamedSelectionKey = ""
geometry_import_preferences.ProcessNamedSelections = True
geometry_import_preferences.ProcessMaterialProperties = True

# Perform the geometry import
geometry_import.Import(geom_file_path, geometry_import_format, geometry_import_preferences)
# sphinx_gallery_end_ignore

# Plot the imported geometry
app.plot()

# Print the tree structure of the Mechanical model
app.print_tree()

# %%
# Get information about all Contacts Defined
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Retrieve all contact regions defined in the model
all_contacts = Model.Connections.GetChildren(
    DataModelObjectCategory.ContactRegion, True
)

# Print count of all contact regions
numContacts = all_contacts.Count
print("There are %s contact regions" % (numContacts) )

# Print details of each contact region
for contact in all_contacts:
    print(
        f"\n{contact.Parent.Name} > {contact.Name} : {contact.ContactType} : "
        f"{contact.Suppressed} : {contact.ContactFormulation}"
    )
    print("Contact: ", contact.ContactBodies, list(contact.SourceLocation.Ids))
    print("Target: ", contact.TargetBodies, list(contact.TargetLocation.Ids))



# %%
# Create Automatic Connections on a chosen named selection
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create a new connection group for automatic connections

contactgroup = Model.Connections.AddConnectionGroup()
contactgroup.FaceFace = True
contactgroup.FaceEdge = contactgroup.FaceEdge.No
contactgroup.GroupBy = contactgroup.GroupBy.Faces
contactgroup.Priority = contactgroup.Priority.FaceOverEdge
contactgroup.InternalObject.DetectCylindricalFacesType = 1

# Retrieve a named selection for the connection group
NSall = Model.NamedSelections.GetChildren[
    Ansys.ACT.Automation.Mechanical.NamedSelection
](True)
my_nsel = [i for i in NSall if i.Name == "bodies_5"][0]

# Assign the named selection to the connection group and create automatic connections
contactgroup.Location = my_nsel
contactgroup.CreateAutomaticConnections()

# Refresh the tree structure to reflect the changes
DataModel.Tree.Refresh()

# %%
# Create a Contact region using face named selections
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Add a new contact region to the model
c = DataModel.Project.Model.Connections
c1 = c.AddContactRegion()

# Retrieve named selections for the source and target locations
NSall = Model.NamedSelections.GetChildren[
    Ansys.ACT.Automation.Mechanical.NamedSelection
](True)
a = [i for i in NSall if i.Name == "block1_washer_cont"][0]
c1.TargetLocation = a
a = [i for i in NSall if i.Name == "block1_washer_targ"][0]
c1.SourceLocation = a


# %%
# Insert a fixed body to ground joint
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
connections = Model.Connections
fixed_joint = connections.AddJoint()
fixed_joint.ConnectionType=JointScopingType.BodyToGround
fixed_joint.Type = JointType.Fixed
fixed_joint.MobileLocation = app.DataModel.GetObjectsByName("block1_washer_cont")[0]



# %%
# Insert a Joint using face IDs
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Define face IDs for the joint
face1 = 135
face2 = 160


from pathlib import Path  # delete

output_path = Path.cwd() / "out"  # delete
test_mechdat_path = str(output_path / "temporarycheck.mechdat")  # delete
app.save_as(test_mechdat_path, overwrite=True)  # delete

# Add a new joint to the model
j = Model.Connections.AddJoint()

# Define the reference and mobile locations for the joint using face IDs
reference_scoping = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
reference_scoping.Ids = [face1]
j.ReferenceLocation = reference_scoping

mobile_scoping = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
mobile_scoping.Ids = [face2]
j.MobileLocation = mobile_scoping

# %%
# Define a ground to body spring with 1 N/m stiffness scoped to preexisting named selection
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
connections = Model.Connections
spring = connections.AddSpring()
spring.ConnectionType=JointScopingType.BodyToGround
spring.LongitudinalStiffness = Quantity(1, "N m^-1")
spring.MobileScopingMethod = GeometryDefineByType.Component
spring.MobileScopeLocation = app.DataModel.GetObjectsByName("block1_washer_cont")[0]


# %%
# Define a Bearing
# ~~~~~~~~~~~~~~~~
# Add a new bearing connection to the model
brg = Model.Connections.AddBearing()

# Set the reference rotation plane for the bearing
brg.ReferenceRotationPlane = RotationPlane.XY

# Define stiffness values for the bearing
brg.StiffnessK11.Output.DiscreteValues = [Quantity("11 [N/m]")]
brg.StiffnessK22.Output.DiscreteValues = [Quantity("22 [N/m]")]
brg.StiffnessK21.Output.DiscreteValues = [Quantity("21 [N/m]")]
brg.StiffnessK12.Output.DiscreteValues = [Quantity("12 [N/m]")]

# Define damping values for the bearing
brg.DampingC11.Output.DiscreteValues = [Quantity("111 [N sec m^-1]")]
brg.DampingC22.Output.DiscreteValues = [Quantity("122 [N sec m^-1]")]
brg.DampingC12.Output.DiscreteValues = [Quantity("112 [N sec m^-1]")]
brg.DampingC21.Output.DiscreteValues = [Quantity("121 [N sec m^-1]")]

# Retrieve named selections for the reference and mobile locations
NSall = Model.NamedSelections.GetChildren[
    Ansys.ACT.Automation.Mechanical.NamedSelection
](True)
brg.ReferenceLocation = [i for i in NSall if i.Name == "shank_surface"][0]
brg.MobileLocation = [i for i in NSall if i.Name == "shank_surface"][0]


# sphinx_gallery_start_ignore
# Save the Mechanical database file
from pathlib import Path

output_path = Path.cwd() / "out"
test_mechdat_path = str(output_path / "test.mechdat")
# app.save_as(test_mechdat_path, overwrite=True)


# Close the application and delete downloaded files
app.close()
delete_downloads()
# sphinx_gallery_end_ignore
