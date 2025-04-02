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
image_export_format = GraphicsImageExportFormat.PNG
settings_720p = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
settings_720p.Resolution = GraphicsResolutionType.EnhancedResolution
settings_720p.Background = GraphicsBackgroundType.White
settings_720p.Width = 1280
settings_720p.Height = 720
settings_720p.CurrentGraphicsDisplay = False
Graphics.Camera.Rotate(180, CameraAxisType.ScreenY)

# %%
# Download geometry and materials files
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

geometry_path = download_file("C_GEOMETRY.agdb", "pymechanical", "embedding")
mat_path = download_file("Air-material.xml", "pymechanical", "embedding")

# %%
# Import the geometry
# ~~~~~~~~~~~~~~~~~~~

geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessNamedSelections = True
geometry_import.Import(geometry_path, geometry_import_format, geometry_import_preferences)


GEOM = Model.Geometry

solid1 = GEOM.Children[0]
solid2 = GEOM.Children[1]
solid3 = GEOM.Children[2]
solid4 = GEOM.Children[3]
solid5 = GEOM.Children[4]
solid6 = GEOM.Children[5]
solid7 = GEOM.Children[6]
solid8 = GEOM.Children[7]
solid9 = GEOM.Children[8]
solid10 = GEOM.Children[9]
solid11 = GEOM.Children[10]

solid1.Suppressed = True
solid2.Suppressed = True
solid3.Suppressed = True
solid4.Suppressed = True
solid5.Suppressed = True
solid7.Suppressed = True
solid10.Suppressed = True
solid11.Suppressed = True


app.plot()

# %%
# Store all Variables necessary for analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MESH = Model.Mesh
NS = Model.NamedSelections
CONN = Model.Connections
CS = Model.CoordinateSystems
MAT = Model.Materials

# %%
# Setup the Analysis
# ~~~~~~~~~~~~~~~~~~
# Add harmonic acoustics and unit system

Model.AddHarmonicAcousticAnalysis()
ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardMKS

# %%
# Import and assign materials

MAT.Import(mat_path)
solid6.Material = "Air"
solid8.Material = "Air"
solid9.Material = "Air"

# %%
# Create coordinate system
LCS1 = CS.AddCoordinateSystem()
LCS1.OriginX = Quantity("0 [mm]")
LCS1.OriginY = Quantity("0 [mm]")
LCS1.OriginZ = Quantity("0 [mm]")
LCS1.PrimaryAxisDefineBy = CoordinateSystemAlignmentType.GlobalZ

# %%
# Generate mesh

MESH.ElementSize = Quantity("200 [mm]")
MESH.GenerateMesh()


# %%
# Create named selections
# ~~~~~~~~~~~~~~~~~~~~~~~~

SF_Velo = Model.AddNamedSelection()
SF_Velo.ScopingMethod = GeometryDefineByType.Worksheet
SF_Velo.Name = "SF_Velo"
GEN_CRT1 = SF_Velo.GenerationCriteria
CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT1.Active = True
CRT1.Action = SelectionActionType.Add
CRT1.EntityType = SelectionType.GeoFace
CRT1.Criterion = SelectionCriterionType.Size
CRT1.Operator = SelectionOperatorType.Equal
CRT1.Value = Quantity("3e6 [mm^2]")
GEN_CRT1.Add(CRT1)
CRT2 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT2.Active = True
CRT2.Action = SelectionActionType.Filter
CRT2.EntityType = SelectionType.GeoFace
CRT2.Criterion = SelectionCriterionType.LocationZ
CRT2.Operator = SelectionOperatorType.Equal
CRT2.Value = Quantity("15000 [mm]")
GEN_CRT1.Add(CRT2)
SF_Velo.Activate()
SF_Velo.Generate()

ABS_Face = Model.AddNamedSelection()
ABS_Face.ScopingMethod = GeometryDefineByType.Worksheet
ABS_Face.Name = "ABS_Face"
GEN_CRT2 = ABS_Face.GenerationCriteria
CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT1.Active = True
CRT1.Action = SelectionActionType.Add
CRT1.EntityType = SelectionType.GeoFace
CRT1.Criterion = SelectionCriterionType.Size
CRT1.Operator = SelectionOperatorType.Equal
CRT1.Value = Quantity("1.5e6 [mm^2]")
GEN_CRT2.Add(CRT1)
CRT2 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT2.Active = True
CRT2.Action = SelectionActionType.Filter
CRT2.EntityType = SelectionType.GeoFace
CRT2.Criterion = SelectionCriterionType.LocationY
CRT2.Operator = SelectionOperatorType.Equal
CRT2.Value = Quantity("500 [mm]")
GEN_CRT2.Add(CRT2)
ABS_Face.Activate()
ABS_Face.Generate()

