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

""".. _ref_bolt_pretension:

Bolt pretension
---------------

This example demonstrates how to insert a Static Structural analysis
into a new Mechanical session and execute a sequence of Python scripting
commands that define and solve a bolt-pretension analysis.
Scripts then evaluate the following results: deformation,
equivalent stresses, contact, and bolt.
"""

# %%
# Import the necessary libraries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from pathlib import Path
import typing

from matplotlib import pyplot as plt
import matplotlib.animation as animation
from PIL import Image

from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

# %%
# Initialize the embedded application
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app = App()
print(app)

# Import the enums and global variables instead of using app.update_globals(globals())
# or App(globals=globals())
from ansys.mechanical.core.embedding.enum_importer import *  # noqa: F403
from ansys.mechanical.core.embedding.global_importer import Quantity
from ansys.mechanical.core.embedding.transaction import Transaction

# %%
# Configure view and path for image export
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Set camera orientation
graphics = app.Graphics
camera = graphics.Camera
camera.SetSpecificViewOrientation(ViewOrientationType.Iso)
camera.SetFit()
camera.Rotate(180, CameraAxisType.ScreenY)

# Set the path for the output files (images, gifs, mechdat)
output_path = Path.cwd() / "out"


# %%
# Download and import the geometry
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Download the geometry file from the ansys/example-data repository
geometry_path = download_file("example_06_bolt_pret_geom.pmdb", "pymechanical", "00_basic")

# Import/reload the geometry from the CAD (pmdb) file using the provided preferences
geometry_import = app.helpers.import_geometry(geometry_path)
# sphinx_gallery_start_ignore
# Assert the geometry import was successful
assert geometry_import.ObjectState == ObjectState.Solved, "Geometry Import unsuccessful"
# sphinx_gallery_end_ignore

# Visualize the model in 3D
app.plot()

# %%
# Download and import the materials
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Download the material files from the ansys/example-data repository
copper_material_file_path = download_file("example_06_Mat_Copper.xml", "pymechanical", "00_basic")
steel_material_file_path = download_file("example_06_Mat_Steel.xml", "pymechanical", "00_basic")

# %%
# Add materials to the model and import the material files
app.helpers.import_materials(copper_material_file_path)
app.helpers.import_materials(steel_material_file_path)

# %%
# Define analysis and unit system
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Add static structural analysis to the model
model = app.Model
model.AddStaticStructuralAnalysis()
static_structural = model.Analyses[0]
static_structural_solution = static_structural.Solution
static_structural_analysis_setting = static_structural.Children[0]

# %%
# Store the named selections
named_selections_dictionary = {}
named_selections_list = [
    "block3_block2_cont",
    "block3_block2_targ",
    "shank_block3_cont",
    "shank_block3_targ",
    "block1_washer_cont",
    "block1_washer_targ",
    "washer_bolt_cont",
    "washer_bolt_targ",
    "shank_bolt_targ",
    "shank_bolt_cont",
    "block2_block1_cont",
    "block2_block1_targ",
]

# %%
# Set the unit system to Standard NMM

app.ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMM

# %%
# Get tree objects for each named selection
for named_selection in named_selections_list:
    named_selections_dictionary[named_selection] = app.DataModel.GetObjectsByName(named_selection)[
        0
    ]

# %%
# Create a list with material assignment for each ``model.Geometry.Children`` index
children_materials = ["Steel", "Copper", "Copper", "Steel", "Steel", "Steel"]

# %%
# Assign surface materials to the ``model.Geometry`` bodies
geometry = model.Geometry
for children_index, material_name in enumerate(children_materials):
    # Get the surface of the body
    surface = geometry.Children[children_index].Children[0]
    # Assign the material to the surface
    surface.Material = material_name

# %%
# Add and define a coordinate system
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Add a coordinate system to the model
coordinate_systems = model.CoordinateSystems
coordinate_system = coordinate_systems.AddCoordinateSystem()

# %%
# Define the coordinate system and set its axis properties
coordinate_system.OriginDefineBy = CoordinateSystemAlignmentType.Fixed
coordinate_system.OriginX = Quantity(-195, "mm")
coordinate_system.OriginY = Quantity(100, "mm")
coordinate_system.OriginZ = Quantity(50, "mm")
coordinate_system.PrimaryAxis = CoordinateSystemAxisType.PositiveZAxis

