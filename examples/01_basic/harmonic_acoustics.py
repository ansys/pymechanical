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

""".. _ref_harmonic_acoustics:

Harmonic acoustic analysis
--------------------------

This example examines a harmonic acoustic analysis that uses
surface velocity to determine the steady-state response of a
structure and the surrounding fluid medium to loads and excitations
that vary sinusoidally with time.
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
    set_fit: bool = False,
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
    if set_fit:
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

# Set the camera orientation to isometric view
camera.SetSpecificViewOrientation(ViewOrientationType.Iso)

# Set the image export format to PNG and configure the export settings
image_export_format = GraphicsImageExportFormat.PNG
settings_720p = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
settings_720p.Resolution = GraphicsResolutionType.EnhancedResolution
settings_720p.Background = GraphicsBackgroundType.White
settings_720p.Width = 1280
settings_720p.Height = 720
settings_720p.CurrentGraphicsDisplay = False
camera.Rotate(180, CameraAxisType.ScreenY)

# %%
# Download geometry and materials files
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Download the geometry file from the ansys/example-data repository
geometry_path = download_file("C_GEOMETRY.agdb", "pymechanical", "embedding")
# Download the material file from the ansys/example-data repository
mat_path = download_file("Air-material.xml", "pymechanical", "embedding")

# %%
# Import the geometry
# ~~~~~~~~~~~~~~~~~~~

# Define the model
model = app.Model

# Add the geometry import group and set its preferences
geometry_import = model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessNamedSelections = True

# Import the geometry file with the specified format and preferences
geometry_import.Import(geometry_path, geometry_import_format, geometry_import_preferences)

# Define the geometry in the model
geometry = model.Geometry

# Suppress the bodies at the specified geometry.Children indices
suppressed_indices = [0, 1, 2, 3, 4, 6, 9, 10]
for index, child in enumerate(geometry.Children):
    if index in suppressed_indices:
        child.Suppressed = True

# Visualize the model in 3D
app.plot()

# %%
# Store all variables necessary for analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

mesh = model.Mesh
named_selection = model.NamedSelections
connection = model.Connections
coordinate_systems = model.CoordinateSystems
mat = model.Materials

# %%
# Set up the analysis
# ~~~~~~~~~~~~~~~~~~~

# Add the harmonic acoustics analysis and unit system
model.AddHarmonicAcousticAnalysis()
app.ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardMKS

# %%
# Import and assign the materials

mat.Import(mat_path)

# Assign the material to the ``geometry.Children`` bodies that are not suppressed
for child in range(geometry.Children.Count):
    if child not in suppressed_indices:
        geometry.Children[child].Material = "Air"

# %%
# Create a coordinate system

lcs1 = coordinate_systems.AddCoordinateSystem()
lcs1.OriginX = Quantity("0 [mm]")
lcs1.OriginY = Quantity("0 [mm]")
lcs1.OriginZ = Quantity("0 [mm]")
lcs1.PrimaryAxisDefineBy = CoordinateSystemAlignmentType.GlobalZ

# %%
# Generate the mesh

mesh.ElementSize = Quantity("200 [mm]")
mesh.GenerateMesh()

# %%
# Create named selections
# ~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Create a function to set up named selections


def setup_named_selection(scoping_method, name):
    """Create a named selection with the specified scoping method and name.

    Parameters
    ----------
    scoping_method : GeometryDefineByType
        The scoping method for the named selection.
    name : str
        The name of the named selection.

    Returns
    -------
    Ansys.ACT.Automation.Mechanical.NamedSelection
        The created named selection.
    """
    ns = model.AddNamedSelection()
    ns.ScopingMethod = scoping_method
    ns.Name = name
    return ns


# %%
# Create a function to add generation criteria to the named selection


def add_generation_criteria(
    named_selection,
    value,
    active=True,
    action=SelectionActionType.Add,
    entity_type=SelectionType.GeoFace,
    criterion=SelectionCriterionType.Size,
    operator=SelectionOperatorType.Equal,
):
    """Add generation criteria to the named selection.

    Parameters
    ----------
    named_selection : Ansys.ACT.Automation.Mechanical.NamedSelection
        The named selection to which the criteria will be added.
    value : Quantity
        The value for the criteria.
    active : bool
        Whether the criteria is active.
    action : SelectionActionType
        The action type for the criteria.
    entity_type : SelectionType
        The entity type for the criteria.
    criterion : SelectionCriterionType
        The criterion type for the criteria.
    operator : SelectionOperatorType
        The operator for the criteria.
    """
    generation_criteria = named_selection.GenerationCriteria
    criteria = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
    criteria.Active = active
    criteria.Action = action
    criteria.EntityType = entity_type
    criteria.Criterion = criterion
    criteria.Operator = operator
    criteria.Value = value
    generation_criteria.Add(criteria)


# %%
# Add a named selection for the surface velocity and define its generation criteria

sf_velo = setup_named_selection(GeometryDefineByType.Worksheet, "sf_velo")
add_generation_criteria(sf_velo, Quantity("3e6 [mm^2]"))
add_generation_criteria(
    sf_velo,
    Quantity("15000 [mm]"),
    action=SelectionActionType.Filter,
    criterion=SelectionCriterionType.LocationZ,
)
# Activate and generate the named selection
sf_velo.Activate()
sf_velo.Generate()

# %%
# Add named selections for the absorption faces and define its generation criteria

abs_face = setup_named_selection(GeometryDefineByType.Worksheet, "abs_face")
add_generation_criteria(abs_face, Quantity("1.5e6 [mm^2]"))
add_generation_criteria(
    abs_face,
    Quantity("500 [mm]"),
    action=SelectionActionType.Filter,
    criterion=SelectionCriterionType.LocationY,
)
# Activate and generate the named selection
abs_face.Activate()
abs_face.Generate()

# %%
# Add named selections for the pressure faces and define its generation criteria

pres_face = setup_named_selection(GeometryDefineByType.Worksheet, "pres_face")
add_generation_criteria(pres_face, Quantity("1.5e6 [mm^2]"))
add_generation_criteria(
    pres_face,
    Quantity("4500 [mm]"),
    action=SelectionActionType.Filter,
    criterion=SelectionCriterionType.LocationY,
)
# Activate and generate the named selection
pres_face.Activate()
pres_face.Generate()

# %%
# Add named selections for the acoustic region and define its generation criteria

acoustic_region = setup_named_selection(GeometryDefineByType.Worksheet, "acoustic_region")
add_generation_criteria(
    acoustic_region,
    8,
    entity_type=SelectionType.GeoBody,
    criterion=SelectionCriterionType.Type,
)
# Activate and generate the named selection
acoustic_region.Activate()
acoustic_region.Generate()

# %%
# Set up the analysis settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

analysis_settings = model.Analyses[0].AnalysisSettings
analysis_settings.RangeMaximum = Quantity("100 [Hz]")
analysis_settings.SolutionIntervals = 50
analysis_settings.CalculateVelocity = True
analysis_settings.CalculateEnergy = True
analysis_settings.CalculateVolumeEnergy = True

# %%
# Set the boundary conditions and load
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Get the harmonic acoustics analysis
harmonic_acoustics = model.Analyses[0]

# %%
# Set the location for the acoustics region from the harmonic acoustics analysis

acoustics_region = [
    child for child in harmonic_acoustics.Children if child.Name == "Acoustics Region"
][0]
acoustics_region.Location = acoustic_region

# %%
# Add a surface velocity boundary condition to the harmonic acoustics analysis

surface_velocity = harmonic_acoustics.AddAcousticSurfaceVelocity()
surface_velocity.Location = sf_velo
surface_velocity.Magnitude.Output.DiscreteValues = [Quantity("5000 [mm s-1]")]

# %%
# Add an acoustic pressure boundary condition to the harmonic acoustics analysis

acoustic_pressure = harmonic_acoustics.AddAcousticPressure()
acoustic_pressure.Location = pres_face
acoustic_pressure.Magnitude = Quantity("1.5e-7 [MPa]")

# %%
# Add an acoustic absorption surface to the harmonic acoustics analysis

absorption_surface = harmonic_acoustics.AddAcousticAbsorptionSurface()
absorption_surface.Location = abs_face
absorption_surface.AbsorptionCoefficient.Output.DiscreteValues = [Quantity("0.02")]

# Activate the harmonic acoustics analysis
harmonic_acoustics.Activate()
# Set the camera to fit the mesh and export the image
set_camera_and_display_image(
    camera, graphics, settings_720p, output_path, "bounday_conditions.png", set_fit=True
)

# %%
# Add results to the harmonic acoustics solution
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Get the harmonic acoustics solution
solution = model.Analyses[0].Solution

# %%
# Add the acoustic pressure result

acoustic_pressure_result_1 = solution.AddAcousticPressureResult()
acoustic_pressure_result_1.By = SetDriverStyle.ResultSet
acoustic_pressure_result_1.SetNumber = 25

# %%
# Add the acoustic total and directional velocity results

# Add the acoustic total velocity result and set its frequency
acoustic_total_velocity_1 = solution.AddAcousticTotalVelocityResult()
acoustic_total_velocity_1.Frequency = Quantity("50 [Hz]")

# Add the acoustic directional velocity result and set its frequency and coordinate system
acoustic_directional_velocity_1 = solution.AddAcousticDirectionalVelocityResult()
acoustic_directional_velocity_1.Frequency = Quantity("50 [Hz]")
acoustic_directional_velocity_1.CoordinateSystem = lcs1

# Add the acoustic total velocity result and set its orientation
acoustic_directional_velocity_2 = solution.AddAcousticDirectionalVelocityResult()
acoustic_directional_velocity_2.NormalOrientation = NormalOrientationType.ZAxis
acoustic_directional_velocity_2.By = SetDriverStyle.ResultSet
acoustic_directional_velocity_2.SetNumber = 25

# %%
# Add the acoustic sound pressure levels and frequency band responses

# Add the acoustic sound pressure level and set its frequency
acoustic_spl = solution.AddAcousticSoundPressureLevel()
acoustic_spl.Frequency = Quantity("50 [Hz]")

# Add the acoustic A-weighted sound pressure level and set its frequency
acoustic_a_spl = solution.AddAcousticAWeightedSoundPressureLevel()
acoustic_a_spl.Frequency = Quantity("50 [Hz]")

# Add the acoustic frequency band sound pressure level
acoustic_frq_band_spl = solution.AddAcousticFrequencyBandSPL()

# Add the acoustic A-weighted frequency band sound pressure level
a_freq_band_spl = solution.AddAcousticFrequencyBandAWeightedSPL()

# Add the acoustic velocity frequency response and set its orientation and location
z_velocity_response = solution.AddAcousticVelocityFrequencyResponse()
z_velocity_response.NormalOrientation = NormalOrientationType.ZAxis
# Set the location to the pressure face named selection
z_velocity_response.Location = pres_face

# %%
# Add the acoustic kinetic and potentional energy frequency responses

# Add the acoustic kinetic energy frequency response and set its location
# to the absorption face named selection
ke_response = solution.AddAcousticKineticEnergyFrequencyResponse()
ke_response.Location = abs_face
ke_display = ke_response.TimeHistoryDisplay

# Add the acoustic potential energy frequency response and set its location
# to the absorption face named selection
pe_response = solution.AddAcousticPotentialEnergyFrequencyResponse()
pe_response.Location = abs_face
pe_display = pe_response.TimeHistoryDisplay

# %%
# Create a function to set the properties of the acoustic velocity result


def set_properties(
    element,
    frequency,
    location,
    amplitude=True,
    normal_orientation=None,
):
    """Set the properties of the acoustic velocity result."""
    element.Frequency = frequency
    element.Amplitude = amplitude
    if normal_orientation:
        element.NormalOrientation = normal_orientation
    # Set the location to the specified named selection
    element.Location = location
    return element


# %%
# Add the acoustic total and directional velocity results

acoustic_total_velocity_2 = solution.AddAcousticTotalVelocityResult()
set_properties(acoustic_total_velocity_2, Quantity("30 [Hz]"), pres_face)

acoustic_directional_velocity_3 = solution.AddAcousticDirectionalVelocityResult()
set_properties(
    acoustic_directional_velocity_3,
    Quantity("10 [Hz]"),
    pres_face,
    normal_orientation=NormalOrientationType.ZAxis,
)

# %%
# Add the acoustic kinetic and potential energy results

acoustic_ke = solution.AddAcousticKineticEnergy()
set_properties(acoustic_ke, Quantity("68 [Hz]"), abs_face)

acoustic_pe = solution.AddAcousticPotentialEnergy()
set_properties(acoustic_pe, Quantity("10 [Hz]"), abs_face)

# %%
# Solve the harmonic acoustics analysis solution
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
# Postprocessing
# ~~~~~~~~~~~~~~

# %%
# Display the total acoustic pressure result

app.Tree.Activate([acoustic_pressure_result_1])
set_camera_and_display_image(camera, graphics, settings_720p, output_path, "pressure.png")

# %%
# Display the total acoustic velocity

app.Tree.Activate([acoustic_pressure_result_1])
set_camera_and_display_image(camera, graphics, settings_720p, output_path, "total_velocity.png")

# %%
# Display the acoustic sound pressure level

app.Tree.Activate([acoustic_spl])
set_camera_and_display_image(
    camera, graphics, settings_720p, output_path, "sound_pressure_level.png"
)

# %%
# Display the acoustic directional velocity

app.Tree.Activate([acoustic_directional_velocity_3])
set_camera_and_display_image(
    camera, graphics, settings_720p, output_path, "directional_velocity.png"
)

# %%
# Display the acoustic kinetic energy

app.Tree.Activate([acoustic_ke])
set_camera_and_display_image(camera, graphics, settings_720p, output_path, "kinetic_energy.png")

# %%
# Create a function to update the animation frames


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
# Display the total acoustic pressure animation

# Set the animation export format to GIF
animation_export_format = Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat.GIF

# Configure the export settings for the animation
settings_720p = Ansys.Mechanical.Graphics.AnimationExportSettings()
settings_720p.Width = 1280
settings_720p.Height = 720

# Export the animation of the acoustic pressure result
press_gif = output_path / "press.gif"
acoustic_pressure_result_1.ExportAnimation(str(press_gif), animation_export_format, settings_720p)

# Open the GIF file and create an animation
gif = Image.open(press_gif)
# Set the subplots for the animation and turn off the axis
figure, axes = plt.subplots(figsize=(16, 9))
axes.axis("off")
# Change the color of the image
image = axes.imshow(gif.convert("RGBA"))

# Create the animation using the figure, update_animation function, and the GIF frames
# Set the interval between frames to 200 milliseconds and repeat the animation
ani = FuncAnimation(
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
# Display the output file from the solve
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Get the working directory of the solve
solve_path = harmonic_acoustics.WorkingDir
solve_out_path = Path(solve_path) / "solve.out"

# Check if the solve output file exists and write its contents to the console
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
mechdat_file = output_path / "harmonic_acoustics.mechdat"
app.save(str(mechdat_file))

# Close the app
app.close()

# Delete the example file
delete_downloads()
