""".. _ref_example_03_show_object_properties:

Details View properties of an object
---------------------------------------

In this example, using the support files, you will display the properties that you would see in the
Details View of the object.

"""

###############################################################################
# Example Setup
# -------------
# When you run this workflow, the required file will be downloaded.
#
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Download the mechdat file.

import os

from ansys.mechanical.core import launch_mechanical
from ansys.mechanical.core.examples import download_file

mechdat_path = download_file("example_03_simple_bolt_new.mechdat", "pymechanical", "00_basic")
print(f"Downloaded the mechdat file at : {mechdat_path}")

###############################################################################
# Launch Mechanical
# ~~~~~~~~~~~~~~~~~
# Launch a new Mechanical Session in batch. 'cleanup_on_exit' set to False,
# you need to call mechanical.exit to close Mechanical.

mechanical = launch_mechanical(batch=True, cleanup_on_exit=False)
print(mechanical)

###############################################################################
# Initialize the variable needed for this workflow
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the mechdat_path for later user.
# Make this variable compatible for windows/linux/container.

project_directory = mechanical.project_directory
print(f"project directory = {project_directory}")

# upload the file to the project directory
mechanical.upload(file_name=mechdat_path, file_location_destination=project_directory)

# build the path relative to project directory
base_name = os.path.basename(mechdat_path)
combined_path = os.path.join(project_directory, base_name)
mechdat_path_modified = combined_path.replace("\\", "\\\\")
mechanical.run_python_script(f"mechdat_path='{mechdat_path_modified}'")

# verify the path
result = mechanical.run_python_script(f"mechdat_path")
print(f"mechdat_path on the server: {result}")

###################################################################################
# Execute the Mechanical script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script to display the properties and their current values for the analysis object.

result = mechanical.run_python_script(
    """
import json

ExtAPI.DataModel.Project.Open(mechdat_path)

analysisSettings = Model.Analyses[0].AnalysisSettings
props = {}
if hasattr(analysisSettings,'VisibleProperties') != False:
    for prop in analysisSettings.VisibleProperties:
        props[prop.Caption] = prop.StringValue

json.dumps(props, indent=1)
"""
)
print(f"AnalysisSettings properties:\n{result}")

###################################################################################
# Don't save the project
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clear Mechanical data.

mechanical.clear()

###########################################################
# Close Mechanical
# ~~~~~~~~~~~~~~~~
# # Close the Mechanical instance.

mechanical.exit()
