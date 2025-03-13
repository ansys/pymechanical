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

""".. _ref_bolt_pretension:

Bolt Pretension
---------------

This example demonstrates how to insert a Static Structural analysis
into a new Mechanical session and execute a sequence of Python scripting
commands that define and solve a bolt-pretension analysis.
Scripts then evaluate the following results: deformation,
equivalent stresses, contact, and bolt
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

Graphics.Camera.SetSpecificViewOrientation(ViewOrientationType.Iso)
Graphics.Camera.SetFit()
image_export_format = GraphicsImageExportFormat.PNG
settings_720p = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
settings_720p.Resolution = GraphicsResolutionType.EnhancedResolution
settings_720p.Background = GraphicsBackgroundType.White
settings_720p.Width = 1280
settings_720p.Height = 720
settings_720p.CurrentGraphicsDisplay = False
Graphics.Camera.Rotate(180, CameraAxisType.ScreenY)

# %%
# Download and import geometry
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Download the geometry file

geometry_path = download_file("example_06_bolt_pret_geom.agdb", "pymechanical", "00_basic")

# %%
# Import geometry

geometry_import_group = Model.GeometryImportGroup
geometry_import = geometry_import_group.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessNamedSelections = True
geometry_import.Import(geometry_path, geometry_import_format, geometry_import_preferences)

# sphinx_gallery_start_ignore
assert str(geometry_import.ObjectState) == "Solved", "Geometry Import unsuccessful"
# sphinx_gallery_end_ignore

app.plot()


# %%
# Download and import material
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Download materials

mat_Copper_file_path = download_file("example_06_Mat_Copper.xml", "pymechanical", "00_basic")
mat_Steel_file_path = download_file("example_06_Mat_Steel.xml", "pymechanical", "00_basic")

# %%
# Import materials

MAT = Model.Materials
MAT.Import(mat_Copper_file_path)
MAT.Import(mat_Steel_file_path)

# sphinx_gallery_start_ignore
assert str(MAT.ObjectState) == "FullyDefined", "Materials are not defined"
# sphinx_gallery_end_ignore

# %%
# Define Analysis and unit system
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Add Structural analysis

Model.AddStaticStructuralAnalysis()
STAT_STRUC = Model.Analyses[0]
STAT_STRUC_SOLN = STAT_STRUC.Solution
STAT_STRUC_ANA_SETTING = STAT_STRUC.Children[0]

# %%
# Set up the unit system.

ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMM

# %%
# Store all main tree nodes as variables

MODEL = Model
GEOM = Model.Geometry
CONN_GRP = Model.Connections
CS_GRP = Model.CoordinateSystems
MSH = Model.Mesh
NS_GRP = Model.NamedSelections

# %%
# Store named selections

block3_block2_cont_NS = [x for x in Tree.AllObjects if x.Name == "block3_block2_cont"][0]
block3_block2_targ_NS = [x for x in Tree.AllObjects if x.Name == "block3_block2_targ"][0]
shank_block3_targ_NS = [x for x in Tree.AllObjects if x.Name == "shank_block3_targ"][0]
shank_block3_cont_NS = [x for x in Tree.AllObjects if x.Name == "shank_block3_cont"][0]
block1_washer_cont_NS = [x for x in Tree.AllObjects if x.Name == "block1_washer_cont"][0]
block1_washer_targ_NS = [x for x in Tree.AllObjects if x.Name == "block1_washer_targ"][0]
washer_bolt_cont_NS = [x for x in Tree.AllObjects if x.Name == "washer_bolt_cont"][0]
washer_bolt_targ_NS = [x for x in Tree.AllObjects if x.Name == "washer_bolt_targ"][0]
shank_bolt_targ_NS = [x for x in Tree.AllObjects if x.Name == "shank_bolt_targ"][0]
shank_bolt_cont_NS = [x for x in Tree.AllObjects if x.Name == "shank_bolt_cont"][0]
block2_block1_cont_NS = [x for x in Tree.AllObjects if x.Name == "block2_block1_cont"][0]
block2_block1_targ_NS = [x for x in Tree.AllObjects if x.Name == "block2_block1_targ"][0]
all_bodies = [x for x in Tree.AllObjects if x.Name == "all_bodies"][0]
bodies_5 = [x for x in Tree.AllObjects if x.Name == "bodies_5"][0]
shank = [x for x in Tree.AllObjects if x.Name == "shank"][0]
shank_face = [x for x in Tree.AllObjects if x.Name == "shank_face"][0]
shank_face2 = [x for x in Tree.AllObjects if x.Name == "shank_face2"][0]
bottom_surface = [x for x in Tree.AllObjects if x.Name == "bottom_surface"][0]
block2_surface = [x for x in Tree.AllObjects if x.Name == "block2_surface"][0]
shank_surface = [x for x in Tree.AllObjects if x.Name == "shank_surface"][0]

# %%
# Assign material to bodies

SURFACE1 = GEOM.Children[0].Children[0]
SURFACE1.Material = "Steel"

SURFACE2 = GEOM.Children[1].Children[0]
SURFACE2.Material = "Copper"

SURFACE3 = GEOM.Children[2].Children[0]
SURFACE3.Material = "Copper"

SURFACE4 = GEOM.Children[3].Children[0]
SURFACE4.Material = "Steel"

SURFACE5 = GEOM.Children[4].Children[0]
SURFACE5.Material = "Steel"

SURFACE6 = GEOM.Children[5].Children[0]
SURFACE6.Material = "Steel"

# %%
# Define coordinate system
# ~~~~~~~~~~~~~~~~~~~~~~~~~

coordinate_system = CS_GRP.AddCoordinateSystem()
coordinate_system.OriginDefineBy = CoordinateSystemAlignmentType.Fixed
coordinate_system.OriginX = Quantity(-195, "mm")
coordinate_system.OriginY = Quantity(100, "mm")
coordinate_system.OriginZ = Quantity(50, "mm")
coordinate_system.PrimaryAxis = CoordinateSystemAxisType.PositiveZAxis

# %%
# Define Contacts
# ~~~~~~~~~~~~~~~
# Change contact settings

# %%
# Delete existing contacts

for connection in CONN_GRP.Children:
    if connection.DataModelObjectCategory == DataModelObjectCategory.ConnectionGroup:
        connection.Delete()

CONT_REG1 = CONN_GRP.AddContactRegion()
CONT_REG1.SourceLocation = NS_GRP.Children[0]
CONT_REG1.TargetLocation = NS_GRP.Children[1]
CONT_REG1.ContactType = ContactType.Frictional
CONT_REG1.FrictionCoefficient = 0.2
CONT_REG1.SmallSliding = ContactSmallSlidingType.Off
CONT_REG1.UpdateStiffness = UpdateContactStiffness.Never
CMD1 = CONT_REG1.AddCommandSnippet()

# %%
# Add missing contact keyopt and Archard Wear Model using a command snippet

AWM = """keyopt,cid,9,5
rmodif,cid,10,0.00
rmodif,cid,23,0.001"""
CMD1.AppendText(AWM)

CONTS = CONN_GRP.Children[0]
CONT_REG2 = CONTS.AddContactRegion()
CONT_REG2.SourceLocation = NS_GRP.Children[3]
CONT_REG2.TargetLocation = NS_GRP.Children[2]
CONT_REG2.ContactType = ContactType.Bonded
CONT_REG2.ContactFormulation = ContactFormulation.MPC

CONT_REG3 = CONTS.AddContactRegion()
CONT_REG3.SourceLocation = NS_GRP.Children[4]
CONT_REG3.TargetLocation = NS_GRP.Children[5]
CONT_REG3.ContactType = ContactType.Frictional
CONT_REG3.FrictionCoefficient = 0.2
CONT_REG3.SmallSliding = ContactSmallSlidingType.Off
CONT_REG3.UpdateStiffness = UpdateContactStiffness.Never
CMD3 = CONT_REG3.AddCommandSnippet()

# Add missing contact keyopt and Archard Wear Model using a command snippet

AWM3 = """keyopt,cid,9,5
rmodif,cid,10,0.00
rmodif,cid,23,0.001"""
CMD3.AppendText(AWM3)

CONT_REG4 = CONTS.AddContactRegion()
CONT_REG4.SourceLocation = NS_GRP.Children[6]
CONT_REG4.TargetLocation = NS_GRP.Children[7]
CONT_REG4.ContactType = ContactType.Bonded
CONT_REG4.ContactFormulation = ContactFormulation.MPC

CONT_REG5 = CONTS.AddContactRegion()
CONT_REG5.SourceLocation = NS_GRP.Children[9]
CONT_REG5.TargetLocation = NS_GRP.Children[8]
CONT_REG5.ContactType = ContactType.Bonded
CONT_REG5.ContactFormulation = ContactFormulation.MPC

CONT_REG6 = CONTS.AddContactRegion()
CONT_REG6.SourceLocation = NS_GRP.Children[10]
CONT_REG6.TargetLocation = NS_GRP.Children[11]
CONT_REG6.ContactType = ContactType.Frictional
CONT_REG6.FrictionCoefficient = 0.2
CONT_REG6.SmallSliding = ContactSmallSlidingType.Off
CONT_REG6.UpdateStiffness = UpdateContactStiffness.Never
CMD6 = CONT_REG6.AddCommandSnippet()

# Add missing contact keyopt and Archard Wear Model using a command snippet

AWM6 = """keyopt,cid,9,5
rmodif,cid,10,0.00
rmodif,cid,23,0.001"""
CMD6.AppendText(AWM6)

# %%
# Mesh
# ~~~~

Hex_Method = MSH.AddAutomaticMethod()
Hex_Method.Location = all_bodies
Hex_Method.Method = MethodType.Automatic

BODY_SIZING1 = MSH.AddSizing()
BODY_SIZING1.Location = bodies_5
BODY_SIZING1.ElementSize = Quantity(15, "mm")

BODY_SIZING2 = MSH.AddSizing()
BODY_SIZING2.Location = shank
BODY_SIZING2.ElementSize = Quantity(7, "mm")

Face_Meshing = MSH.AddFaceMeshing()
Face_Meshing.Location = shank_face
Face_Meshing.MappedMesh = False

Sweep_Method = MSH.AddAutomaticMethod()
Sweep_Method.Location = shank
Sweep_Method.Method = MethodType.Sweep
Sweep_Method.SourceTargetSelection = 2
Sweep_Method.SourceLocation = shank_face
Sweep_Method.TargetLocation = shank_face2

MSH.Activate()
MSH.GenerateMesh()

Graphics.Camera.SetFit()
Graphics.ExportImage(os.path.join(cwd, "mesh.png"), image_export_format, settings_720p)
display_image("mesh.png")

# %%
# Analysis settings
# ~~~~~~~~~~~~~~~~~

STAT_STRUC_ANA_SETTING.NumberOfSteps = 4
step_index_list = [1]

with Transaction():
    for step_index in step_index_list:
        STAT_STRUC_ANA_SETTING.SetAutomaticTimeStepping(step_index, AutomaticTimeStepping.Off)

STAT_STRUC_ANA_SETTING.Activate()
step_index_list = [1]

with Transaction():
    for step_index in step_index_list:
        STAT_STRUC_ANA_SETTING.SetNumberOfSubSteps(step_index, 2)

STAT_STRUC_ANA_SETTING.Activate()
STAT_STRUC_ANA_SETTING.SolverType = SolverType.Direct
STAT_STRUC_ANA_SETTING.SolverPivotChecking = SolverPivotChecking.Off

# %%
# Define loads and boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FIX_SUP = STAT_STRUC.AddFixedSupport()
FIX_SUP.Location = block2_surface

Tabular_Force = STAT_STRUC.AddForce()
Tabular_Force.Location = bottom_surface
Tabular_Force.DefineBy = LoadDefineBy.Components
Tabular_Force.XComponent.Inputs[0].DiscreteValues = [
    Quantity("0[s]"),
    Quantity("1[s]"),
    Quantity("2[s]"),
    Quantity("3[s]"),
    Quantity("4[s]"),
]
Tabular_Force.XComponent.Output.DiscreteValues = [
    Quantity("0[N]"),
    Quantity("0[N]"),
    Quantity("5.e+005[N]"),
    Quantity("0[N]"),
    Quantity("-5.e+005[N]"),
]

Bolt_Pretension = STAT_STRUC.AddBoltPretension()
Bolt_Pretension.Location = shank_surface
Bolt_Pretension.Preload.Inputs[0].DiscreteValues = [
    Quantity("1[s]"),
    Quantity("2[s]"),
    Quantity("3[s]"),
    Quantity("4[s]"),
]
Bolt_Pretension.Preload.Output.DiscreteValues = [
    Quantity("6.1363e+005[N]"),
    Quantity("0 [N]"),
    Quantity("0 [N]"),
    Quantity("0[N]"),
]
Bolt_Pretension.SetDefineBy(2, BoltLoadDefineBy.Lock)
Bolt_Pretension.SetDefineBy(3, BoltLoadDefineBy.Lock)
Bolt_Pretension.SetDefineBy(4, BoltLoadDefineBy.Lock)

Tree.Activate([Bolt_Pretension])
Graphics.ExportImage(
    os.path.join(cwd, "loads_and_boundaryconditions.png"),
    image_export_format,
    settings_720p,
)
display_image("loads_and_boundaryconditions.png")

# %%
# Insert results
# ~~~~~~~~~~~~~~

Post_Contact_Tool = STAT_STRUC_SOLN.AddContactTool()
Post_Contact_Tool.ScopingMethod = GeometryDefineByType.Worksheet
Bolt_Tool = STAT_STRUC_SOLN.AddBoltTool()
Bolt_Working_Load = Bolt_Tool.AddWorkingLoad()
Total_Deformation = STAT_STRUC_SOLN.AddTotalDeformation()
Equivalent_stress_1 = STAT_STRUC_SOLN.AddEquivalentStress()
Equivalent_stress_2 = STAT_STRUC_SOLN.AddEquivalentStress()
Equivalent_stress_2.Location = shank
Force_Reaction_1 = STAT_STRUC_SOLN.AddForceReaction()
Force_Reaction_1.BoundaryConditionSelection = FIX_SUP
Moment_Reaction_2 = STAT_STRUC_SOLN.AddMomentReaction()
Moment_Reaction_2.BoundaryConditionSelection = FIX_SUP

# %%
# Solve
# ~~~~~

STAT_STRUC_SOLN.Solve(True)
STAT_STRUC_SS = STAT_STRUC_SOLN.Status
# sphinx_gallery_start_ignore
assert str(STAT_STRUC_SS) == "Done", "Solution status is not 'Done'"
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
# Results
# ~~~~~~~
# Total deformation

Tree.Activate([Total_Deformation])
Graphics.Camera.SetFit()
Graphics.ExportImage(os.path.join(cwd, "total_deformation.png"), image_export_format, settings_720p)
display_image("total_deformation.png")

# %%
# Equivalent stress on all bodies

Tree.Activate([Equivalent_stress_1])
Graphics.Camera.SetFit()
Graphics.ExportImage(
    os.path.join(cwd, "equivalent_stress_total.png"), image_export_format, settings_720p
)
display_image("equivalent_stress_total.png")

# %%
# Equivalent stress on shank

Tree.Activate([Equivalent_stress_2])
Graphics.Camera.SetFit()
Graphics.ExportImage(
    os.path.join(cwd, "equivalent_stress_shank.png"), image_export_format, settings_720p
)
display_image("equivalent_stress_shank.png")

# %%
# Export contact status animation

Post_Contact_Tool_status = Post_Contact_Tool.Children[0]
Tree.Activate([Post_Contact_Tool_status])
Graphics.Camera.SetFit()
animation_export_format = Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat.GIF
settings_720p = Ansys.Mechanical.Graphics.AnimationExportSettings()
settings_720p.Width = 1280
settings_720p.Height = 720

Post_Contact_Tool_status.ExportAnimation(
    os.path.join(cwd, "contact_status.gif"), animation_export_format, settings_720p
)
gif = Image.open(os.path.join(cwd, "contact_status.gif"))
fig, ax = plt.subplots(figsize=(16, 9))
ax.axis("off")
img = ax.imshow(gif.convert("RGBA"))


def update(frame):
    gif.seek(frame)
    img.set_array(gif.convert("RGBA"))
    return [img]


ani = FuncAnimation(fig, update, frames=range(gif.n_frames), interval=200, repeat=True, blit=True)
plt.show()

# %%
# Project tree
# ~~~~~~~~~~~~

app.print_tree()

# %%
# Cleanup
# ~~~~~~~
# Save project

app.save(os.path.join(cwd, "bolt_pretension.mechdat"))
app.new()

# %%
# Delete the example file

delete_downloads()
