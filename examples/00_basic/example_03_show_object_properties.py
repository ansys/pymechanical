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
# Make this variable compatible on both windows and linux.

mechdat_path_modified = mechdat_path.replace("\\", "\\\\")
mechanical.run_python_script(f"mechdat_path='{mechdat_path_modified}'")
result = mechanical.run_python_script(f"mechdat_path")
print(result)

###################################################################################
# Execute the Mechanical script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script to display the properties and their current values for the analysis object.

output = mechanical.run_python_script(
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
print(output)

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