PRES_Face = Model.AddNamedSelection()
PRES_Face.ScopingMethod = GeometryDefineByType.Worksheet
PRES_Face.Name = "PRES_Face"
GEN_CRT3 = PRES_Face.GenerationCriteria
CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT1.Active = True
CRT1.Action = SelectionActionType.Add
CRT1.EntityType = SelectionType.GeoFace
CRT1.Criterion = SelectionCriterionType.Size
CRT1.Operator = SelectionOperatorType.Equal
CRT1.Value = Quantity("1.5e6 [mm^2]")
GEN_CRT3.Add(CRT1)
CRT2 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT2.Active = True
CRT2.Action = SelectionActionType.Filter
CRT2.EntityType = SelectionType.GeoFace
CRT2.Criterion = SelectionCriterionType.LocationY
CRT2.Operator = SelectionOperatorType.Equal
CRT2.Value = Quantity("4500 [mm]")
GEN_CRT3.Add(CRT2)
PRES_Face.Activate()
PRES_Face.Generate()

ACOUSTIC_Region = Model.AddNamedSelection()
ACOUSTIC_Region.ScopingMethod = GeometryDefineByType.Worksheet
ACOUSTIC_Region.Name = "ACOUSTIC_Region"
GEN_CRT4 = ACOUSTIC_Region.GenerationCriteria
CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
CRT1.Active = True
CRT1.Action = SelectionActionType.Add
CRT1.EntityType = SelectionType.GeoBody
CRT1.Criterion = SelectionCriterionType.Type
CRT1.Operator = SelectionOperatorType.Equal
CRT1.Value = 8
GEN_CRT4.Add(CRT1)
ACOUSTIC_Region.Activate()
ACOUSTIC_Region.Generate()

# %%
# Analysis settings
# ~~~~~~~~~~~~~~~~~

ANALYSIS_SETTINGS = Model.Analyses[0].AnalysisSettings
ANALYSIS_SETTINGS.RangeMaximum = Quantity("100 [Hz]")
ANALYSIS_SETTINGS.SolutionIntervals = 50
ANALYSIS_SETTINGS.CalculateVelocity = True
ANALYSIS_SETTINGS.CalculateEnergy = True
ANALYSIS_SETTINGS.CalculateVolumeEnergy = True

# %%
# Boundary conditions and load
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HARM_ACOUST = Model.Analyses[0]

# %%
# Acoustic region

Acoustic_region = [x for x in HARM_ACOUST.Children if x.Name == "Acoustics Region"][0]
Acoustic_region.Location = ACOUSTIC_Region

# %%
# Surface velocity

SURF_VEL = HARM_ACOUST.AddAcousticSurfaceVelocity()
SURF_VEL.Location = SF_Velo
SURF_VEL.Magnitude.Output.DiscreteValues = [Quantity("5000 [mm s-1]")]

# %%
# Acoustic pressure

ACOUST_PRES = HARM_ACOUST.AddAcousticPressure()
ACOUST_PRES.Location = PRES_Face
ACOUST_PRES.Magnitude = Quantity("1.5e-7 [MPa]")

# %%
# Acoustic absoption surface

ABSORP_SURF = HARM_ACOUST.AddAcousticAbsorptionSurface()
ABSORP_SURF.Location = ABS_Face
ABSORP_SURF.AbsorptionCoefficient.Output.DiscreteValues = [Quantity("0.02")]

HARM_ACOUST.Activate()
Graphics.Camera.SetFit()
Graphics.ExportImage(
    os.path.join(cwd, "bounday_conditions.png"), image_export_format, settings_720p
)
display_image("bounday_conditions.png")

# %%
# Add results
# ~~~~~~~~~~~

SOLN = Model.Analyses[0].Solution

# %%
# Acoustic pressure

ACOUST_PRES_RES1 = SOLN.AddAcousticPressureResult()
ACOUST_PRES_RES1.By = SetDriverStyle.ResultSet
ACOUST_PRES_RES1.SetNumber = 25

# %%
# Acoustic velocity - total and directional

ACOUST_TOT_VEL1 = SOLN.AddAcousticTotalVelocityResult()
ACOUST_TOT_VEL1.Frequency = Quantity("50 [Hz]")

ACOUST_DIR_VEL1 = SOLN.AddAcousticDirectionalVelocityResult()
ACOUST_DIR_VEL1.Frequency = Quantity("50 [Hz]")
ACOUST_DIR_VEL1.CoordinateSystem = LCS1

ACOUST_DIR_VEL2 = SOLN.AddAcousticDirectionalVelocityResult()
ACOUST_DIR_VEL2.NormalOrientation = NormalOrientationType.ZAxis
ACOUST_DIR_VEL2.By = SetDriverStyle.ResultSet
ACOUST_DIR_VEL2.SetNumber = 25

# %%
# Acoustic sound pressure and frequency bands

ACOUST_SPL = SOLN.AddAcousticSoundPressureLevel()
ACOUST_SPL.Frequency = Quantity("50 [Hz]")

