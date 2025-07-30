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

""".. _ref_non_linear_analysis_rubber_boot_seal:

Nonlinear Analysis of a Rubber Boot Seal Model
----------------------------------------------

This example demonstrates a nonlinear 3D analysis of a rubber boot seal to:

- Create a rigid-flexible contact pair between a rigid shaft and a
  rubber boot part.
- Specify ramped effects using the On Gauss Point Detection Method
  to update contact stiffness at each iteration.
- Specify contact pairs at the inner and outer surfaces of the rubber boot.
- Specify non-ramped effects using the Nodal-Projected Normal From Contact
  Detection Method to update contact stiffness at each iteration.
"""

# %%
# Import the necessary libraries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from pathlib import Path
from typing import TYPE_CHECKING

from PIL import Image
from matplotlib import image as mpimg
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

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
    graphics_image_export_settings : Ansys.Mechanical.Graphics.GraphicsImageExportSettings
        The settings for exporting the image.
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
# Configure graphics for image export
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

graphics = app.Graphics
camera = graphics.Camera

# Set the camera orientation to the isometric view
camera.SetSpecificViewOrientation(Ansys.Mechanical.DataModel.Enums.ViewOrientationType.Iso)
camera.SetFit()

# Set the image export format and settings
image_export_format = GraphicsImageExportFormat.PNG
settings_720p = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
settings_720p.Resolution = GraphicsResolutionType.EnhancedResolution
settings_720p.Background = GraphicsBackgroundType.White
settings_720p.Width = 1280
settings_720p.Height = 720
settings_720p.CurrentGraphicsDisplay = False

# %%
# Download the geometry and material files
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

geometry_path = download_file("example_05_td26_Rubber_Boot_Seal.agdb", "pymechanical", "00_basic")
mat_path = download_file("example_05_Boot_Mat.xml", "pymechanical", "00_basic")

# %%
# Import the geometry and material
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Import the material

model = app.Model
materials = model.Materials
materials.Import(mat_path)

# %%
# Import the geometry

# Add a geometry import to the geometry import group for the model
geometry_import = model.GeometryImportGroup.AddGeometryImport()

# Set the geometry import format and preferences
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessNamedSelections = True
geometry_import_preferences.ProcessCoordinateSystems = True

# Import the geometry with the specified format and preferences
geometry_import.Import(geometry_path, geometry_import_format, geometry_import_preferences)

# Visualize the imported geometry in 3D
app.plot()

# %%
# Set up the analysis
# ~~~~~~~~~~~~~~~~~~~

# Set the active unit system and angle unit
app.ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMM
app.ExtAPI.Application.ActiveAngleUnit = AngleUnitType.Radian

# %%
# Store all main tree nodes as variables

# Define the geometry for the model
geometry = model.Geometry
# Get the part and solid objects from the geometry
part1 = app.DataModel.GetObjectsByName("Part")[0]
part2 = app.DataModel.GetObjectsByName("Solid")[1]

# Define the coordinate systems
coordinate_systems = model.CoordinateSystems
geometry_coordinate_systems = coordinate_systems.Children[0]

# %%
# Add a static structural analysis

# Add a static structural analysis to the model
model.AddStaticStructuralAnalysis()

# Get the static structural analysis from the model
static_structural_analysis = model.Analyses[0]

# Get the analysis settings, solution, and solution information
analysis_settings = static_structural_analysis.Children[0]
stat_struct_soln = static_structural_analysis.Solution
soln_info = stat_struct_soln.SolutionInformation

# %%
# Create a function to get named selections


