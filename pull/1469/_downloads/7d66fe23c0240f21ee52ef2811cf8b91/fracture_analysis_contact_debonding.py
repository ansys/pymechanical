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

""".. _ref_contact:

Fracture analysis - contact debonding
-------------------------------------

The following example demonstrates the use of the Contact Debonding
featuring in Mechanical using the Cohesive Zone Material (CZM) method.
This example displaces two two-dimensional parts on a
double cantilever beam.
"""

# %%
# Import the necessary libraries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from pathlib import Path
from typing import TYPE_CHECKING

from matplotlib import image as mpimg, pyplot as plt
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

# %%
# Configure camera and graphics for image export
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Set camera orientation
graphics = app.Graphics
camera = graphics.Camera
camera.SetSpecificViewOrientation(ViewOrientationType.Front)

# Set camera settings for 720p resolution
image_export_format = GraphicsImageExportFormat.PNG
graphics_image_export_settings = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
graphics_image_export_settings.Resolution = GraphicsResolutionType.EnhancedResolution
graphics_image_export_settings.Background = GraphicsBackgroundType.White
graphics_image_export_settings.CurrentGraphicsDisplay = False
graphics_image_export_settings.Width = 1280
graphics_image_export_settings.Height = 720

# %%
# Create functions to set camera and display images
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Set the path for the output files (images, gifs, mechdat)
output_path = Path.cwd() / "out"


def set_camera_and_display_image(
    camera,
    graphics,
    graphics_image_export_settings,
    image_output_path: Path,
    image_name: str,
) -> None:
    """Set the camera to fit the model and display the image.

    Parameters
    ----------
    camera : Ansys.ACT.Common.Graphics.MechanicalCameraWrapper
        The camera object to set the view.
    graphics : Ansys.ACT.Common.Graphics.MechanicalGraphicsWrapper
        The graphics object to export the image.
    image_output_path : Path
        The path to save the exported image.
    image_name : str
        The name of the exported image file.
    """
    # Set the camera to fit the mesh
    camera.SetFit()
    # Export the mesh image with the specified settings
    image_path = image_output_path / image_name
    graphics.ExportImage(str(image_path), image_export_format, graphics_image_export_settings)
    # Display the exported mesh image
    display_image(image_path)


def display_image(
    image_path: str,
    pyplot_figsize_coordinates: tuple = (16, 9),
    plot_xticks: list = [],
    plot_yticks: list = [],
    plot_axis: str = "off",
) -> None:
    """Display the image with the specified parameters.

    Parameters
    ----------
    image_path : str
        The path to the image file to display.
    pyplot_figsize_coordinates : tuple
        The size of the figure in inches (width, height).
    plot_xticks : list
        The x-ticks to display on the plot.
    plot_yticks : list
        The y-ticks to display on the plot.
    plot_axis : str
        The axis visibility setting ('on' or 'off').
    """
    # Set the figure size based on the coordinates specified
    plt.figure(figsize=pyplot_figsize_coordinates)
    # Read the image from the file into an array
    plt.imshow(mpimg.imread(image_path))
    # Get or set the current tick locations and labels of the x-axis
    plt.xticks(plot_xticks)
    # Get or set the current tick locations and labels of the y-axis
    plt.yticks(plot_yticks)
    # Turn off the axis
    plt.axis(plot_axis)
    # Display the figure
    plt.show()


# %%
# Download and import the geometry file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Set the model
model = app.Model
# Create a geometry import group for the model
geometry_import_group = model.GeometryImportGroup
# Add the geometry import to the group
geometry_import = geometry_import_group.AddGeometryImport()
# Set the geometry import format
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
# Set the geometry import preferences
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessNamedSelections = True
geometry_import_preferences.AnalysisType = (
    Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.AnalysisType.Type2D
)

# Download the geometry file from the ansys/example-data repository
geometry_path = download_file("Contact_Debonding_Example.agdb", "pymechanical", "embedding")

# Import/reload the geometry from the CAD (.agdb) file using the provided preferences
geometry_import.Import(geometry_path, geometry_import_format, geometry_import_preferences)

# Visualize the model in 3D
app.plot()