# %%
# Create functions for contact region set up
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# %%
# Add a contact region to the body with the specified source location, target location,
# and contact type
def set_contact_region_locations_and_types(
    body: typing.Union[
        "Ansys.ACT.Automation.Mechanical.Connections",
        "Ansys.ACT.Automation.Mechanical.Connections.ConnectionGroup",
    ],
    source_location: "Ansys.ACT.Automation.Mechanical.NamedSelection",
    target_location: "Ansys.ACT.Automation.Mechanical.NamedSelection",
    contact_type: "ContactType",
) -> "Ansys.ACT.Automation.Mechanical.Connections.ContactRegion":
    """Add a contact region to the body with the specified source location, target location,
    and contact type.

    Parameters
    ----------
    body : Ansys.ACT.Automation.Mechanical.Connections or
    Ansys.ACT.Automation.Mechanical.Connections.ConnectionGroup
        The body to which the contact region will be added.
    source_location : Ansys.ACT.Automation.Mechanical.NamedSelection
        The source location for the contact region.
    target_location : Ansys.ACT.Automation.Mechanical.NamedSelection
        The target location for the contact region.
    contact_type : ContactType
        The type of contact for the contact region.

    Returns
    -------
    Ansys.ACT.Automation.Mechanical.Connections.ContactRegion
        The created contact region.
    """
    contact_region = body.AddContactRegion()
    contact_region.SourceLocation = source_location
    contact_region.TargetLocation = target_location
    contact_region.ContactType = contact_type
    return contact_region


# %%
# Set the friction coefficient, small sliding, and update stiffness settings for the contact region
def advanced_contact_settings(
    contact_region: Ansys.ACT.Automation.Mechanical.Connections.ContactRegion,
    friction_coefficient: int,
    small_sliding: ContactSmallSlidingType,
    update_stiffness: UpdateContactStiffness,
) -> None:
    """Set the friction coefficient, small sliding, and update stiffness settings for the
    contact region.

    Parameters
    ----------
    contact_region : Ansys.ACT.Automation.Mechanical.Connections.ContactRegion
        The contact region to set the settings for.
    friction_coefficient : int
        The friction coefficient for the contact region.
    small_sliding : ContactSmallSlidingType
        The small sliding setting for the contact region.
    update_stiffness : UpdateContactStiffness
        The update stiffness setting for the contact region.
    """
    contact_region.FrictionCoefficient = friction_coefficient
    contact_region.SmallSliding = small_sliding
    contact_region.UpdateStiffness = update_stiffness


# %%
# Add a command snippet to the contact region with the specified Archard Wear Model
def add_command_snippet(
    contact_region: "Ansys.ACT.Automation.Mechanical.Connections.ContactRegion",
    archard_wear_model: str,
) -> None:
    """Add a command snippet to the contact region with the specified Archard Wear Model.

    Parameters
    ----------
    contact_region : Ansys.ACT.Automation.Mechanical.Connections.ContactRegion
        The contact region to add the command snippet to.
    archard_wear_model : str
        The Archard Wear Model command snippet to add to the contact region.
    """
    contact_region_cmd = contact_region.AddCommandSnippet()
    contact_region_cmd.AppendText(archard_wear_model)


# %%
# Add and define contact regions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Set up the model connections and delete the existing connections for ConnectionGroups
connections = model.Connections
for connection in connections.Children:
    if connection.DataModelObjectCategory == DataModelObjectCategory.ConnectionGroup:
        app.DataModel.Remove(connection)

# %%
# Set the archard wear model and get the named selections from the model

# Set the archard wear model
archard_wear_model = """keyopt,cid,9,5
rmodif,cid,10,0.00
rmodif,cid,23,0.001"""

# Get named selections from the model for contact regions
named_selections = model.NamedSelections

# %%
# Add a contact region for the model's named selections Children 0 and 1 with the specified
# contact type
contact_region = set_contact_region_locations_and_types(
    body=connections,
    source_location=named_selections.Children[0],
    target_location=named_selections.Children[1],
    contact_type=ContactType.Frictional,
)
# Set the friction coefficient, small sliding, and update stiffness settings for the contact region
advanced_contact_settings(
    contact_region=contact_region,
    friction_coefficient=0.2,
    small_sliding=ContactSmallSlidingType.Off,
    update_stiffness=UpdateContactStiffness.Never,
)
# Add a command snippet to the contact region with the specified Archard Wear Model
add_command_snippet(contact_region, archard_wear_model)

# %%
# Set the connection group for the contact regions
connection_group = connections.Children[0]

