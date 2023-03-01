""".. _ref_example_01_simple_structural_solve:

Static Structural Analysis
-------------------------------

In this example, using the support files, you will insert a Static Structural analysis into a new
Mechanical session and execute a sequence of python scripting commands that will define and
solve the analysis. The deformation results are reported back after the solution.

"""

###############################################################################
# Example Setup
# -------------
# When you run this workflow, the required file will be downloaded.
#
# Perform required download.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Download the geometry file.
import os

from ansys.mechanical.core import launch_mechanical
from ansys.mechanical.core.examples import download_file

geometry_path = download_file("example_01_geometry.agdb", "pymechanical", "00_basic")
print(f"Downloaded the geometry file at : {geometry_path}")

###############################################################################
# Launch Mechanical
# ~~~~~~~~~~~~~~~~~
# Launch a new Mechanical Session in batch. 'cleanup_on_exit' set to False,
# you need to call mechanical.exit to close Mechanical.

mechanical = launch_mechanical(batch=True, cleanup_on_exit=False)
print(mechanical)

###############################################################################
# Disable Distributed Solve
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Comment this if this is not the container scenario
script = (
    'ExtAPI.Application.SolveConfigurations["My Computer"].'
    "SolveProcessSettings.DistributeSolution = False"
)
mechanical.run_python_script(script)

###############################################################################
# Initialize the variable needed for this workflow
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the part_file_path for later user.
# Make this variable compatible for  windows/linux/container.

project_directory = mechanical.project_directory
print(f"project directory = {project_directory}")

# upload the file to the project directory
mechanical.upload(file_name=geometry_path, file_location_destination=project_directory)

# build the path relative to project directory
base_name = os.path.basename(geometry_path)
combined_path = os.path.join(project_directory, base_name)
part_file_path = combined_path.replace("\\", "\\\\")
mechanical.run_python_script(f"part_file_path='{part_file_path}'")

# verify the path
result = mechanical.run_python_script("part_file_path")
print(f"part_file_path on server: {result}")

###################################################################################
# Execute the Mechanical script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script to attach geometry, setup and solve the analysis.

output = mechanical.run_python_script(
    """
import json

geometry_import_group_11 = Model.GeometryImportGroup
geometry_import_19 = geometry_import_group_11.AddGeometryImport()

geometry_import_19_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.\
    Format.Automatic
geometry_import_19_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_19_preferences.ProcessNamedSelections = True
geometry_import_19_preferences.ProcessCoordinateSystems = True

geometry_import_19.Import(part_file_path, geometry_import_19_format, geometry_import_19_preferences)

Model.AddStaticStructuralAnalysis()
STAT_STRUC = Model.Analyses[0]
CS_GRP = Model.CoordinateSystems
ANALYSIS_SETTINGS = STAT_STRUC.Children[0]
SOLN= STAT_STRUC.Solution

# Section 2 Set up the Unit System.

ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardMKS
ExtAPI.Application.ActiveAngleUnit = AngleUnitType.Radian

# Section 3 Named Selection and Coordinate System.

NS1 = Model.NamedSelections.Children[0]
NS2 = Model.NamedSelections.Children[1]
NS3 = Model.NamedSelections.Children[2]
NS4 = Model.NamedSelections.Children[3]
GCS = CS_GRP.Children[0]
LCS1 = CS_GRP.Children[1]

# Section 4 Define remote point.

RMPT_GRP = Model.RemotePoints
RMPT_1 = RMPT_GRP.AddRemotePoint()
RMPT_1.Location = NS1
RMPT_1.XCoordinate=Quantity("7 [m]")
RMPT_1.YCoordinate=Quantity("0 [m]")
RMPT_1.ZCoordinate=Quantity("0 [m]")

#  Section 5 Define Mesh Settings.

MSH = Model.Mesh
MSH.ElementSize =Quantity("0.5 [m]")
MSH.GenerateMesh()

#  Section 6 Define boundary conditions.

# Insert FIXED Support
FIX_SUP = STAT_STRUC.AddFixedSupport()
FIX_SUP.Location = NS2

# Insert Frictionless Support
FRIC_SUP = STAT_STRUC.AddFrictionlessSupport()
FRIC_SUP.Location = NS3

#  Section 7 Define remote force.

REM_FRC1 = STAT_STRUC.AddRemoteForce()
REM_FRC1.Location = RMPT_1
REM_FRC1.DefineBy =LoadDefineBy.Components
REM_FRC1.XComponent.Output.DiscreteValues = [Quantity("1e10 [N]")]

#  Section 8 Define thermal condition.

THERM_COND = STAT_STRUC.AddThermalCondition()
THERM_COND.Location = NS4
THERM_COND.Magnitude.Output.DefinitionType=VariableDefinitionType.Formula
THERM_COND.Magnitude.Output.Formula="50*(20+z)"
THERM_COND.XYZFunctionCoordinateSystem=LCS1
THERM_COND.RangeMinimum=Quantity("-20 [m]")
THERM_COND.RangeMaximum=Quantity("1 [m]")

#  Section 9 Insert directional deformation.

DIR_DEF = STAT_STRUC.Solution.AddDirectionalDeformation()
DIR_DEF.Location = NS1
DIR_DEF.NormalOrientation =NormalOrientationType.XAxis

# Section 10 Add Total Deformation and force reaction probe

TOT_DEF = STAT_STRUC.Solution.AddTotalDeformation()

# Add Force Reaction
FRC_REAC_PROBE = STAT_STRUC.Solution.AddForceReaction()
FRC_REAC_PROBE.BoundaryConditionSelection = FIX_SUP
FRC_REAC_PROBE.ResultSelection =ProbeDisplayFilter.XAxis

# Section 11 Solve and get the results.

# Solve Static Analysis
STAT_STRUC.Solution.Solve(True)

dir_deformation_details = {
"Minimum": str(DIR_DEF.Minimum),
"Maximum": str(DIR_DEF.Maximum),
"Average": str(DIR_DEF.Average),
}

json.dumps(dir_deformation_details)
"""
)
print(output)

###########################################################
# Close Mechanical
# ~~~~~~~~~~~~~~~~
# Close the Mechanical instance.

mechanical.exit()