# %%
# Download and import the material files
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Download the material files from the ansys/example-data repository
mat1_path = download_file("Contact_Debonding_Example_Mat1.xml", "pymechanical", "embedding")
mat2_path = download_file("Contact_Debonding_Example_Mat2.xml", "pymechanical", "embedding")

# Add materials to the model and import the material files
model_materials = model.Materials
model_materials.Import(mat1_path)
model_materials.Import(mat2_path)

# %%
# Add connections to the model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add connections to the model
add_connections = model.AddConnections()
# Add a connection group to the connections
add_connections.AddConnectionGroup()

# Define and create automatic connections for the model
connections = model.Connections
connections.CreateAutomaticConnections()

# %%
# Add a static structural analysis to the model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add a static structural analysis to the model
model.AddStaticStructuralAnalysis()
static_structural_analysis = app.DataModel.AnalysisByName("Static Structural")
static_structural_analysis_solution = static_structural_analysis.Solution

# Set the unit system
app.ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMM

# %%
# Activate the geometry and set the 2D behavior
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define the geometry for the model
geometry = model.Geometry
# Activate the geometry
geometry.Activate()
# Set the 2D behavior for the geometry
geometry.Model2DBehavior = Model2DBehavior.PlaneStrain


# %%
# Create a function to get the child object by name
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_child_object(body, child_type, name: str):
    """Get the named selection child by name."""
    return [child for child in body.GetChildren[child_type](True) if child.Name == name][0]


# %%
# Activate the ``Part 2`` object and set its material
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Get the ``Part 2`` object from the tree
part2_object = app.DataModel.GetObjectsByName("Part 2")[0]

# Activate the ``Part 2`` object
part2_object.Activate()

# Set the material for the ``Part 2`` object
part2_object.Material = get_child_object(
    model_materials, Ansys.ACT.Automation.Mechanical.Material, "Interface Body Material"
).Name

# %%
# Define the contact and contact regions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Activate the contact region

# Get the contact from the connection group
contact = get_child_object(
    connections, Ansys.ACT.Automation.Mechanical.Connections.ConnectionGroup, "Contacts"
)

# Get the contact region from the contact
contact_region = get_child_object(
    contact, Ansys.ACT.Automation.Mechanical.Connections.ContactRegion, "Contact Region"
)
# Activate the contact region
contact_region.Activate()

# %%
# Set properties for the contact region

# Define the model named selections
named_selections = model.NamedSelections
# Set the source location to the high edge named selection
contact_region.SourceLocation = get_child_object(
    named_selections, Ansys.ACT.Automation.Mechanical.NamedSelection, "High_Edge"
)
# Set the target location to the low edge named selection`
contact_region.TargetLocation = get_child_object(
    named_selections, Ansys.ACT.Automation.Mechanical.NamedSelection, "Low_Edge"
)
# Set the contact type to bonded
contact_region.ContactType = ContactType.Bonded
# Set the contact formulation to pure penalty
contact_region.ContactFormulation = ContactFormulation.PurePenalty

# %%
# Generate the mesh
# ~~~~~~~~~~~~~~~~~

# Define the mesh for the model
mesh = model.Mesh

# Set the mesh element order to quadratic
mesh.ElementOrder = ElementOrder.Quadratic
# Turn off adaptive sizing
mesh.UseAdaptiveSizing = False
# Set the mesh element size to 0.75 mm
mesh.ElementSize = Quantity("0.75 [mm]")


# %%
# Create a function to add sizing to the mesh


def add_sizing(
    mesh: Ansys.ACT.Automation.Mechanical.MeshControls.Mesh,
    name: str,
    element_size: Ansys.Core.Units.Quantity,
    behavior: Ansys.Mechanical.DataModel.Enums.SizingBehavior,
) -> None:
    """Add sizing to the mesh and set its location, element size, and behavior.

    Parameters
    ----------
    mesh : Ansys.ACT.Automation.Mechanical.MeshControls.Mesh
        The mesh object to add sizing to.
    name : str
        The name of the named selection to use for sizing.
    element_size : Ansys.Core.Units.Quantity
        The element size to set for the sizing.
    behavior : Ansys.Mechanical.DataModel.Enums.SizingBehavior
        The behavior of the sizing (e.g., hard or soft).
    """
    sizing = mesh.AddSizing()
    sizing.Location = get_child_object(
        named_selections, Ansys.ACT.Automation.Mechanical.NamedSelection, name
    )
    sizing.ElementSize = element_size
    sizing.Behavior = behavior


