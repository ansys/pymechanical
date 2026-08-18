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

""".. _ref_modal_acoustics_analysis:

Modal acoustics analysis
------------------------

This example demonstrate modal acoustic analysis that involves
modeling both a structure and the surrounding
fluid to analyze frequencies and standing wave patterns within the structure.
This type of analysis is essential for applications such as Sonar, concert hall design,
noise reduction in various settings, audio speaker design, and geophysical exploration.

Mechanical enables you to model pure acoustic problems and fluid-structure
interaction (FSI) problems. A coupled acoustic analysis accounts for FSI.
An uncoupled acoustic analysis simulates
the fluid only and ignores any fluid-structure interaction.
"""

# %%
# Import the necessary libraries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from pathlib import Path
from typing import TYPE_CHECKING

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image

from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

if TYPE_CHECKING:
    import Ansys

# %%
# Initialize the embedded application
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app = App(globals=globals())
print(app)

# Set the path for the output files (images, gifs, mechdat)
output_path = Path.cwd() / "out"
graphics = app.Graphics
camera = graphics.Camera

# %%
# Download the geometry and material files
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Download the geometry file from the ansys/example-data repository
geometry_path = download_file("sloshing_geometry.pmdb", "pymechanical", "embedding")
# Download the water material file from the ansys/example-data repository
mat_path = download_file("Water_material_explicit.xml", "pymechanical", "embedding")

# %%
# Import and display the geometry
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app.helpers.import_geometry(geometry_path, process_named_selections=True)
app.plot()

# %%
# Store all variables necessary for analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

model = app.Model
geometry = model.Geometry
mesh = model.Mesh
named_selections = model.NamedSelections
connections = model.Connections
materials = model.Materials

# %%
# Add modal acoustic analysis and import the material
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add a modal acoustic analysis to the model
model.AddModalAcousticAnalysis()
# Set the unit system to Standard MKS
app.ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardMKS
# Import the water material from the specified XML file
app.helpers.import_materials(mat_path)

# %%
# Assign material to solid bodies
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_solid_set_material(name: str) -> None:
    """Get the solid body by name and assign the material.

    Parameters
    ----------
    name : str
        The name of the solid body to get.
    """
    # Get the solid body by name
    solid = [
        i
        for i in geometry.GetChildren[Ansys.ACT.Automation.Mechanical.Body](True)
        if i.Name == name
    ][0]

    # Assign material water to acoustic parts
    solid.Material = "WATER"


# Assign material water to acoustic parts for solids 1 to 4
for i in range(1, 5):
    solid_name = f"Solid{i}"
    get_solid_set_material(solid_name)


# %%
# Add mesh methods and sizings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Create a function to get the named selection by name


def get_named_selection(name: str) -> Ansys.ACT.Automation.Mechanical.NamedSelection:
    """Get the named selection by name.

    Parameters
    ----------
    name : str
        The name of the named selection to get.

    Returns
    -------
    Ansys.ACT.Automation.Mechanical.NamedSelection
        The named selection object.
    """
    return [
        child
        for child in named_selections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](
            True
        )
        if child.Name == name
    ][0]


# %%
# Create a function to set the mesh properties


def set_mesh_properties(
    mesh_element,
    named_selection,
    method_type=None,
    element_size=None,
    behavior=None,
):
    """Set the properties for mesh automatic methods and sizings.

    Parameters
    ----------
    mesh_element
        The mesh element to set properties for.
    named_selection : Ansys.ACT.Automation.Mechanical.NamedSelection
        The named selection to set the location for the mesh element.
    method_type : MethodType, optional
        The method type for the mesh (default is None).
    element_size : Quantity, optional
        The element size for the mesh (default is None).
    behavior : SizingBehavior, optional
        The sizing behavior for the mesh (default is None).
    """
    mesh_element.Location = named_selection
    if method_type:
        mesh_element.Method = method_type
    if element_size:
        mesh_element.ElementSize = element_size
    if behavior:
        mesh_element.Behavior = behavior


