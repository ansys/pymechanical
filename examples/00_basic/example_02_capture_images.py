""".. _ref_example_02_capture_images:

Capture Images after Solve
-------------------------------

In this example, using the support files, resume a mechdat file and capture the images of all
the results into a folder on disk.

"""

###############################################################################
# Example Setup
# -------------
# When you run this workflow, the required files will be downloaded.
#
# Perform required downloads.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Download the mechdat and the script files.

import tempfile

from ansys.mechanical.core import launch_mechanical
from ansys.mechanical.core.examples import download_file

mechdat_path = download_file("example_03_simple_bolt_new.mechdat", "pymechanical", "00_basic")
print(f"Downloaded the mechdat file at : {mechdat_path}")

script_file_path = download_file("example_02_capture_images_helper.py", "pymechanical", "00_basic")
print(f"Downloaded the script file at : {script_file_path}")

###############################################################################
# Launch Mechanical
# ~~~~~~~~~~~~~~~~~
# Launch a new Mechanical Session in batch. 'cleanup_on_exit' set to False,
# you need to call mechanical.exit to close Mechanical.

mechanical = launch_mechanical(batch=True, cleanup_on_exit=False)
print(mechanical)

###############################################################################
# Initialize the variables needed for this workflow
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the mechdat_path and image_dir for later user.
# Make these variables compatible on both windows and linux.

mechdat_path_modified = mechdat_path.replace("\\", "\\\\")
mechanical.run_python_script(f"mechdat_path='{mechdat_path_modified}'")
result = mechanical.run_python_script(f"mechdat_path")
print(result)

image_dir = tempfile.gettempdir()
image_dir_modified = image_dir.replace("\\", "\\\\")
mechanical.run_python_script(f"image_dir='{image_dir_modified}'")
result = mechanical.run_python_script(f"image_dir")
print(f"Images will be stored at: {result}")

###################################################################################
# Execute the Mechanical script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script file and create the images.

mechanical.run_python_script_from_file(script_file_path)

###################################################################################
# Don't save the project
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clear Mechanical data.

mechanical.clear()

###########################################################
# Close Mechanical
# ~~~~~~~~~~~~~~~~
# Close the Mechanical instance.

mechanical.exit()
