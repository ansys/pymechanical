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

from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

if TYPE_CHECKING:
    pass

# %%
# Initialize the embedded application
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app = App(globals=globals())
print(app)

# %%
# Setup the output path and camera
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Set the path for the output files (images, gifs, mechdat)
output_path = Path.cwd() / "out"

# Set the camera orientation to the front view
app.helpers.setup_view("front")

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
image_path = output_path / "total_deformation.png"
app.helpers.setup_view()
app.helpers.export_image(struct_sln.Children[1], image_path)
app.helpers.display_image(image_path)
# %%
# Activate the equivalent stress result and display the image

struct_sln.Children[2].Activate()
image_path = output_path / "equivalent_stress.png"
app.helpers.setup_view()
app.helpers.export_image(struct_sln.Children[2], image_path)
app.helpers.display_image(image_path)

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
app.helpers.setup_view()
app.helpers.export_image(topology_optimization, output_path / "boundary_conditions.png")
app.helpers.display_image(output_path / "boundary_conditions.png")

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
image_path = output_path / "topo_opitimized_smooth.png"
app.helpers.setup_view()
app.helpers.export_image(topology_density.Children[0], image_path)
app.helpers.display_image(image_path)

# %%
# Export the animation

topology_optimized_gif = output_path / "topology_opitimized.gif"
app.helpers.export_animation(topology_density, topology_optimized_gif)

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