# %%
# Add sizing to the mesh for the short and long edges
add_sizing(mesh, "Short_Edges", Quantity("0.75 [mm]"), SizingBehavior.Hard)
add_sizing(mesh, "Long_Edges", Quantity("0.5 [mm]"), SizingBehavior.Hard)

# %%
# Add sizing to the mesh for both faces
sizing_mesh_both_faces = mesh.AddFaceMeshing()
sizing_mesh_both_faces.Location = get_child_object(
    named_selections, Ansys.ACT.Automation.Mechanical.NamedSelection, "Both_Faces"
)
# Set the face meshing method to quadrilaterals
sizing_mesh_both_faces.Method = FaceMeshingMethod.Quadrilaterals

# Activate and generate the mesh
mesh.Activate()
mesh.GenerateMesh()

# Display the mesh image
set_camera_and_display_image(
    camera, graphics, graphics_image_export_settings, output_path, "mesh.png"
)

# %%
# Add a contact debonding object
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Activate the model
model.Activate()

# Add a fracture to the model
fracture = model.AddFracture()

# Add contact debonding to the fracture
contact_debonding = fracture.AddContactDebonding()
# Set the material for the contact debonding
contact_debonding.Material = get_child_object(
    model_materials, Ansys.ACT.Automation.Mechanical.Material, "CZM Crack Material"
).Name
# Set the contact region for the contact debonding
contact_debonding.ContactRegion = contact_region

# %%
# Define the static structural analysis settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define the static structural analysis settings
analysis_settings = static_structural_analysis.AnalysisSettings
# Activate the analysis settings
analysis_settings.Activate()
# Turn on automatic time stepping
analysis_settings.AutomaticTimeStepping = AutomaticTimeStepping.On
# Define the time step settings with substeps
analysis_settings.DefineBy = TimeStepDefineByType.Substeps
# Set the initial, minimum, and maximum time step sizes
analysis_settings.InitialSubsteps = 100
analysis_settings.MinimumSubsteps = 100
analysis_settings.MaximumSubsteps = 100
# Turn on large deflection
analysis_settings.LargeDeflection = True

# %%
# Define boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add fixed support to the static structural analysis
fixed_support = static_structural_analysis.AddFixedSupport()
# Set the fixed support location to the fixed edges named selection
fixed_support.Location = get_child_object(
    named_selections, Ansys.ACT.Automation.Mechanical.NamedSelection, "Fixed_Edges"
)

# %%
# Add displacements to the static structural analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Create a function to add displacement to the static structural analysis


def add_displacement(
    static_structural_analysis: Ansys.ACT.Automation.Mechanical.Analysis,
    named_selections: Ansys.ACT.Automation.Mechanical.NamedSelections,
    name: str,
    y_component_value: Ansys.Core.Units.Quantity,
) -> None:
    """Add a displacement to the static structural analysis.

    Parameters
    ----------
    static_structural_analysis : Ansys.ACT.Automation.Mechanical.Analysis
        The static structural analysis object.
    named_selections : Ansys.ACT.Automation.Mechanical.NamedSelections
        The named selections object.
    name : str
        The name of the named selection to use for displacement.
    y_component_value : str
        The value of the Y component for the displacement.
    """
    # Add a displacement to the static structural analysis
    displacement = static_structural_analysis.AddDisplacement()
    # Set the location for the displacement to the named selection with the given name
    displacement.Location = get_child_object(
        named_selections, Ansys.ACT.Automation.Mechanical.NamedSelection, name
    )
    # Set the displacement type to components
    displacement.DefineBy = LoadDefineBy.Components
    # Set the value of the Y component for the displacement
    displacement.YComponent.Output.DiscreteValues = [y_component_value]

    return displacement


# %%
# Add displacements to the static structural analysis

displacement1_vertex = add_displacement(
    static_structural_analysis, named_selections, "Disp1_Vertex", Quantity("10 [mm]")
)
displacement2_vertex = add_displacement(
    static_structural_analysis, named_selections, "Disp2_Vertex", Quantity("-10 [mm]")
)