# %%
# Add a contact region for the model's named selections Children 2 and 3 with the specified
# contact type
contact_region_2 = set_contact_region_locations_and_types(
    body=connection_group,
    source_location=named_selections.Children[3],
    target_location=named_selections.Children[2],
    contact_type=ContactType.Bonded,
)
contact_region_2.ContactFormulation = ContactFormulation.MPC

# %%
# Add a contact region for the model's named selections Children 4 and 5 with the specified
# contact type
contact_region_3 = set_contact_region_locations_and_types(
    body=connection_group,
    source_location=named_selections.Children[4],
    target_location=named_selections.Children[5],
    contact_type=ContactType.Frictional,
)
# Set the friction coefficient, small sliding, and update stiffness settings for the contact region
advanced_contact_settings(
    contact_region=contact_region_3,
    friction_coefficient=0.2,
    small_sliding=ContactSmallSlidingType.Off,
    update_stiffness=UpdateContactStiffness.Never,
)
# Add a command snippet to the contact region with the specified Archard Wear Model
add_command_snippet(contact_region_3, archard_wear_model)

# %%
# Add a contact region for the model's named selections Children 6 and 7 with the specified
# contact type
contact_region_4 = set_contact_region_locations_and_types(
    body=connection_group,
    source_location=named_selections.Children[6],
    target_location=named_selections.Children[7],
    contact_type=ContactType.Bonded,
)
contact_region_4.ContactFormulation = ContactFormulation.MPC

# %%
# Add a contact region for the model's named selections Children 8 and 9 with the specified
# contact type
contact_region_5 = set_contact_region_locations_and_types(
    body=connection_group,
    source_location=named_selections.Children[9],
    target_location=named_selections.Children[8],
    contact_type=ContactType.Bonded,
)
contact_region_5.ContactFormulation = ContactFormulation.MPC

# %%
# Add a contact region for the model's named selections Children 10 and 11 with the specified
# contact type
contact_region_6 = set_contact_region_locations_and_types(
    body=connection_group,
    source_location=named_selections.Children[10],
    target_location=named_selections.Children[11],
    contact_type=ContactType.Frictional,
)
# Set the friction coefficient, small sliding, and update stiffness settings for the contact region
advanced_contact_settings(
    contact_region=contact_region_6,
    friction_coefficient=0.2,
    small_sliding=ContactSmallSlidingType.Off,
    update_stiffness=UpdateContactStiffness.Never,
)
# Add a command snippet to the contact region with the specified Archard Wear Model
add_command_snippet(contact_region_6, archard_wear_model)

# %%
# Create functions to set up the mesh
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# %%
# Set the mesh method location for the specified method and object name
def set_mesh_method_location(method, object_name: str, location_type: str = "") -> None:
    """Set the location of the method based on the specified name and location type.

    Parameters
    ----------
    method : Ansys.ACT.Automation.Mechanical.MeshMethod
        The method to set the location for.
    object_name : str
        The name of the object to set the location for.
    location_type : str, optional
        The type of location to set for the method. Can be "source", "target", or empty string.
        Default is an empty string.
    """
    # Get the tree object for the specified name
    tree_obj = app.DataModel.GetObjectsByName(object_name)[0]

    # Set the method location based on the specified location type
    if location_type == "source":
        method.SourceLocation = tree_obj
    elif location_type == "target":
        method.TargetLocation = tree_obj
    else:
        method.Location = tree_obj


# %%
# Add a mesh sizing to the mesh with the specified name, quantity value, and measurement
def add_mesh_sizing(mesh, object_name: str, element_size: Quantity) -> None:
    """Add a mesh sizing to the mesh with the specified name, quantity value, and measurement.

    Parameters
    ----------
    mesh : Ansys.ACT.Automation.Mechanical.Mesh
        The mesh to add the sizing to.
    object_name : str
        The name of the object to set the sizing for.
    element_size : Quantity
        The element size for the mesh sizing.
    """
    # Add sizing to the mesh
    body_sizing = mesh.AddSizing()
    # Get the tree object for the specified name
    body_sizing.Location = app.DataModel.GetObjectsByName(object_name)[0]

    # Set the element size to the mesh
    body_sizing.ElementSize = element_size


# %%
# Add mesh methods, sizing, and face meshing
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Add the mesh sizing to the ``bodies_5`` and ``shank`` objects

mesh = model.Mesh
add_mesh_sizing(mesh=mesh, object_name="bodies_5", element_size=Quantity(15, "mm"))
add_mesh_sizing(mesh=mesh, object_name="shank", element_size=Quantity(7, "mm"))

