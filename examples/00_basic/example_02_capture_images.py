""".. _ref_example_02_capture_images:

Capture images after a solve
----------------------------

Using supplied files, this example shows how to resume a MECHDAT file
and capture the images of all results in a folder on the disk.

"""

###############################################################################
# Download required files
# ~~~~~~~~~~~~~~~~~~~~~~~
# Download the required files. Print the file paths for the MECHDAT file and
# script files.

import os

from ansys.mechanical.core import launch_mechanical
from ansys.mechanical.core.examples import download_file

mechdat_path = download_file("example_03_simple_bolt_new.mechdat", "pymechanical", "00_basic")
print(f"Downloaded the MECHDAT file to: {mechdat_path}")

script_file_path = download_file("example_02_capture_images_helper.py", "pymechanical", "00_basic")
print(f"Downloaded the script files to: {script_file_path}")

###############################################################################
# Launch Mechanical
# ~~~~~~~~~~~~~~~~~
# Launch a new Mechanical session in batch, setting ``cleanup_on_exit`` to
# ``False``. To close this Mechanical session when finished, this example
# must call  the ``mechanical.exit()`` method.

mechanical = launch_mechanical(batch=True, cleanup_on_exit=False)
print(mechanical)

###############################################################################
# Initialize the variables needed for this workflow
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the paths for the MECHDATA file and image directory for later use.
# Make these variables compatible for Windows, Linux, and Docker containers.

project_directory = mechanical.project_directory
print(f"project directory = {project_directory}")

# Upload the file to the project directory.
mechanical.upload(file_name=mechdat_path, file_location_destination=project_directory)

# Build the path relative to the project directory.
base_name = os.path.basename(mechdat_path)
combined_path = os.path.join(project_directory, base_name)
mechdat_path_modified = combined_path.replace("\\", "\\\\")
mechanical.run_python_script(f"mechdat_path='{mechdat_path_modified}'")

# Verify the path for the MECHDAT file.
result = mechanical.run_python_script(f"mechdat_path")
print(f"The MECHDATA file is stored on the server at: {result}")

image_directory_modified = project_directory.replace("\\", "\\\\")
mechanical.run_python_script(f"image_dir='{image_directory_modified}'")

# Verify the path for the images directory.
result = mechanical.run_python_script(f"image_dir")
print(f"Images are stored on the server at: {result}")

###################################################################################
# Execute the script
# ~~~~~~~~~~~~~~~~~~
# Run the Mechanical script file for creating the images.

mechanical.run_python_script_from_file(script_file_path)

###################################################################################
# Clear the data
# ~~~~~~~~~~~~~~
# Clear the data so it isn't saved to the project.

mechanical.clear()

###########################################################
# Close Mechanical
# ~~~~~~~~~~~~~~~~
# Close the Mechanical instance.

mechanical.exit()