# %%
# Set the camera to fit the model and display the image of the boundary conditions

static_structural_analysis.Activate()

set_camera_and_display_image(
    camera,
    graphics,
    graphics_image_export_settings,
    output_path,
    "boundary_conditions.png",
)

# %%
# Add results to the solution
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Activate the static structural analysis solution
static_structural_analysis_solution.Activate()

# %%
# Add directional deformation to the static structural analysis solution

directional_deformation = static_structural_analysis_solution.AddDirectionalDeformation()
# Set the orientation of the directional deformation to Y-axis
directional_deformation.NormalOrientation = NormalOrientationType.YAxis

# %%
# Add the force reaction to the static structural analysis solution
force_reaction = static_structural_analysis_solution.AddForceReaction()
# Set the boundary condition selection to the vertex named selection
force_reaction.BoundaryConditionSelection = displacement1_vertex

# %%
# Solve the solution
# ~~~~~~~~~~~~~~~~~~

static_structural_analysis_solution.Solve(True)

# sphinx_gallery_start_ignore
assert static_structural_analysis_solution.Status == SolutionStatusType.Done, (
    "Solution status is not 'Done'"
)
# sphinx_gallery_end_ignore

# %%
# Show messages
# ~~~~~~~~~~~~~

# Print all messages from Mechanical
app.messages.show()

# %%
# Activate the reactions and display the images
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Directional deformation

directional_deformation.Activate()
set_camera_and_display_image(
    camera,
    graphics,
    graphics_image_export_settings,
    output_path,
    "directional_deformation.png",
)

# %%
# Force reaction

force_reaction.Activate()
set_camera_and_display_image(
    camera, graphics, graphics_image_export_settings, output_path, "force_reaction.png"
)

# %%
# Export the animation
# ~~~~~~~~~~~~~~~~~~~~

# %%
# Create a function to update the animation frame


def update_animation(frame: int) -> list[mpimg.AxesImage]:
    """Update the animation frame for the GIF.

    Parameters
    ----------
    frame : int
        The frame number to update the animation.

    Returns
    -------
    list[mpimg.AxesImage]
        A list containing the updated image for the animation.
    """
    # Seeks to the given frame in this sequence file
    gif.seek(frame)
    # Set the image array to the current frame of the GIF
    image.set_data(gif.convert("RGBA"))
    # Return the updated image
    return [image]


# %%
# Display the animation of the force reaction

# Set the animation export format and settings
animation_export_format = GraphicsAnimationExportFormat.GIF
animation_export_settings = Ansys.Mechanical.Graphics.AnimationExportSettings()
animation_export_settings.Width = 1280
animation_export_settings.Height = 720

# Set the path for the contact status GIF
force_reaction_gif_path = output_path / "force_reaction.gif"

# Export the force reaction animation to a GIF file
force_reaction.ExportAnimation(
    str(force_reaction_gif_path), animation_export_format, animation_export_settings
)

# Open the GIF file and create an animation
gif = Image.open(force_reaction_gif_path)
# Set the subplots for the animation and turn off the axis
figure, axes = plt.subplots(figsize=(16, 9))
axes.axis("off")
# Change the color of the image
image = axes.imshow(gif.convert("RGBA"))

# Create the animation using the figure, update_animation function, and the GIF frames
# Set the interval between frames to 200 milliseconds and repeat the animation
FuncAnimation(
    figure,
    update_animation,
    frames=range(gif.n_frames),
    interval=100,
    repeat=True,
    blit=True,
)

# Show the animation
plt.show()

# %%
# Display the output file from the solve
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Get the working directory for the static structural analysis
solve_path = Path(static_structural_analysis.WorkingDir)
# Get the solve output path
solve_out_path = solve_path / "solve.out"

# Print the content of the solve output file if it exists
if solve_out_path:
    with solve_out_path.open("rt") as file:
        for line in file:
            print(line, end="")

# %%
# Print the project tree
# ~~~~~~~~~~~~~~~~~~~~~~

app.print_tree()

# %%
# Clean up the project
# ~~~~~~~~~~~~~~~~~~~~

# Save the project
mechdat_path = output_path / "contact_debonding.mechdat"
app.save(str(mechdat_path))

# Close the app
app.close()

# Delete the example files
delete_downloads()