ACOUST_A_SPL = SOLN.AddAcousticAWeightedSoundPressureLevel()
ACOUST_A_SPL.Frequency = Quantity("50 [Hz]")

ACOUST_FRQ_BAND_SPL = SOLN.AddAcousticFrequencyBandSPL()

A_FREQ_BAND_SPL = SOLN.AddAcousticFrequencyBandAWeightedSPL()

Z_VELO_RESP = SOLN.AddAcousticVelocityFrequencyResponse()
Z_VELO_RESP.NormalOrientation = NormalOrientationType.ZAxis
Z_VELO_RESP.Location = PRES_Face
Z_VELO_RESP.NormalOrientation = NormalOrientationType.ZAxis

# %%
# Acoustic kinetic  and potentional energy frequency response

KE_RESP = SOLN.AddAcousticKineticEnergyFrequencyResponse()
KE_RESP.Location = ABS_Face
KE_display = KE_RESP.TimeHistoryDisplay

PE_RESP = SOLN.AddAcousticPotentialEnergyFrequencyResponse()
PE_RESP.Location = ABS_Face
PE_display = PE_RESP.TimeHistoryDisplay

# %%
# Acoustic total and directional velocity

ACOUST_TOT_VEL2 = SOLN.AddAcousticTotalVelocityResult()
ACOUST_TOT_VEL2.Location = PRES_Face
ACOUST_TOT_VEL2.Frequency = Quantity("30 [Hz]")
ACOUST_TOT_VEL2.Amplitude = True

ACOUST_DIR_VEL3 = SOLN.AddAcousticDirectionalVelocityResult()
ACOUST_DIR_VEL3.NormalOrientation = NormalOrientationType.ZAxis
ACOUST_DIR_VEL3.Location = PRES_Face
ACOUST_DIR_VEL3.Frequency = Quantity("10 [Hz]")
ACOUST_DIR_VEL3.Amplitude = True

ACOUST_KE = SOLN.AddAcousticKineticEnergy()
ACOUST_KE.Location = ABS_Face
ACOUST_KE.Frequency = Quantity("68 [Hz]")
ACOUST_KE.Amplitude = True

ACOUST_PE = SOLN.AddAcousticPotentialEnergy()
ACOUST_PE.Location = ABS_Face
ACOUST_PE.Frequency = Quantity("10 [Hz]")
ACOUST_PE.Amplitude = True

# %%
# Solve
# ~~~~~

SOLN.Solve(True)

# sphinx_gallery_start_ignore
assert str(SOLN.Status) == "Done", "Solution status is not 'Done'"
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
# Postprocessing
# ~~~~~~~~~~~~~~

# %%
# Total acoustic pressure
# ^^^^^^^^^^^^^^^^^^^^^^^

Tree.Activate([ACOUST_PRES_RES1])
Graphics.ExportImage(os.path.join(cwd, "acou_pressure.png"), image_export_format, settings_720p)
display_image("acou_pressure.png")

# %%
# Total acoustic velocity
# ^^^^^^^^^^^^^^^^^^^^^^^

Tree.Activate([ACOUST_PRES_RES1])
Graphics.ExportImage(os.path.join(cwd, "totalvelocity.png"), image_export_format, settings_720p)
display_image("totalvelocity.png")

# %%
# Sound pressure level
# ^^^^^^^^^^^^^^^^^^^^

Tree.Activate([ACOUST_SPL])
Graphics.ExportImage(os.path.join(cwd, "sound_pressure.png"), image_export_format, settings_720p)
display_image("sound_pressure.png")

# %%
# Total velocity on pressure surface
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tree.Activate([ACOUST_TOT_VEL2])
Graphics.ExportImage(
    os.path.join(cwd, "totalvelocity_pressure.png"), image_export_format, settings_720p
)
display_image("totalvelocity_pressure.png")

# %%
# Kinetic energy on absorption face
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tree.Activate([ACOUST_KE])
Graphics.ExportImage(os.path.join(cwd, "kineticenergy.png"), image_export_format, settings_720p)
display_image("kineticenergy.png")

# %%
# Total acoustic pressure animation
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

animation_export_format = Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat.GIF
settings_720p = Ansys.Mechanical.Graphics.AnimationExportSettings()
settings_720p.Width = 1280
settings_720p.Height = 720

ACOUST_PRES_RES1.ExportAnimation(
    os.path.join(cwd, "press.gif"), animation_export_format, settings_720p
)
gif = Image.open(os.path.join(cwd, "press.gif"))
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
# Display output file from solve
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def write_file_contents_to_console(path):
    """Write file contents to console."""
    with open(path, "rt") as file:
        for line in file:
            print(line, end="")


solve_path = HARM_ACOUST.WorkingDir
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

app.save(os.path.join(cwd, "harmnonic_acoustics.mechdat"))
app.new()

# delete example file
delete_downloads()