# %%
# Add automatic mesh methods

mesh.ElementOrder = ElementOrder.Quadratic

method1 = mesh.AddAutomaticMethod()
acst_bodies = get_named_selection("Acoustic_bodies")
# Set the automatic method location to the acoustic bodies and the method type to AllTriAllTet
set_mesh_properties(method1, acst_bodies, MethodType.AllTriAllTet)

# Add an automatic mesh method
method2 = mesh.AddAutomaticMethod()
top_bodies = get_named_selection("top_bodies")
# Set the automatic method location to the top bodies and the method type to Automatic
set_mesh_properties(method2, top_bodies, MethodType.Automatic)

# %%
# Add mesh sizing

sizing1 = mesh.AddSizing()
# Set the mesh sizing location to the top bodies, the element size to 0.2m, and
# the sizing behavior to hard
set_mesh_properties(
    sizing1, top_bodies, element_size=Quantity("0.2 [m]"), behavior=SizingBehavior.Hard
)

sizing2 = mesh.AddSizing()
# Set the mesh sizing location to the acoustic bodies, the element size to 0.2m, and
# the sizing behavior to hard
set_mesh_properties(
    sizing2, acst_bodies, element_size=Quantity("0.2 [m]"), behavior=SizingBehavior.Hard
)

# %%
# Add a mesh method for the container bodies

# Add an automatic mesh method
method3 = mesh.AddAutomaticMethod()
container_bodies = get_named_selection("container_bodies")
# Set the automatic method location to the container bodies and the method type to Sweep
set_mesh_properties(method3, container_bodies, MethodType.Sweep)
# Set the source target selection to 4
method3.SourceTargetSelection = 4

# %%
# Generate the mesh and display the image

mesh.GenerateMesh()

image_path = output_path / "mesh.png"
camera.SetFit()
app.helpers.export_image(mesh, image_path)
app.helpers.display_image(image_path)

# %%
# Set up the contact regions in the connection group
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Create a function to set the contact region properties


def set_contact_region_properties(
    contact_region,
    source_location,
    target_location,
    contact_formulation=ContactFormulation.MPC,
    contact_behavior=ContactBehavior.Asymmetric,
    pinball_region=ContactPinballType.Radius,
    pinball_radius=Quantity("0.25 [m]"),
    set_target_before_src=False,
):
    """Set the properties for the contact region.

    Parameters
    ----------
    contact_region : Ansys.ACT.Automation.Mechanical.ContactRegion
        The contact region to set properties for.
    source_location : Ansys.ACT.Automation.Mechanical.NamedSelection
        The source location for the contact region.
    target_location : Ansys.ACT.Automation.Mechanical.NamedSelection
        The target location for the contact region.
    contact_formulation : ContactFormulation, optional
        The contact formulation for the contact region (default is MPC).
    contact_behavior : ContactBehavior, optional
        The contact behavior for the contact region (default is Asymmetric).
    pinball_region : ContactPinballType, optional
        The pinball region type for the contact region (default is Radius).
    pinball_radius : Quantity, optional
        The pinball radius for the contact region (default is 0.25 m).
    set_target_before_src : bool, optional
        Whether to set the target location before the source location (default is False).
    """
    # If the target location is set before the source location
    if set_target_before_src:
        contact_region.TargetLocation = get_named_selection(target_location)
        contact_region.SourceLocation = source_location
    else:
        contact_region.SourceLocation = get_named_selection(source_location)
        contact_region.TargetLocation = get_named_selection(target_location)
    contact_region.ContactFormulation = contact_formulation
    contact_region.Behavior = contact_behavior
    contact_region.PinballRegion = pinball_region
    contact_region.PinballRadius = pinball_radius


# %%
# Add contact regions and set their properties

# Add a connection group to the model
connection_group = connections.AddConnectionGroup()