def get_named_selection(
    named_selections, name: str
) -> Ansys.ACT.Automation.Mechanical.NamedSelection:
    """Get a named selection by its name.

    Parameters
    ----------
    named_selections : Ansys.ACT.Automation.Mechanical.NamedSelections
        The named selections object to search in.
    name : str
        The name of the named selection to retrieve.

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
# Define named selections and coordinate systems

named_selections = app.ExtAPI.DataModel.Project.Model.NamedSelections
top_face = get_named_selection(named_selections, "Top_Face")
bottom_face = get_named_selection(named_selections, "Bottom_Face")
symm_faces30 = get_named_selection(named_selections, "Symm_Faces30")
faces2 = get_named_selection(named_selections, "Faces2")
cyl_faces2 = get_named_selection(named_selections, "Cyl_Faces2")
rubber_bodies30 = get_named_selection(named_selections, "Rubber_Bodies30")
inner_faces30 = get_named_selection(named_selections, "Inner_Faces30")
outer_faces30 = get_named_selection(named_selections, "Outer_Faces30")
shaft_face = get_named_selection(named_selections, "Shaft_Face")
symm_faces15 = get_named_selection(named_selections, "Symm_Faces15")

# Add a coordinate system and set its origin y-coordinate
lcs1 = coordinate_systems.AddCoordinateSystem()
lcs1.OriginY = Quantity("97[mm]")

# %%
# Assign material

# Set the material for the rubber boot part
part1.Material = "Boot"
# Set the stiffness behavior for the rubber boot part
part2.StiffnessBehavior = StiffnessBehavior.Rigid

# %%
# Create a function to add a contact region and set its properties


def add_contact_region_and_props(
    body,
    target_location,
    src_location,
    set_src_first: bool = True,
    contact_type=ContactType.Frictional,
    friction_coefficient=0.2,
    behavior=ContactBehavior.Asymmetric,
    small_sliding=ContactSmallSlidingType.Off,
    detection_method=ContactDetectionPoint.OnGaussPoint,
    update_stiffness=UpdateContactStiffness.EachIteration,
):
    """Add a contact region and set its properties.

    Parameters
    ----------
    body : Ansys.ACT.Automation.Mechanical.Body
        The body to which the contact region is added.
    target_location : Ansys.ACT.Automation.Mechanical.NamedSelection
        The target location for the contact region.
    src_location : Ansys.ACT.Automation.Mechanical.NamedSelection
        The source location for the contact region.
    set_src_first : bool
        Whether to set the source location first.
    contact_type : ContactType
        The type of contact (default is Frictional).
    friction_coefficient : float
        The friction coefficient for the contact region (default is 0.2).
    behavior : ContactBehavior
        The behavior of the contact region (default is Asymmetric).
    small_sliding : ContactSmallSlidingType
        The small sliding type for the contact region (default is Off).
    detection_method : ContactDetectionPoint
        The detection method for the contact region (default is OnGaussPoint).
    update_stiffness : UpdateContactStiffness
        The update stiffness method for the contact region (default is EachIteration).

    Returns
    -------
    Ansys.ACT.Automation.Mechanical.ContactRegion
        The created contact region.
    """
    # Add a contact region to the connection or child connection
    contact_region = body.AddContactRegion()
    # Set the source and target locations for the contact region
    if set_src_first:
        contact_region.SourceLocation = src_location
        contact_region.TargetLocation = target_location
    else:
        contact_region.TargetLocation = target_location
        contact_region.SourceLocation = src_location
    # Set the contact type, friction coefficient, behavior, small sliding,
    # detection method, and update stiffness for the contact region
    contact_region.ContactType = contact_type
    contact_region.FrictionCoefficient = friction_coefficient
    contact_region.Behavior = behavior
    contact_region.SmallSliding = small_sliding
    contact_region.DetectionMethod = detection_method
    contact_region.UpdateStiffness = update_stiffness

    return contact_region


# %%
# Add contact regions

# Add a contact region to the connections
connections = model.Connections
contact_region1 = add_contact_region_and_props(
    connections,
    target_location=shaft_face,
    src_location=inner_faces30,
    set_src_first=False,
)
# Set interface treatment and target properties
contact_region1.InterfaceTreatment = ContactInitialEffect.AddOffsetRampedEffects
contact_region1.TargetGeometryCorrection = TargetCorrection.Smoothing
contact_region1.TargetOrientation = TargetOrientation.Cylinder
contact_region1.TargetStartingPoint = geometry_coordinate_systems
contact_region1.TargetEndingPoint = lcs1

# Add a contact region to the child connections
conts = connections.Children[0]
contact_region2 = add_contact_region_and_props(
    conts,
    target_location=inner_faces30,
    src_location=inner_faces30,
    detection_method=ContactDetectionPoint.NodalProjectedNormalFromContact,
)
# Set the stiffness value type and factor
contact_region2.NormalStiffnessValueType = ElementControlsNormalStiffnessType.Factor
contact_region2.NormalStiffnessFactor = 1

# Add a contact region to the child connections
contact_region3 = add_contact_region_and_props(
    conts,
    target_location=outer_faces30,
    src_location=outer_faces30,
    detection_method=ContactDetectionPoint.NodalProjectedNormalFromContact,
)
# Set the stiffness value type and factor
contact_region3.NormalStiffnessValueType = ElementControlsNormalStiffnessType.Factor
contact_region3.NormalStiffnessFactor = 1

# %%
# Add face meshing and sizing
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define the mesh for the model
mesh = model.Mesh

# Add face meshing to the mesh
face_mesh = mesh.AddFaceMeshing()
# Set the location of the face mesh to the shaft face
# and set the internal number of divisions to 1
face_mesh.Location = shaft_face
face_mesh.InternalNumberOfDivisions = 1

# Add sizing to the mesh
mesh_size = mesh.AddSizing()
# Set the location of the mesh size to the symmetry faces
# and set the element size to 2 mm
mesh_size.Location = symm_faces15
mesh_size.ElementSize = Quantity("2 [mm]")
mesh.ElementOrder = ElementOrder.Linear
mesh.Resolution = 2

# Generate the mesh and display the image
mesh.GenerateMesh()
set_camera_and_display_image(camera, graphics, settings_720p, output_path, "mesh.png")

# %%
# Add remote points
# ~~~~~~~~~~~~~~~~~


def add_remote_point(
    model,
    location,
    behavior=LoadBehavior.Rigid,
):
    """Add a remote point to the model.

    Parameters
    ----------
    model : Ansys.ACT.Automation.Mechanical.Model
        The model to which the remote point is added.
    location : Ansys.ACT.Automation.Mechanical.NamedSelection
        The location of the remote point.
    behavior : LoadBehavior
        The behavior of the remote point (default is Rigid).

    Returns
    -------
    Ansys.ACT.Automation.Mechanical.RemotePoint
        The created remote point.
    """
    remote_point = model.AddRemotePoint()
    remote_point.Location = location
    remote_point.Behavior = behavior

    return remote_point


remote_point01 = add_remote_point(model, bottom_face)
remote_point02 = add_remote_point(model, top_face)

# %%
# Configure the analysis settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Define a function to set the analysis settings


def set_analysis_settings(
    analysis_settings,
    current_step_number: int,
    initial_substeps: int,
    minimum_substeps: int,
    store_results_at_value: int,
    automatic_time_stepping: bool = AutomaticTimeStepping.On,
    define_by: TimeStepDefineByType = TimeStepDefineByType.Substeps,
    maximum_substeps: int = 1000,
    store_results_at: TimePointsOptions = TimePointsOptions.EquallySpacedPoints,
):
    analysis_settings.CurrentStepNumber = current_step_number
    analysis_settings.AutomaticTimeStepping = automatic_time_stepping
    analysis_settings.DefineBy = define_by
    analysis_settings.InitialSubsteps = initial_substeps
    analysis_settings.MinimumSubsteps = minimum_substeps
    analysis_settings.MaximumSubsteps = maximum_substeps
    analysis_settings.StoreResultsAt = store_results_at
    analysis_settings.StoreResulsAtValue = store_results_at_value


# %%
# Configure the analysis settings

analysis_settings.Activate()
analysis_settings.LargeDeflection = True
analysis_settings.Stabilization = StabilizationType.Off
analysis_settings.NumberOfSteps = 2

set_analysis_settings(
    analysis_settings,
    current_step_number=1,
    initial_substeps=5,
    minimum_substeps=5,
    store_results_at_value=5,
)

set_analysis_settings(
    analysis_settings,
    current_step_number=2,
    initial_substeps=10,
    minimum_substeps=10,
    store_results_at_value=10,
)

set_analysis_settings(
    analysis_settings,
    current_step_number=3,
    initial_substeps=30,
    minimum_substeps=30,
    store_results_at_value=20,
)

soln_info.NewtonRaphsonResiduals = 4

# %%
# Set load and boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

remote_displacement = static_structural_analysis.AddRemoteDisplacement()
remote_displacement.Location = remote_point01

# %%
# Define a function to convert a list of values to quantities


def convert_to_quantity(quantity_list: tuple) -> list:
    """Convert a list of values to quantities.

    Parameters
    ----------
    quantity_list : tuple
        A tuple containing a list of values and the unit.

    Returns
    -------
    list
        A list of quantities with the specified unit.
    """
    values, unit = quantity_list
    return [Quantity(f"{value} [{unit}]") for value in values]


# %%
# Set the input values for all remote displacement components

input_values = convert_to_quantity(([0, 1, 2, 3], "s"))

# %%
# Set the X component input and output values

x_component = remote_displacement.XComponent
x_component.Inputs[0].DiscreteValues = input_values
x_component.Output.DiscreteValues = convert_to_quantity(([0, 0, 0, 0], "mm"))

# %%
# Set the Y component input and output values

y_component = remote_displacement.YComponent
y_component.Inputs[0].DiscreteValues = input_values
y_component.Output.DiscreteValues = convert_to_quantity(([0, 0, -10, -10], "mm"))

# %%
# Set the Z component input and output values

z_component = remote_displacement.ZComponent
z_component.Inputs[0].DiscreteValues = input_values
z_component.Output.DiscreteValues = convert_to_quantity(([0, 0, 0, 0], "mm"))

# %%
# Set the rotation X component input and output values

rotation_x = remote_displacement.RotationX
rotation_x.Inputs[0].DiscreteValues = input_values
rotation_x.Output.DiscreteValues = convert_to_quantity(([0, 0, 0, 0], "rad"))

# %%
# Set the rotation X component input and output values

rotation_y = remote_displacement.RotationY
rotation_y.Inputs[0].DiscreteValues = input_values
rotation_y.Output.DiscreteValues = convert_to_quantity(([0, 0, 0, 0], "rad"))

# %%
# Set the rotation Z component input and output values

rotation_z = remote_displacement.RotationZ
rotation_z.Inputs[0].DiscreteValues = input_values
rotation_z.Output.DiscreteValues = convert_to_quantity(([0, 0, 0, 0.55], "rad"))

# %%
# Add frictionless support to the static structural analysis


def add_frictionless_support(
    static_structural_analysis,
    location,
    name: str,
):
    """Add frictionless support to the static structural analysis.

    Parameters
    ----------
    static_structural_analysis : Ansys.ACT.Automation.Mechanical.StaticStructuralAnalysis
        The static structural analysis object.
    location : Ansys.ACT.Automation.Mechanical.NamedSelection
        The location of the frictionless support.
    name : str
        The name of the frictionless support.

    Returns
    -------
    Ansys.ACT.Automation.Mechanical.FrictionlessSupport
        The created frictionless support.
    """
    frictionless_support = static_structural_analysis.AddFrictionlessSupport()
    frictionless_support.Location = location
    frictionless_support.Name = name

    return frictionless_support


add_frictionless_support(static_structural_analysis, symm_faces30, "Symmetry_BC")
add_frictionless_support(static_structural_analysis, faces2, "Boot_Bottom_BC")
add_frictionless_support(static_structural_analysis, cyl_faces2, "Boot_Radial_BC")

# %%
# Add results
# ~~~~~~~~~~~

# Add total deformation results to the solution
total_deformation = static_structural_analysis.Solution.AddTotalDeformation()
total_deformation.Location = rubber_bodies30

# Add equivalent stress results to the solution
equivalent_stress = static_structural_analysis.Solution.AddEquivalentStress()
equivalent_stress.Location = rubber_bodies30

# %%
# Solve the static structural analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

static_structural_analysis.Solution.Solve(True)

# sphinx_gallery_start_ignore
assert stat_struct_soln.Status == SolutionStatusType.Done, "Solution status is not 'Done'"
# sphinx_gallery_end_ignore

# %%
# Postprocessing
# ~~~~~~~~~~~~~~

# Activate the total deformation result and display the image
app.Tree.Activate([total_deformation])
set_camera_and_display_image(camera, graphics, settings_720p, output_path, "total_deformation.png")

# %%
# Equivalent stress

# Activate the equivalent stress result and display the image
app.Tree.Activate([equivalent_stress])
set_camera_and_display_image(camera, graphics, settings_720p, output_path, "equivalent_stress.png")

# %%
# Create a function to set the animation for the GIF


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
# Show the total deformation animation

# Set the animation export format and settings
animation_export_format = Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat.GIF
settings_720p = Ansys.Mechanical.Graphics.AnimationExportSettings()
settings_720p.Width = 1280
settings_720p.Height = 720

# Export the total deformation animation as a GIF
total_deformation_gif = output_path / "total_deformation.gif"
total_deformation.ExportAnimation(
    str(total_deformation_gif), animation_export_format, settings_720p
)

# Open the GIF file and create an animation
gif = Image.open(total_deformation_gif)
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
    interval=200,
    repeat=True,
    blit=True,
)

# Show the animation
plt.show()

# %%
# Clean up the project
# ~~~~~~~~~~~~~~~~~~~~

# Save the mechdat file
mechdat_file = output_path / "non_linear_rubber_boot_seal.mechdat"
app.save(str(mechdat_file))

# Close the app
app.close()

# Delete the example files
delete_downloads()
