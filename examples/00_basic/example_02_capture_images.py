""".. _ref_example_02_capture_images:

Capture Images after Solve
-------------------------------

In this example, using the support files, resume a mechdb file and capture images of all the results
into a folder on disk.

This example requires you to download the following Mechanical database and python file.
- SimpleBoltNew.mechdat
- capture_images.py
"""

###############################################################################
# Launch Mechanical
# ~~~~~~~~~~~~~~~~~
# Launch a new Mechanical Session in batch.
import os

from ansys.mechanical.core import launch_mechanical

mechanical = launch_mechanical(batch=True, cleanup_on_exit=False)
print(mechanical)

###################################################################################
# Set the mechdat path for the script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Execute the Mechanical script to set the mechdat path
# os.chdir(r"C:\temp\pymechtest")
# working_dir = os.getcwd()
working_dir = r"C:\temp\pymechtest"

mechdat_path = os.path.join(working_dir, "example_03_simple_bolt_new.mechdat")
mechdat_path_modified = mechdat_path.replace("\\", "\\\\")
mechanical.run_python_script(f"mechdat_path='{mechdat_path_modified}'")
result = mechanical.run_python_script(f"mechdat_path")
print(result)

###################################################################################
# Set image directory for the script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the image directory for later use

image_dir = working_dir.replace("\\", "\\\\")
mechanical.run_python_script(f"image_dir='{image_dir}'")
result = mechanical.run_python_script(f"image_dir")
print(result)

###################################################################################
# Create images
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script and create images
script_file_path = os.path.join(working_dir, "example_02_capture_images_helper.py")
mechanical.run_python_script_from_file(script_file_path)

###################################################################################
# Don't save the project
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# exit without saving the project
mechanical.clear()

###########################################################
# Close Mechanical
# ~~~~~~~~~~~~~~~~
# Close Mechanical

mechanical.exit()
