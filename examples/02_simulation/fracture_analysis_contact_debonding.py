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

""".. _ref_contact:

Fracture Analysis - Contact debonding
-------------------------------------

The following example demonstrates the use of the Contact Debonding
featuring in Mechanical using the Cohesive Zone Material (CZM) method.
This example displaces two two-dimensional parts on a
double cantilever beam.
"""

# %%
# Import necessary libraries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~

import os

from PIL import Image
from matplotlib import image as mpimg
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

# %%
# Embed mechanical and set global variables

app = App()
app.update_globals(globals())
print(app)

cwd = os.path.join(os.getcwd(), "out")


def display_image(image_name):
    plt.figure(figsize=(16, 9))
    plt.imshow(mpimg.imread(os.path.join(cwd, image_name)))
    plt.xticks([])
    plt.yticks([])
    plt.axis("off")
    plt.show()


# %%
# Configure graphics for image export
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Graphics.Camera.SetSpecificViewOrientation(ViewOrientationType.Front)
image_export_format = GraphicsImageExportFormat.PNG
settings_720p = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
settings_720p.Resolution = GraphicsResolutionType.EnhancedResolution
settings_720p.Background = GraphicsBackgroundType.White
settings_720p.Width = 1280
settings_720p.Height = 720
settings_720p.CurrentGraphicsDisplay = False

# %%
# Download geometry and materials files
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

geometry_path = download_file("Contact_Debonding_Example.agdb", "pymechanical", "embedding")
mat1_path = download_file("Contact_Debonding_Example_Mat1.xml", "pymechanical", "embedding")
mat2_path = download_file("Contact_Debonding_Example_Mat2.xml", "pymechanical", "embedding")


# %%
# Import the geometry
# ~~~~~~~~~~~~~~~~~~~

geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessNamedSelections = True
geometry_import_preferences.AnalysisType = (
    Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.AnalysisType.Type2D
)
geometry_import.Import(geometry_path, geometry_import_format, geometry_import_preferences)

app.plot()

# %%
# Material import, named selections, and connections
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import materials

MODEL = Model
GEOMETRY = Model.Geometry
MAT_GRP = MODEL.Materials
MAT_GRP.Import(mat1_path)
MAT_GRP.Import(mat2_path)

PART = [x for x in Tree.AllObjects if x.Name == "Part 2"][0]
MAT_BODY = [
    i
    for i in MAT_GRP.GetChildren[Ansys.ACT.Automation.Mechanical.Material](True)
    if i.Name == "Interface Body Material"
][0]
MAT_CZM = [
    i
    for i in MAT_GRP.GetChildren[Ansys.ACT.Automation.Mechanical.Material](True)
    if i.Name == "CZM Crack Material"
][0]

# %%
# Connections

connections = MODEL.AddConnections()
CONNECTIONS_GRP = connections.AddConnectionGroup()
MODEL.Connections.CreateAutomaticConnections()
CONNECTIONS_GRP = Model.Connections
CONTACTS = [
    i
    for i in CONNECTIONS_GRP.GetChildren[
        Ansys.ACT.Automation.Mechanical.Connections.ConnectionGroup
    ](True)
    if i.Name == "Contacts"
][0]
CONTACT_REGION = [
    i
    for i in CONTACTS.GetChildren[Ansys.ACT.Automation.Mechanical.Connections.ContactRegion](True)
    if i.Name == "Contact Region"
][0]

# %%
# Named selections

NAMED_SELECTIONS = Model.NamedSelections
NS_EDGE_HIGH = [
    i
    for i in NAMED_SELECTIONS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "High_Edge"
][0]
NS_EDGE_LOW = [
    i
    for i in NAMED_SELECTIONS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Low_Edge"
][0]
NS_EDGES_SHORT = [
    i
    for i in NAMED_SELECTIONS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Short_Edges"
][0]
NS_EDGES_LONG = [
    i
    for i in NAMED_SELECTIONS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Long_Edges"
][0]
NS_EDGES_FIXED = [
    i
    for i in NAMED_SELECTIONS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Fixed_Edges"
][0]
NS_VERTEX_DISP1 = [
    i
    for i in NAMED_SELECTIONS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Disp1_Vertex"
][0]
NS_VERTEX_DISP2 = [
    i
    for i in NAMED_SELECTIONS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Disp2_Vertex"
][0]
NS_FACES_BOTH = [
    i
    for i in NAMED_SELECTIONS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Both_Faces"
][0]

