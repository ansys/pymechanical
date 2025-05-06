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

""".. _ref_modal_acoustics_analysis:

Modal acoustics analysis
------------------------

This example demonstrate modal acoustic analysis that involves
modeling both a structure and the surrounding
fluid to analyze frequencies and standing wave patterns within the structure.
This type of analysis is essential for applications such as Sonar, concert hall design,
noise reduction in various settings, audio speaker design, and geophysical exploration.

Mechanical enables you to model pure acoustic problems and fluid-structure
interaction (FSI) problems.A coupled acoustic analysis accounts for FSI.
An uncoupled acoustic analysis simulates
the fluid only and ignores any fluid-structure interaction.
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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Graphics.Camera.SetSpecificViewOrientation(ViewOrientationType.Iso)
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

geometry_path = download_file("sloshing_geometry.agdb", "pymechanical", "embedding")
mat_path = download_file("Water_material_explicit.xml", "pymechanical", "embedding")


# %%
# Import the geometry
# ~~~~~~~~~~~~~~~~~~~

geometry_import_group = Model.GeometryImportGroup
geometry_import = geometry_import_group.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessNamedSelections = True
geometry_import.Import(geometry_path, geometry_import_format, geometry_import_preferences)

Graphics.Camera.SetFit()
Graphics.ExportImage(os.path.join(cwd, "geometry.png"), image_export_format, settings_720p)
display_image("geometry.png")

# %%
# Store all variables necessary for analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GEOM = Model.Geometry
MESH = Model.Mesh
NS = Model.NamedSelections
CONN = Model.Connections
MAT = Model.Materials

# %%
# Import material setup analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Model.AddModalAcousticAnalysis()
ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardMKS
MAT.Import(mat_path)
print("Material Import Done !")

# %%
# Get all required named selections and assign materials
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

acst_bodies = [
    i
    for i in NS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Acoustic_bodies"
][0]
struct_bodies = [
    i
    for i in NS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Structural_bodies"
][0]
top_bodies = [
    i
    for i in NS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "top_bodies"
][0]
cont_bodies = [
    i
    for i in NS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "container_bodies"
][0]
cont_V1 = [
    i
    for i in NS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Cont_V1"
][0]
cont_V2 = [
    i
    for i in NS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Cont_V2"
][0]
cont_V3 = [
    i
    for i in NS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Cont_V3"
][0]
cont_face1 = [
    i
    for i in NS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Cont_face1"
][0]
cont_face2 = [
    i
    for i in NS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Cont_face2"
][0]
cont_face3 = [
    i
    for i in NS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Cont_face3"
][0]
cont_face4 = [
    i
    for i in NS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Cont_face4"
][0]
free_faces = [
    i
    for i in NS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "Free_faces"
][0]
fsi_faces = [
    i
    for i in NS.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
    if i.Name == "FSI_faces"
][0]

solid1 = [
    i for i in GEOM.GetChildren[Ansys.ACT.Automation.Mechanical.Body](True) if i.Name == "Solid1"
][0]
solid2 = [
    i for i in GEOM.GetChildren[Ansys.ACT.Automation.Mechanical.Body](True) if i.Name == "Solid2"
][0]
solid3 = [
    i for i in GEOM.GetChildren[Ansys.ACT.Automation.Mechanical.Body](True) if i.Name == "Solid3"
][0]
solid4 = [
    i for i in GEOM.GetChildren[Ansys.ACT.Automation.Mechanical.Body](True) if i.Name == "Solid4"
][0]


# %%
# Assign material water to acoustic parts

solid1.Material = "WATER"
solid2.Material = "WATER"
solid3.Material = "WATER"
solid4.Material = "WATER"

# %%
# Mesh
# ~~~~

MESH.ElementOrder = ElementOrder.Quadratic

method1 = MESH.AddAutomaticMethod()
method1.Location = acst_bodies
method1.Method = MethodType.AllTriAllTet

method2 = MESH.AddAutomaticMethod()
method2.Location = top_bodies
method2.Method = MethodType.Automatic

# Add mesh sizing

sizing1 = MESH.AddSizing()
sizing1.Location = top_bodies
sizing1.ElementSize = Quantity("0.2 [m]")
sizing1.Behavior = SizingBehavior.Hard

# Add mesh sizing

sizing2 = MESH.AddSizing()
sizing2.Location = acst_bodies
sizing2.ElementSize = Quantity("0.2 [m]")
sizing2.Behavior = SizingBehavior.Hard

# Add mesh method

method3 = MESH.AddAutomaticMethod()
method3.Location = cont_bodies
method3.Method = MethodType.Sweep
method3.SourceTargetSelection = 4

MESH.GenerateMesh()

Graphics.ExportImage(os.path.join(cwd, "mesh.png"), image_export_format, settings_720p)
display_image("mesh.png")

# %%
# Insert contacts
# ~~~~~~~~~~~~~~~
# Contact 1
CONN_GROUP = CONN.AddConnectionGroup()
CONT1 = CONN_GROUP.AddContactRegion()
CONT1.SourceLocation = cont_V1
CONT1.TargetLocation = cont_face1
CONT1.ContactFormulation = ContactFormulation.MPC
CONT1.Behavior = ContactBehavior.Asymmetric
CONT1.PinballRegion = ContactPinballType.Radius
CONT1.PinballRadius = Quantity("0.25 [m]")

# %%
# Contact 2

CONT2 = CONN_GROUP.AddContactRegion()
CONT2.SourceLocation = cont_V2
CONT2.TargetLocation = cont_face2
CONT2.ContactFormulation = ContactFormulation.MPC
CONT2.Behavior = ContactBehavior.Asymmetric
CONT2.PinballRegion = ContactPinballType.Radius
CONT2.PinballRadius = Quantity("0.25 [m]")

# %%
# Contact 3

CONT3 = CONN_GROUP.AddContactRegion()
CONT3.SourceLocation = cont_V3
CONT3.TargetLocation = cont_face3
CONT3.ContactFormulation = ContactFormulation.MPC
CONT3.Behavior = ContactBehavior.Asymmetric
CONT3.PinballRegion = ContactPinballType.Radius
CONT3.PinballRadius = Quantity("0.25 [m]")

# %%
# Contact 3

sel_manager = ExtAPI.SelectionManager
cnv4 = DataModel.GeoData.Assemblies[0].Parts[1].Bodies[0].Vertices[3]
cont_V4 = sel_manager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
cont_V4.Entities = [cnv4]

# %%
# Contact 4

CONT4 = CONN_GROUP.AddContactRegion()
CONT4.TargetLocation = cont_face4
CONT4.SourceLocation = cont_V4
CONT4.ContactFormulation = ContactFormulation.MPC
CONT4.Behavior = ContactBehavior.Asymmetric
CONT4.PinballRegion = ContactPinballType.Radius
CONT4.PinballRadius = Quantity("0.25 [m]")

# %%
# Fully define Modal Multiphysics region with two physics regions

MODAL_ACST = DataModel.Project.Model.Analyses[0]
ACOUST_REG = MODAL_ACST.Children[2]
ACOUST_REG.Location = acst_bodies


STRUCT_REG = MODAL_ACST.AddPhysicsRegion()
STRUCT_REG.Structural = True
STRUCT_REG.RenameBasedOnDefinition()
STRUCT_REG.Location = struct_bodies


# %%
# Analysis settings
# ~~~~~~~~~~~~~~~~~

ANALYSIS_SETTINGS = MODAL_ACST.Children[1]
ANALYSIS_SETTINGS.MaximumModesToFind = 12
ANALYSIS_SETTINGS.SearchRangeMinimum = Quantity("0.1 [Hz]")
ANALYSIS_SETTINGS.SolverType = SolverType.Unsymmetric
ANALYSIS_SETTINGS.GeneralMiscellaneous = True
ANALYSIS_SETTINGS.CalculateReactions = True

# %%
# Boundary conditions and load
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Free surface

FREE_SF = MODAL_ACST.AddAcousticFreeSurface()
FREE_SF.Location = free_faces

# %%
# Solid fluid interface

FSI_OBJ = MODAL_ACST.AddFluidSolidInterface()
FSI_OBJ.Location = fsi_faces

# %%
# Gravity

ACCELERATION = MODAL_ACST.AddAcceleration()
ACCELERATION.DefineBy = LoadDefineBy.Components
ACCELERATION.YComponent.Output.DiscreteValues = [Quantity("9.81 [m sec^-1 sec^-1]")]

# %%
# Fixed Support

fv1 = DataModel.GeoData.Assemblies[0].Parts[1].Bodies[0].Vertices[0]
fv2 = DataModel.GeoData.Assemblies[0].Parts[1].Bodies[1].Vertices[0]
fv3 = DataModel.GeoData.Assemblies[0].Parts[1].Bodies[2].Vertices[0]
fv4 = DataModel.GeoData.Assemblies[0].Parts[1].Bodies[3].Vertices[0]

fvert = sel_manager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
fvert.Entities = [fv1, fv2, fv3, fv4]
FIXED_SUPPORT = MODAL_ACST.AddFixedSupport()
FIXED_SUPPORT.Location = fvert

MODAL_ACST.Activate()
Graphics.ExportImage(os.path.join(cwd, "geometry.png"), image_export_format, settings_720p)
display_image("geometry.png")

# %%
# Add results
# ~~~~~~~~~~~
# Add 10 modes

soln = Model.Analyses[0].Solution
TOT_DEF1 = soln.AddTotalDeformation()
TOT_DEF2 = soln.AddTotalDeformation()
TOT_DEF2.Mode = 2
TOT_DEF3 = soln.AddTotalDeformation()
TOT_DEF3.Mode = 3
TOT_DEF4 = soln.AddTotalDeformation()
TOT_DEF4.Mode = 4
TOT_DEF5 = soln.AddTotalDeformation()
TOT_DEF5.Mode = 5
TOT_DEF6 = soln.AddTotalDeformation()
TOT_DEF6.Mode = 6
TOT_DEF7 = soln.AddTotalDeformation()
TOT_DEF7.Mode = 7
TOT_DEF8 = soln.AddTotalDeformation()
TOT_DEF8.Mode = 8
TOT_DEF9 = soln.AddTotalDeformation()
TOT_DEF9.Mode = 9
TOT_DEF10 = soln.AddTotalDeformation()
TOT_DEF10.Mode = 10

# %%
# Add acoustic pressure

ACOUST_PRES_RES = soln.AddAcousticPressureResult()

# %%
# Add force reaction scoped to fixed Support

FORCE_REACT1 = soln.AddForceReaction()
FORCE_REACT1.BoundaryConditionSelection = FIXED_SUPPORT

# %%
# Solve
# ~~~~~

soln.Solve(True)

# sphinx_gallery_start_ignore
assert str(soln.Status) == "Done", "Solution status is not 'Done'"
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
# Total deformation - mode 1

Tree.Activate([TOT_DEF1])
Graphics.Camera.SetFit()
Graphics.ExportImage(os.path.join(cwd, "totaldeformation1.png"), image_export_format, settings_720p)
display_image("totaldeformation1.png")


# %%
# Acoustic pressure

Tree.Activate([ACOUST_PRES_RES])
Graphics.ExportImage(os.path.join(cwd, "acoustic_pressure.png"), image_export_format, settings_720p)
display_image("acoustic_pressure.png")


# %%
# Display all modal frequency, force reaction
# and acoustic pressure values

FREQ1 = TOT_DEF1.ReportedFrequency.Value
FREQ2 = TOT_DEF2.ReportedFrequency.Value
FREQ3 = TOT_DEF3.ReportedFrequency.Value
FREQ4 = TOT_DEF4.ReportedFrequency.Value
FREQ5 = TOT_DEF5.ReportedFrequency.Value
FREQ6 = TOT_DEF6.ReportedFrequency.Value
FREQ7 = TOT_DEF7.ReportedFrequency.Value
FREQ8 = TOT_DEF8.ReportedFrequency.Value
FREQ9 = TOT_DEF9.ReportedFrequency.Value
FREQ10 = TOT_DEF10.ReportedFrequency.Value

PRMAX = ACOUST_PRES_RES.Maximum.Value
PRMIN = ACOUST_PRES_RES.Minimum.Value

FRC1_X = FORCE_REACT1.XAxis.Value
FRC1_Z = FORCE_REACT1.ZAxis.Value

print("Modal Acoustic Results")
print("----------------------")
print("Frequency for mode 1 : ", FREQ1)
print("Frequency for mode 2 : ", FREQ2)
print("Frequency for mode 3 : ", FREQ3)
print("Frequency for mode 4 : ", FREQ4)
print("Frequency for mode 5 : ", FREQ5)
print("Frequency for mode 6 : ", FREQ6)
print("Frequency for mode 7 : ", FREQ7)
print("Frequency for mode 8 : ", FREQ8)
print("Frequency for mode 9 : ", FREQ9)
print("Frequency for mode 10 : ", FREQ10)
print("Acoustic pressure minimum : ", PRMIN)
print("Acoustic pressure Maximum : ", PRMAX)
print("Force reaction x-axis : ", FRC1_X)
print("Force reaction z-axis : ", FRC1_Z)

# %%
# Total deformation animation for mode 10

animation_export_format = Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat.GIF
settings_720p = Ansys.Mechanical.Graphics.AnimationExportSettings()
settings_720p.Width = 1280
settings_720p.Height = 720

TOT_DEF10.ExportAnimation(
    os.path.join(cwd, "deformation_10.gif"), animation_export_format, settings_720p
)
gif = Image.open(os.path.join(cwd, "deformation_10.gif"))
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
# Project tree
# ~~~~~~~~~~~~

app.print_tree()

# %%
# Cleanup
# ~~~~~~~
# Save project

app.save(os.path.join(cwd, "modal_acoustics.mechdat"))
app.new()

# %%
# Delete example file

delete_downloads()
