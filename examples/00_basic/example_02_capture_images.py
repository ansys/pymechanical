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

import os

from matplotlib import image as mpimg
from matplotlib import pyplot as plt

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
# Initialize the variable needed for opening the mechdat
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
# Open the mechdat file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script to open the mechadat file.

mechanical.run_python_script("ExtAPI.DataModel.Project.Open(mechdat_path)")

###################################################################################
# Initialize the variable needed for the image directory
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the image_dir for later user.
# Make this variable compatible for windows/linux/container.

# opening the mechdat file changes the project directory
project_directory = mechanical.project_directory
print(f"project directory = {project_directory}")

image_directory_modified = project_directory.replace("\\", "\\\\")
mechanical.run_python_script(f"image_dir='{image_directory_modified}'")

# verify the path
result = mechanical.run_python_script(f"image_dir")
print(f"Images will be stored on the server at: {result}")

###################################################################################
# Execute the Mechanical script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script file and create the images.

mechanical.run_python_script_from_file(script_file_path)


###############################################################################
# Download the image and plot
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Download one image file from the server to the current working directory and plot
# using matplotlib.
def get_image_path(image_name):
    return image_directory_modified + image_name


def display_image(path):
    print(f"Printing {path} using matplotlib")
    image1 = mpimg.imread(path)
    plt.figure(figsize=(15, 15))
    plt.axis("off")
    plt.imshow(image1)
    plt.show()


image_name = "Total Deformation @ 1 sec_Right.png"
image_path_server = get_image_path(image_name)

if image_path_server != "":
    current_working_directory = os.getcwd()

    mechanical.download(image_path_server, target_dir=current_working_directory)
    image_local_path = os.path.join(current_working_directory, image_name)

    display_image(image_local_path)

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