# %%
# Define static structural analysis and settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MODEL.AddStaticStructuralAnalysis()
STATIC_STRUCTURAL = DataModel.AnalysisByName("Static Structural")
ANALYSIS_SETTINGS = STATIC_STRUCTURAL.AnalysisSettings
SOLUTION = STATIC_STRUCTURAL.Solution
MESH = Model.Mesh

# Set unit system

ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMM

# Set 2D behavior

GEOMETRY.Activate()
GEOMETRY.Model2DBehavior = Model2DBehavior.PlaneStrain

# Assign material

PART.Activate()
PART.Material = MAT_BODY.Name

# Define contact Region

CONTACT_REGION.Activate()
CONTACT_REGION.SourceLocation = NS_EDGE_HIGH
CONTACT_REGION.TargetLocation = NS_EDGE_LOW
CONTACT_REGION.ContactType = ContactType.Bonded
CONTACT_REGION.ContactFormulation = ContactFormulation.PurePenalty

# %%
# Define mesh controls and generate mesh
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MESH.Activate()
MESH.ElementOrder = ElementOrder.Quadratic
MESH.UseAdaptiveSizing = False
MESH.ElementSize = Quantity("0.75 [mm]")

SIZING_MESH = MESH.AddSizing()
SIZING_MESH.Location = NS_EDGES_SHORT
SIZING_MESH.ElementSize = Quantity("0.75 [mm]")
SIZING_MESH.Behavior = SizingBehavior.Hard

SIZING_MESH2 = MESH.AddSizing()
SIZING_MESH2.Location = NS_EDGES_LONG
SIZING_MESH2.ElementSize = Quantity("0.5 [mm]")
SIZING_MESH2.Behavior = SizingBehavior.Hard

FACE_MESHING = MESH.AddFaceMeshing()
FACE_MESHING.Location = NS_FACES_BOTH
FACE_MESHING.Method = FaceMeshingMethod.Quadrilaterals

MESH.Activate()
MESH.GenerateMesh()

Graphics.Camera.SetFit()
Graphics.ExportImage(os.path.join(cwd, "mesh.png"), image_export_format, settings_720p)
display_image("mesh.png")

# %%
# Add contact debonding object
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MODEL.Activate()
FRACTURE = MODEL.AddFracture()

CONTACT_DEBONDING = FRACTURE.AddContactDebonding()
CONTACT_DEBONDING.Material = MAT_CZM.Name
CONTACT_DEBONDING.ContactRegion = CONTACT_REGION

# %%
# Define analysis settings
# ~~~~~~~~~~~~~~~~~~~~~~~~

ANALYSIS_SETTINGS.Activate()
ANALYSIS_SETTINGS.AutomaticTimeStepping = AutomaticTimeStepping.On
ANALYSIS_SETTINGS.DefineBy = TimeStepDefineByType.Substeps
ANALYSIS_SETTINGS.MaximumSubsteps = 100
ANALYSIS_SETTINGS.InitialSubsteps = 100
ANALYSIS_SETTINGS.MinimumSubsteps = 100
ANALYSIS_SETTINGS.LargeDeflection = True

# %%
# Define boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Add fixed support

STATIC_STRUCTURAL.Activate()
FIXED_SUPPORT = STATIC_STRUCTURAL.AddFixedSupport()
FIXED_SUPPORT.Location = NS_EDGES_FIXED

# %%
# Add displacement

