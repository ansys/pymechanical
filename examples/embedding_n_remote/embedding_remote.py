""" .. _ref_embedding_remote:

Embedding & Remote Example
--------------------------
The code below illustrates the same example, first demonstrated using an embedded instance, and later demonstrated using a remote session.

"""

###############################################################################
# -----------------
# Embedded Instance
# -----------------

###############################################################################
# Launch Embedding Instance
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Launch a new embedding instance for Ansys Mechanical version 232.
# Starts a non-graphical Mechanical session within the python.exe, and
# updates global variables to get access to the same variables (Model, DataModel, etc.)
# as in the Mechanical scripting console​.

import os
import ansys.mechanical.core as mech
from ansys.mechanical.core.examples import download_file

app = mech.App(version=232) 
globals().update(mech.global_variables(app))
print(app)

###############################################################################
# Add Static Analysis
# ~~~~~~~~~~~~~~~~~~~
# Add static analysis to the Model.

analysis = Model.AddStaticStructuralAnalysis()

###############################################################################
# Download Valve.pmdb file
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Set working directory to project location and download Valve.pmdb to that location.

work_dir = app.ExtAPI.DataModel.Project.ProjectDirectory # os.getcwd()

filename = download_file("Valve.pmdb", "pymechanical", "embedding", destination=work_dir)
print(filename)

###############################################################################
# Import geometry
# ~~~~~~~~~~~~~~~

geometry_file = os.path.join(work_dir,'Valve.pmdb')
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessNamedSelections = True
geometry_import.Import(geometry_file, geometry_import_format, geometry_import_preferences)

# Assign material
# To import materials library: method 1
#import sys
#path_to_232_lib = os.path.join(path_to_232,'Addins\ACT\libraries\Mechanical')
#sys.path.append(path_to_232_lib)
#import materials

# To import materials library: method 2
#material_file = get_material_file().replace("\\", "\\\\")
#script = 'DS.Tree.Projects.Item(1).LoadEngrDataLibraryFromFile("' + material_file + '");'
#ExtAPI.Application.ScriptByName('jscript').ExecuteCommand(script)
#import materials

###############################################################################
# Assign material
# ~~~~~~~~~~~~~~~

matAssignment = Model.Materials.AddMaterialAssignment()
tempSel = ExtAPI.SelectionManager.CreateSelectionInfo(Ansys.ACT.Interfaces.Common.SelectionTypeEnum.GeometryEntities)
bodies = [body for body in ExtAPI.DataModel.Project.Model.Geometry.GetChildren(Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Body,True)]
geobodies = [body.GetGeoBody() for body in bodies]
ids = System.Collections.Generic.List[System.Int32]()
[ids.Add(item.Id) for item in geobodies]
tempSel.Ids = ids
matAssignment.Location = tempSel
matAssignment.Material = "Structural Steel"

###############################################################################
# Define mesh settings
# ~~~~~~~~~~~~~~~~~~~~

mesh = Model.Mesh
mesh.ElementSize = Quantity('25 [mm]')
mesh.GenerateMesh()

###############################################################################
# Define boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~

fixedSupport = analysis.AddFixedSupport()
fixedSupport.Location = ExtAPI.DataModel.GetObjectsByName("NSFixedSupportFaces")[0]

frictionlessSupport = analysis.AddFrictionlessSupport()
frictionlessSupport.Location = ExtAPI.DataModel.GetObjectsByName("NSFrictionlessSupportFaces")[0]

pressure = analysis.AddPressure()
pressure.Location = ExtAPI.DataModel.GetObjectsByName("NSInsideFaces")[0]

inputs_quantities = [Quantity("0 [s]"), Quantity("1 [s]")]  
output_quantities = [Quantity("0 [Pa]"), Quantity("15 [MPa]")]  

inputs_quantities_2 = System.Collections.Generic.List[Ansys.Core.Units.Quantity]()
[inputs_quantities_2.Add(item) for item in inputs_quantities]

output_quantities_2 = System.Collections.Generic.List[Ansys.Core.Units.Quantity]()
[output_quantities_2.Add(item) for item in output_quantities]

pressure.Magnitude.Inputs[0].DiscreteValues = inputs_quantities_2
pressure.Magnitude.Output.DiscreteValues = output_quantities_2

###############################################################################
# Solve model
# ~~~~~~~~~~~

Model.Solve()

###############################################################################
# Add results
# ~~~~~~~~~~~

solution = analysis.Solution
solution.AddTotalDeformation()
solution.AddEquivalentStress()
solution.EvaluateAllResults()

###############################################################################
# Export result values to a text file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

fileExtension=r".txt"
results =  solution.GetChildren(Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Result,True)
for result in results:
    fileName = str(result.Name)
    path = os.path.join(work_dir,fileName+fileExtension)
    result.ExportToTextFile(True,path)

###############################################################################
# Save model
# ~~~~~~~~~~

app.save(os.path.join(work_dir,'file.mechdat')) 
app.close()
# exit()



###############################################################################
# --------------
# Remote Session
# --------------

###############################################################################
#
# Launch Mechanical
# ~~~~~~~~~~~~~~~~~
# Launch a new Mechanical session in batch, setting ``cleanup_on_exit`` to
# ``False``. To close this Mechanical session when finished, this example
# must call  the ``mechanical.exit()`` method.

import os
from ansys.mechanical.core import launch_mechanical

# Launch mechanical
mechanical = launch_mechanical(batch=True, loglevel="DEBUG")
print(mechanical)


###############################################################################
# Download required files
# ~~~~~~~~~~~~~~~~~~~~~~~
# Download the required files. Print the file path for the geometry file.

# Check working directory
server_project_directory = mechanical.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")
print(server_project_directory)

# Download the Valve.pmdb file
filename = download_file("Valve.pmdb", "pymechanical", "embedding", destination=server_project_directory)
print(filename)


###############################################################################
# Run mech_script.py
# ~~~~~~~~~~~~~~~~~~
# Run mech_script.py in the current working directory.

# Set work_dir 
work_dir = os.getcwd()
# Have to move mech_script.py into example-data github

# Run mechanical automation script
mechanical_script = os.path.join(work_dir,'mech_script.py')
print(mechanical_script)
# result = mechanical.run_python_script_from_file(mechanical_script, enable_logging=True, log_level="DEBUG", progress_interval=1000)


###############################################################################
# Get list of generated files
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Print each file in the list of generated files.

# # Get list of generated files
# list_files = mechanical.list_files()
# for file in list_files:
#     print(file)


###############################################################################
# Download files to local working directory.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Download files back to local working directory.

# dest_dir = "download"
# dest_dir = os.path.join(work_dir, dest_dir)
# for file in list_files:
#     downloaded = mechanical.download(file, target_dir=dest_dir)


###############################################################################
# Exit remote session
# ~~~~~~~~~~~~~~~~~~~
# Leave the active remote session.

# # Exit remote session
# mechanical.exit(force=True)