# %%
# Add an automatic method to the mesh and set the method type
hex_method = mesh.AddAutomaticMethod()
hex_method.Method = MethodType.Automatic
# Set the method location for the all_bodies object
set_mesh_method_location(method=hex_method, object_name="all_bodies")

# %%
# Add face meshing to the mesh and set the MappedMesh property to False
face_meshing = mesh.AddFaceMeshing()
face_meshing.MappedMesh = False
# Set the method location for the face meshing
set_mesh_method_location(method=face_meshing, object_name="shank_face")

# %%
# Add an automatic method to the mesh, set the method type, and set the source target selection
sweep_method = mesh.AddAutomaticMethod()
sweep_method.Method = MethodType.Sweep
sweep_method.SourceTargetSelection = 2
# Set the method locations for the shank, shank_face, and shank_face2 objects
set_mesh_method_location(method=sweep_method, object_name="shank")
set_mesh_method_location(method=sweep_method, object_name="shank_face", location_type="source")
set_mesh_method_location(method=sweep_method, object_name="shank_face2", location_type="target")

# %%
# Activate and generate the mesh
mesh.Activate()
mesh.GenerateMesh()

# Set the image export format, path and export the image
mesh_image_path = str(output_path / "mesh.png")
camera.SetFit()
app.helpers.export_image(mesh, mesh_image_path)

# %%
# Display the mesh image
app.helpers.display_image(mesh_image_path)

# %%
# Analysis settings
# ~~~~~~~~~~~~~~~~~

# Set the number of steps for the static structural analysis
static_structural_analysis_setting.NumberOfSteps = 4

# Set the step index list
step_index_list = [1]

# Set the automatic time stepping method for the static structural analysis
# based on the step index
with Transaction():
    for step_index in step_index_list:
        static_structural_analysis_setting.SetAutomaticTimeStepping(
            step_index, AutomaticTimeStepping.Off
        )

# Set the number of substeps for the static structural analysis
# based on the step index
with Transaction():
    for step_index in step_index_list:
        static_structural_analysis_setting.SetNumberOfSubSteps(step_index, 2)

# Activate the static structural analysis settings
static_structural_analysis_setting.Activate()

# Set the solver type and solver pivoting check for the static structural analysis
static_structural_analysis_setting.SolverType = SolverType.Direct
static_structural_analysis_setting.SolverPivotChecking = SolverPivotChecking.Off

# %%
# Define loads and boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add fixed support to the static structural analysis
fixed_support = static_structural.AddFixedSupport()
# Set the fixed support location for the block2_surface object
set_mesh_method_location(method=fixed_support, object_name="block2_surface")

# Create a new force on the static structural analysis
tabular_force = static_structural.AddForce()
# Set the force location for the bottom_surface object
set_mesh_method_location(method=tabular_force, object_name="bottom_surface")

# Define the tabular force input and output components
tabular_force.DefineBy = LoadDefineBy.Components
tabular_force.XComponent.Inputs[0].DiscreteValues = [
    Quantity(0, "s"),
    Quantity(1, "s"),
    Quantity(2, "s"),
    Quantity(3, "s"),
    Quantity(4, "s"),
]
tabular_force.XComponent.Output.DiscreteValues = [
    Quantity(0, "N"),
    Quantity(0, "N"),
    Quantity(5.0e005, "N"),
    Quantity(0, "N"),
    Quantity(-5.0e005, "N"),
]

# Add a bolt presentation to the static structural analysis
bolt_presentation = static_structural.AddBoltPretension()
# Set the bolt presentation location for the shank_surface object
set_mesh_method_location(bolt_presentation, "shank_surface")

# Define the bolt presentation input and output components
bolt_presentation.Preload.Inputs[0].DiscreteValues = [
    Quantity(1, "s"),
    Quantity(2, "s"),
    Quantity(3, "s"),
    Quantity(4, "s"),
]
bolt_presentation.Preload.Output.DiscreteValues = [
    Quantity(6.1363e005, "N"),
    Quantity(0, "N"),
    Quantity(0, "N"),
    Quantity(0, "N"),
]
bolt_presentation.SetDefineBy(2, BoltLoadDefineBy.Lock)
bolt_presentation.SetDefineBy(3, BoltLoadDefineBy.Lock)
bolt_presentation.SetDefineBy(4, BoltLoadDefineBy.Lock)

# Activate the bolt presentation
app.Tree.Activate([bolt_presentation])

