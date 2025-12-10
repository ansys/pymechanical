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

""".. _ref_topology_optimization:

Topology optimization of a simple cantilever beam
-------------------------------------------------

This example demonstrates the structural topology optimization of a simple
cantilever beam. The structural analysis is performed with basic constraints and
load, which is then transferred to the topology optimization.
"""

# %%
# Import the necessary libraries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from pathlib import Path
from typing import TYPE_CHECKING

from matplotlib import image as mpimg, pyplot as plt

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

graphics = app.Graphics
camera = graphics.Camera

# Set the camera orientation to the front view
camera.SetSpecificViewOrientation(ViewOrientationType.Front)

# Set the image export format and settings
image_export_format = GraphicsImageExportFormat.PNG
settings_720p = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
settings_720p.Resolution = GraphicsResolutionType.EnhancedResolution
settings_720p.Background = GraphicsBackgroundType.White
settings_720p.Width = 1280
settings_720p.Height = 720
settings_720p.CurrentGraphicsDisplay = False

# %%
# Import the structural analysis model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Download ``.mechdat`` file
structural_mechdat_file = download_file("cantilever.mechdat", "pymechanical", "embedding")

# Open the project file
app.open(structural_mechdat_file)

# Define the model
model = app.Model

# Get the structural analysis object
struct = model.Analyses[0]

# sphinx_gallery_start_ignore
assert struct.ObjectState == ObjectState.Solved
# sphinx_gallery_end_ignore

# Get the structural analysis object's solution and solve it
struct_sln = struct.Solution
struct_sln.Solve(True)

# sphinx_gallery_start_ignore
assert struct_sln.Status == SolutionStatusType.Done, "Solution status is not 'Done'"
# sphinx_gallery_end_ignore

# %%
# Display the structural analysis results
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Activate the total deformation result and display the image

struct_sln.Children[1].Activate()
set_camera_and_display_image(camera, graphics, settings_720p, output_path, "total_deformation.png")

# %%
# Activate the equivalent stress result and display the image

struct_sln.Children[2].Activate()
set_camera_and_display_image(camera, graphics, settings_720p, output_path, "equivalent_stress.png")

# %%
# Topology optimization
# ~~~~~~~~~~~~~~~~~~~~~

# Set the MKS unit system
app.ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardMKS

# Add the topology optimization analysis to the model and transfer data from the
# structural analysis
topology_optimization = model.AddTopologyOptimizationAnalysis()
topology_optimization.TransferDataFrom(struct)

# Get the optimization region from the data model
optimization_region = DataModel.GetObjectsByType(DataModelObjectCategory.OptimizationRegion)[0]
# Set the optimization region's boundary condition to all loads and supports
optimization_region.BoundaryCondition = BoundaryConditionType.AllLoadsAndSupports
# Set the optimization region's optimization type to topology density
optimization_region.OptimizationType = OptimizationType.TopologyDensity

# sphinx_gallery_start_ignore
assert topology_optimization.ObjectState == ObjectState.NotSolved
# sphinx_gallery_end_ignore

# Delete the mass response constraint from the topology optimization
mass_constraint = topology_optimization.Children[3]
app.DataModel.Remove(mass_constraint)

# Add a volume response constraint to the topology optimization
volume_constraint = topology_optimization.AddVolumeConstraint()

# Add a member size manufacturing constraint to the topology optimization
mem_size_manufacturing_constraint = topology_optimization.AddMemberSizeManufacturingConstraint()
# Set the constraint's minimum to manual and its minimum size to 2.4m
mem_size_manufacturing_constraint.Minimum = ManuMemberSizeControlledType.Manual
mem_size_manufacturing_constraint.MinSize = Quantity("2.4 [m]")

# Activate the topology optimization analysis and display the image
topology_optimization.Activate()
set_camera_and_display_image(
    camera, graphics, settings_720p, output_path, "boundary_conditions.png"
)

# %%
# Solve the solution
# ~~~~~~~~~~~~~~~~~~

# Get the topology optimization analysis solution
top_opt_sln = topology_optimization.Solution
# Solve the solution
top_opt_sln.Solve(True)

# sphinx_gallery_start_ignore
assert top_opt_sln.Status == SolutionStatusType.Done, "Solution status is not 'Done'"
# sphinx_gallery_end_ignore

# %%
# Show messages
# ~~~~~~~~~~~~~

# Print all messages from Mechanical
app.messages.show()

# %%
# Display the results
# ~~~~~~~~~~~~~~~~~~~

# Get the topology density result and activate it
top_opt_sln.Children[1].Activate()
topology_density = top_opt_sln.Children[1]

# %%
# Add smoothing to the stereolithography (STL)

# Add smoothing to the topology density result
topology_density.AddSmoothing()

# Evaluate all results for the topology optimization solution
topology_optimization.Solution.EvaluateAllResults()

# Activate the topology density result after smoothing and display the image
topology_density.Children[0].Activate()
set_camera_and_display_image(
    camera, graphics, settings_720p, output_path, "topo_opitimized_smooth.png"
)

# %%
# Export the animation

app.Tree.Activate([topology_density])

# Set the animation export format and settings
animation_export_format = Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat.GIF
settings_720p = Ansys.Mechanical.Graphics.AnimationExportSettings()
settings_720p.Width = 1280
settings_720p.Height = 720

# Export the animation of the topology density result
topology_optimized_gif = output_path / "topology_opitimized.gif"
topology_density.ExportAnimation(
    str(topology_optimized_gif), animation_export_format, settings_720p
)

# %%
# .. image:: /_static/basic/Topo_opitimized.gif

# %%
# Review the results

# Print the topology density results
print("Topology Density Results")
print("Minimum Density: ", topology_density.Minimum)
print("Maximum Density: ", topology_density.Maximum)
print("Iteration Number: ", topology_density.IterationNumber)
print("Original Volume: ", topology_density.OriginalVolume.Value)
print("Final Volume: ", topology_density.FinalVolume.Value)
print("Percent Volume of Original: ", topology_density.PercentVolumeOfOriginal)
print("Original Mass: ", topology_density.OriginalMass.Value)
print("Final Mass: ", topology_density.FinalMass.Value)
print("Percent Mass of Original: ", topology_density.PercentMassOfOriginal)

# %%
# Display the project tree
# ~~~~~~~~~~~~~~~~~~~~~~~~

app.print_tree()

# %%
# Clean up the project
# ~~~~~~~~~~~~~~~~~~~~

# Save the project file
mechdat_file = output_path / "cantilever_beam_topology_optimization.mechdat"
app.save_as(str(mechdat_file), overwrite=True)

# Close the app
app.close()

# Delete the example files
delete_downloads()