# Add the first contact region to the connection group
contact_region_1 = connection_group.AddContactRegion()
# Set the source location to the Cont_V1 named selection and the target location to the Cont_face1
# named selection
set_contact_region_properties(contact_region_1, "Cont_V1", "Cont_face1")

# Add the second contact region to the connection group
contact_region_2 = connection_group.AddContactRegion()
# Set the source location to the Cont_V2 named selection and the target location to the Cont_face2
# named selection
set_contact_region_properties(contact_region_2, "Cont_V2", "Cont_face2")

# Add the third contact region to the connection group
contact_region_3 = connection_group.AddContactRegion()
# Set the source location to the Cont_V3 named selection and the target location to the Cont_face3
# named selection
set_contact_region_properties(contact_region_3, "Cont_V3", "Cont_face3")

# Set the selection manager
sel_manager = app.ExtAPI.SelectionManager
# Get the contact vertex from the geometry
contact_vertex = DataModel.GeoData.Assemblies[0].Parts[1].Bodies[0].Vertices[3]
# Create a selection info object for the contact vertex
contact_vertex_4 = sel_manager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
# Set the contact vertex as the selected entity
contact_vertex_4.Entities = [contact_vertex]

# Add the fourth contact region to the connection group
contact_region_4 = connection_group.AddContactRegion()
# Set the target location to the contact vertex and the source location to the Cont_face4
# named selection
set_contact_region_properties(
    contact_region_4, contact_vertex_4, "Cont_face4", set_target_before_src=True
)

# %%
# Fully define the modal multiphysics region with two physics regions

# Get the modal acoustic analysis object
modal_acst = DataModel.Project.Model.Analyses[0]
# Get the acoustic region from the modal acoustic analysis
acoustic_region = modal_acst.Children[2]
# Set the acoustic region to the acoustic bodies named selection
acoustic_region.Location = acst_bodies

# Add a physics region to the modal acoustic analysis
structural_region = modal_acst.AddPhysicsRegion()
# Set the physics region to structural and rename it based on the definition
structural_region.Structural = True
structural_region.RenameBasedOnDefinition()
# Set the structural region to the structural bodies named selection
structural_region.Location = get_named_selection("Structural_bodies")

# %%
# Set up the analysis settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Get the analysis settings from the modal acoustic analysis
analysis_settings = modal_acst.Children[1]
# Set the analysis settings properties
analysis_settings.MaximumModesToFind = 12
analysis_settings.SearchRangeMinimum = Quantity("0.1 [Hz]")
analysis_settings.SolverType = SolverType.Unsymmetric
analysis_settings.GeneralMiscellaneous = True
analysis_settings.CalculateReactions = True

# %%
# Set the boundary conditions and load
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add an acoustic free surface to the modal acoustic analysis
free_surface = modal_acst.AddAcousticFreeSurface()
# Set the free surface location to the free faces named selection
free_surface.Location = get_named_selection("Free_faces")

# %%
# Add the solid fluid interface

# Add a fluid solid interface to the modal acoustic analysis
fsi_object = modal_acst.AddFluidSolidInterface()
# Set the fluid solid interface location to the FSI faces named selection
fsi_object.Location = get_named_selection("FSI_faces")

# %%
# Add the gravity load

# Add gravity to the modal acoustic analysis
acceleration = modal_acst.AddAcceleration()
# Set the components and the Y-component of the acceleration to
# 9.81 m/s^2 (gravitational acceleration)
acceleration.DefineBy = LoadDefineBy.Components
acceleration.YComponent.Output.DiscreteValues = [Quantity("9.81 [m sec^-1 sec^-1]")]

# %%
# Add fixed support

# Get vertices from the geometry
vertices = []
for body in range(0, 4):
    vertices.append(DataModel.GeoData.Assemblies[0].Parts[1].Bodies[body].Vertices[0])