# Set the image path for the loads and boundary conditions
loads_boundary_conditions_image_path = str(output_path / "loads_boundary_conditions.png")
# Export the image of the loads and boundary conditions

camera.SetFit()
app.helpers.export_image(bolt_presentation, loads_boundary_conditions_image_path)
# Display the image of the loads and boundary conditions
app.helpers.display_image(loads_boundary_conditions_image_path)

# %%
# Insert results
# ~~~~~~~~~~~~~~

# Add a contact tool to the static structural solution and set the scoping method for it
post_contact_tool = static_structural_solution.AddContactTool()
post_contact_tool.ScopingMethod = GeometryDefineByType.Worksheet

# Add a bolt tool to the static structural solution and add a working load to it
bolt_tool = static_structural_solution.AddBoltTool()
bolt_tool.AddWorkingLoad()

# Add the total deformation to the static structural solution
total_deformation = static_structural_solution.AddTotalDeformation()

# Add equivalent stress to the static structural solution
equivalent_stress_1 = static_structural_solution.AddEquivalentStress()

# Add equivalent stress to the static structural solution and set the location for the shank object
equivalent_stress_2 = static_structural_solution.AddEquivalentStress()
set_mesh_method_location(method=equivalent_stress_2, object_name="shank")

# Add a force reaction to the static structural solution and set the boundary condition selection
# to the fixed support
force_reaction_1 = static_structural_solution.AddForceReaction()
force_reaction_1.BoundaryConditionSelection = fixed_support

# Add a moment reaction to the static structural solution and set the boundary condition selection
# to the fixed support
moment_reaction_2 = static_structural_solution.AddMomentReaction()
moment_reaction_2.BoundaryConditionSelection = fixed_support

# %%
# Solve the static structural solution
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Solve the static structural solution and wait for it to finish
static_structural_solution.Solve(True)

# sphinx_gallery_start_ignore
# Assert the solution status is "Done"
assert static_structural_solution.Status == SolutionStatusType.Done, "Solution status is not 'Done'"
# sphinx_gallery_end_ignore

# %%
# Show messages
# ~~~~~~~~~~~~~

# Print all messages from Mechanical
app.messages.show()

# %%
# Display the results
# ~~~~~~~~~~~~~~~~~~~

# %%
# Total deformation

# Set the image name and path for the object
image_path = str(output_path / "total_deformation.png")
# Export the image of the object
camera.SetFit()
app.helpers.export_image(total_deformation, file_path=image_path)
# Display the image of the object
app.helpers.display_image(image_path)

# %%
# Equivalent stress on all bodies

# Set the image name and path for the object
image_path = str(output_path / "equivalent_stress_all_bodies.png")
# Export the image of the object
camera.SetFit()
app.helpers.export_image(equivalent_stress_1, file_path=image_path)
# Display the image of the object
app.helpers.display_image(image_path)

# %%
# Equivalent stress on the shank

# Set the image name and path for the object
image_path = str(output_path / "equivalent_stress_shank.png")
# Export the image of the object
camera.SetFit()
app.helpers.export_image(equivalent_stress_2, file_path=image_path)
# Display the image of the object
app.helpers.display_image(image_path)

# %%
# Export the contact status animation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Get the post contact tool status
post_contact_tool_status = post_contact_tool.Children[0]

# Set the path for the contact status GIF
contact_status_gif_path = str(output_path / "contact_status.gif")
camera.SetFit()
app.helpers.export_animation(post_contact_tool_status, contact_status_gif_path)

# %%
# Display the contact status animation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Open the GIF file and create an animation
gif = Image.open(contact_status_gif_path)
fig, ax = plt.subplots(figsize=(8, 4))
ax.axis("off")
image = ax.imshow(gif.convert("RGBA"))


# Animation update function
def update_frame(frame):
    """Update the frame for the animation."""
    gif.seek(frame)
    image.set_array(gif.convert("RGBA"))
    return (image,)


# Create and display animation
ani = animation.FuncAnimation(
    fig, update_frame, frames=gif.n_frames, interval=200, blit=True, repeat=True
)

# Show the animation
plt.show()


# %%
# Clean up the project
# ~~~~~~~~~~~~~~~~~~~~

# Save the project
bolt_presentation_mechdat_path = str(output_path / "bolt_pretension.mechdat")
app.save_as(bolt_presentation_mechdat_path, overwrite=True)

# Close the app
app.close()

# Delete the example files
delete_downloads()
