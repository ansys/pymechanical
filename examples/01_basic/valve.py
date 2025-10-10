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

""".. _ref_basic_valve:

Basic valve implementation
--------------------------

This example demonstrates a basic implementation of a valve in Python.
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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

graphics = app.Graphics
camera = graphics.Camera

# Set the camera orientation to the isometric view
camera.SetSpecificViewOrientation(ViewOrientationType.Iso)

# Set the image export format and settings
image_export_format = GraphicsImageExportFormat.PNG
settings_720p = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
settings_720p.Resolution = GraphicsResolutionType.EnhancedResolution
settings_720p.Background = GraphicsBackgroundType.White
settings_720p.Width = 1280
settings_720p.Height = 720
settings_720p.CurrentGraphicsDisplay = False

# %%
# Download and import the geometry file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Download the geometry file
geometry_path = download_file("Valve.pmdb", "pymechanical", "embedding")

# %%
# Import the geometry

# Define the model
model = app.Model

# Add a geometry import to the geometry import group
geometry_import = model.GeometryImportGroup.AddGeometryImport()

# Set the geometry import settings
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessNamedSelections = True

# Import the geometry file with the specified settings
geometry_import.Import(geometry_path, geometry_import_format, geometry_import_preferences)

# Visualize the model in 3D
app.plot()

# %%
# Assign the materials and mesh the geometry
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add the material assignment to the model materials
material_assignment = model.Materials.AddMaterialAssignment()

# Set the material to structural steel
material_assignment.Material = "Structural Steel"

# Create selection information for the geometry entities
selection_info = app.ExtAPI.SelectionManager.CreateSelectionInfo(
    Ansys.ACT.Interfaces.Common.SelectionTypeEnum.GeometryEntities
)

# Get the geometric bodies from the model and add their IDs to the selection info IDs list
selection_info.Ids = [
    body.GetGeoBody().Id
    for body in model.Geometry.GetChildren(
        Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Body, True
    )
]
# Set the material assignment location to the selected geometry entities
material_assignment.Location = selection_info

# %%
# Define the mesh settings and generate the mesh

# Define the mesh
mesh = model.Mesh
# Set the mesh element size to 25mm
mesh.ElementSize = Quantity(25, "mm")

# Generate the mesh
mesh.GenerateMesh()

# Activate the mesh and display the image
app.Tree.Activate([mesh])
set_camera_and_display_image(camera, graphics, settings_720p, output_path, "mesh.png")

# %%
# Add a static structural analysis and apply boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Add a static structural analysis to the model
analysis = model.AddStaticStructuralAnalysis()

# Add a fixed support to the analysis
fixed_support = analysis.AddFixedSupport()
# Set the fixed support location to the "NSFixedSupportFaces" object
fixed_support.Location = app.ExtAPI.DataModel.GetObjectsByName("NSFixedSupportFaces")[0]

# Add a frictionless support to the analysis
frictionless_support = analysis.AddFrictionlessSupport()
# Set the frictionless support location to the "NSFrictionlessSupportFaces" object
frictionless_support.Location = app.ExtAPI.DataModel.GetObjectsByName("NSFrictionlessSupportFaces")[
    0
]

# Add pressure to the analysis
pressure = analysis.AddPressure()
# Set the pressure location to the "NSInsideFaces" object
pressure.Location = app.ExtAPI.DataModel.GetObjectsByName("NSInsideFaces")[0]

# Set the pressure magnitude's input and output values
pressure.Magnitude.Inputs[0].DiscreteValues = [Quantity("0 [s]"), Quantity("1 [s]")]
pressure.Magnitude.Output.DiscreteValues = [Quantity("0 [Pa]"), Quantity("15 [MPa]")]

# Activate the analysis and display the image
analysis.Activate()
set_camera_and_display_image(
    camera, graphics, settings_720p, output_path, "boundary_conditions.png"
)

# %%
# Add results to the analysis solution

# Define the solution for the analysis
solution = analysis.Solution

# Add the total deformation and equivalent stress results to the solution
deformation = solution.AddTotalDeformation()
stress = solution.AddEquivalentStress()

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
# Show the total deformation image

# Activate the total deformation result and display the image
app.Tree.Activate([deformation])
set_camera_and_display_image(
    camera, graphics, settings_720p, output_path, "total_deformation_valve.png"
)

# %%
# Show the equivalent stress image

# Activate the equivalent stress result and display the image
app.Tree.Activate([stress])
set_camera_and_display_image(camera, graphics, settings_720p, output_path, "stress_valve.png")


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
# Export the stress animation

# Set the animation export format and settings
animation_export_format = Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat.GIF
settings_720p = Ansys.Mechanical.Graphics.AnimationExportSettings()
settings_720p.Width = 1280
settings_720p.Height = 720

# Export the animation of the equivalent stress result
valve_gif = output_path / "valve.gif"
stress.ExportAnimation(str(valve_gif), animation_export_format, settings_720p)

# Open the GIF file and create an animation
gif = Image.open(valve_gif)
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

# Get the path to the solve output file
solve_path = analysis.WorkingDir
# Get the solve output file path
solve_out_path = solve_path + "solve.out"
# If the solve output file exists, print its contents
if solve_out_path:
    with Path.open(solve_out_path, "rt") as file:
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
mechdat_file = output_path / "valve.mechdat"
app.save(str(mechdat_file))

# Close the app
app.close()

# Delete the example files
delete_downloads()