# Create a selection info object for the geometry entities
fvert = sel_manager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
# Set the list of vertices as the geometry entities
fvert.Entities = vertices

# Add a fixed support to the modal acoustic analysis
fixed_support = modal_acst.AddFixedSupport()
# Set the location of the fixed support to the geometry entities
fixed_support.Location = fvert

# Activate the modal acoustic analysis and display boundary conditions
modal_acst.Activate()
image_path = output_path / "geometry.png"
camera.SetFit()
app.helpers.export_image(modal_acst, image_path)
app.helpers.display_image(image_path)

# %%
# Add results to the solution
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Get the solution object from the modal acoustic analysis
solution = model.Analyses[0].Solution

# Add 10 total deformation results, setting the mode for every result except the first
total_deformation_results = []
for mode in range(1, 11):
    total_deformation = solution.AddTotalDeformation()
    if mode > 1:
        total_deformation.Mode = mode
    total_deformation_results.append(total_deformation)

# %%
# Add the acoustic pressure result to the solution

acoustic_pressure_result = solution.AddAcousticPressureResult()

# %%
# Scope the force reaction to the fixed support

# Add a force reaction to the solution
force_reaction_1 = solution.AddForceReaction()
# Set the boundary condition selection to the fixed support
force_reaction_1.BoundaryConditionSelection = fixed_support

# %%
# Solve the solution
# ~~~~~~~~~~~~~~~~~~

solution.Solve(True)

# sphinx_gallery_start_ignore
assert solution.Status == SolutionStatusType.Done, "Solution status is not 'Done'"
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
# Activate the first total deformation result and display the image

app.Tree.Activate([total_deformation_results[0]])
image_path = output_path / "total_deformation.png"
camera.SetFit()
app.helpers.export_image(total_deformation_results[0], image_path)
app.helpers.display_image(image_path)

# %%
# Activate the acoustic pressure result and display the image

image_path = output_path / "acoustic_pressure.png"
camera.SetFit()
app.helpers.export_image(acoustic_pressure_result, image_path)
app.helpers.display_image(image_path)
# %%
# Display all modal frequency, force reaction, and acoustic pressure values

print("Modal Acoustic Results")
print("----------------------")

# Print the frequency values for each mode
for index, result in enumerate(total_deformation_results, start=1):
    frequency_value = result.ReportedFrequency.Value
    print(f"Frequency for mode {index}: ", frequency_value)

# Get the maximum and minimum values of the acoustic pressure result
pressure_result_max = acoustic_pressure_result.Maximum.Value
pressure_result_min = acoustic_pressure_result.Minimum.Value

# Get the force reaction values for the x and z axes
force_reaction_1_x = force_reaction_1.XAxis.Value
force_reaction_1_z = force_reaction_1.ZAxis.Value

# Print the results
print("Acoustic pressure minimum : ", pressure_result_min)
print("Acoustic pressure Maximum : ", pressure_result_max)
print("Force reaction x-axis : ", force_reaction_1_x)
print("Force reaction z-axis : ", force_reaction_1_z)

# %%
# Display the total deformation animation
deformation_gif = output_path / "total_deformation_results.gif"
camera.SetFit()
app.helpers.export_animation(total_deformation_results[-1], deformation_gif)


# %%
# Display the total deformation animation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Open the GIF file and create an animation
gif = Image.open(deformation_gif)
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
ani = FuncAnimation(fig, update_frame, frames=gif.n_frames, interval=200, blit=True, repeat=True)

# Show the animation
plt.show()

# %%
# Print the project tree
# ~~~~~~~~~~~~~~~~~~~~~~

app.print_tree()

# %%
# Clean up the project
# ~~~~~~~~~~~~~~~~~~~~

# Save the project file
mechdat_file = output_path / "modal_acoustics.mechdat"
app.save_as(str(mechdat_file), overwrite=True)

# Close the app
app.close()

# Delete the example files
delete_downloads()