STATIC_STRUCTURAL.Activate()
DISPLACEMENT = STATIC_STRUCTURAL.AddDisplacement()
DISPLACEMENT.Location = NS_VERTEX_DISP1
DISPLACEMENT.DefineBy = LoadDefineBy.Components
DISPLACEMENT.YComponent.Output.DiscreteValues = [Quantity("10 [mm]")]

STATIC_STRUCTURAL.Activate()
DISPLACEMENT2 = STATIC_STRUCTURAL.AddDisplacement()
DISPLACEMENT2.Location = NS_VERTEX_DISP2
DISPLACEMENT2.DefineBy = LoadDefineBy.Components
DISPLACEMENT2.YComponent.Output.DiscreteValues = [Quantity("-10 [mm]")]

STATIC_STRUCTURAL.Activate()

Graphics.Camera.SetFit()
Graphics.ExportImage(
    os.path.join(cwd, "boundary_conditions.png"), image_export_format, settings_720p
)
display_image("boundary_conditions.png")

# %%
# Add results
# ~~~~~~~~~~~

SOLUTION.Activate()
DIRECTIONAL_DEFORMATION = SOLUTION.AddDirectionalDeformation()
DIRECTIONAL_DEFORMATION.NormalOrientation = NormalOrientationType.YAxis

FORCE_REACTION = SOLUTION.AddForceReaction()
FORCE_REACTION.BoundaryConditionSelection = DISPLACEMENT

# %%
# Solve
# ~~~~~

STATIC_STRUCTURAL.Activate()
SOLUTION.Solve(True)

# sphinx_gallery_start_ignore
assert str(SOLUTION.Status) == "Done", "Solution status is not 'Done'"
# sphinx_gallery_end_ignore

# %%
# Messages
# ~~~~~~~~

Messages = ExtAPI.Application.Messages
if Messages:
    for message in Messages:
        print(f"[{message.Severity}] {message.DisplayString}")
else:
    print("No [Info]/[Warning]/[Error] Messages")

# %%
# Display results
# ~~~~~~~~~~~~~~~
# Directional deformation

DIRECTIONAL_DEFORMATION.Activate()

Graphics.ExportImage(
    os.path.join(cwd, "directional_deformation.png"), image_export_format, settings_720p
)
display_image("directional_deformation.png")

# %%
# Force reaction

FORCE_REACTION.Activate()

Graphics.Camera.SetFit()
Graphics.ExportImage(os.path.join(cwd, "force_reaction.png"), image_export_format, settings_720p)
display_image("force_reaction.png")

# %%
# Export animation
# ~~~~~~~~~~~~~~~~

animation_export_format = Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat.GIF
settings_720p = Ansys.Mechanical.Graphics.AnimationExportSettings()
settings_720p.Width = 1280
settings_720p.Height = 720

FORCE_REACTION.ExportAnimation(
    os.path.join(cwd, "force_reaction.gif"), animation_export_format, settings_720p
)
gif = Image.open(os.path.join(cwd, "force_reaction.gif"))
fig, ax = plt.subplots(figsize=(16, 9))
ax.axis("off")
img = ax.imshow(gif.convert("RGBA"))


def update(frame):
    gif.seek(frame)
    img.set_array(gif.convert("RGBA"))
    return [img]


ani = FuncAnimation(fig, update, frames=range(gif.n_frames), interval=100, repeat=True, blit=True)
plt.show()

# %%
# Display output file from solve
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def write_file_contents_to_console(path):
    """Write file contents to console."""
    with open(path, "rt") as file:
        for line in file:
            print(line, end="")


solve_path = STATIC_STRUCTURAL.WorkingDir
solve_out_path = os.path.join(solve_path, "solve.out")
if solve_out_path:
    write_file_contents_to_console(solve_out_path)

# %%
# Project tree
# ~~~~~~~~~~~~

app.print_tree()

# %%
# Cleanup
# ~~~~~~~
# Save project

app.save(os.path.join(cwd, "contact_debonding.mechdat"))
app.new()

# %%
# Delete example files

delete_downloads()
