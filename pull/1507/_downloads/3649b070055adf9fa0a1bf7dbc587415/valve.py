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

# Set camera and graphics

graphics = app.Graphics
camera = graphics.Camera

# %%
# Download and import the geometry file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Download the geometry file
geometry_path = download_file("Valve.pmdb", "pymechanical", "embedding")

# %%
# Import the geometry
# ~~~~~~~~~~~~~~~~~~~

# Define the model
model = app.Model

app.helpers.import_geometry(geometry_path, process_named_selections=True)

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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define the mesh
mesh = model.Mesh
# Set the mesh element size to 25mm
mesh.ElementSize = Quantity(25, "mm")

# Generate the mesh
mesh.GenerateMesh()

# Activate the mesh and display the image
image_path = output_path / "mesh.png"
camera.SetFit()
app.helpers.export_image(mesh, image_path)
app.helpers.display_image(image_path)

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
image_path = output_path / "boundary_conditions.png"
camera.SetFit()
app.helpers.export_image(analysis, image_path)
app.helpers.display_image(image_path)

# %%
# Add results to the analysis solution
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Activate the total deformation result and display the image
app.Tree.Activate([deformation])
image_path = output_path / "total_deformation_valve.png"
camera.SetFit()
app.helpers.export_image(deformation, image_path)
app.helpers.display_image(image_path)

# %%
# Show the equivalent stress image
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Activate the equivalent stress result and display the image
app.Tree.Activate([stress])
image_path = output_path / "stress_valve.png"
camera.SetFit()
app.helpers.export_image(stress, image_path)
app.helpers.display_image(image_path)


# %%
# Export the stress animation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

camera.SetFit()
valve_gif = output_path / "valve.gif"
app.helpers.export_animation(stress, valve_gif)

# %%
# Display the stress animation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Open the GIF file and create an animation
gif = Image.open(valve_gif)
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
# Display the output file from the solve
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Get the path to the solve output file
solve_path = Path(analysis.WorkingDir)
# Get the solve output file path
solve_out_path = solve_path / "solve.out"
# If the solve output file exists, print its contents
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
mechdat_file = output_path / "valve.mechdat"
app.save_as(str(mechdat_file), overwrite=True)

# Close the app
app.close()

# Delete the example files
delete_downloads()
