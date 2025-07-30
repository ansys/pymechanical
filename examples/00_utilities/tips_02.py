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

""".. _ref_tips_02:

Export image
------------

The following example demonstrates how to export an image of the imported geometry
and display it using matplotlib.
"""

# %%
# Import the necessary libraries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from pathlib import Path

from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

# %%
# Initialize the embedded application
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Create an instance of the App class
app = App(globals=globals())

# Print the app to ensure it is working
print(app)

# %%
# Download and import the geometry file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# %%
# Download the geometry file
geometry_path = download_file("Valve.pmdb", "pymechanical", "embedding")

# %%
# Import the geometry file

geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import.Import(geometry_path)

# %%
# Configure graphics for image export
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Set the orientation of the camera
ExtAPI.Graphics.Camera.SetSpecificViewOrientation(ViewOrientationType.Iso)

# Set the image export format
image_export_format = GraphicsImageExportFormat.PNG

# Configure the export settings for the image
settings_720p = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
settings_720p.Resolution = GraphicsResolutionType.EnhancedResolution
settings_720p.Background = GraphicsBackgroundType.White
settings_720p.Width = 1280
settings_720p.Height = 720
settings_720p.CurrentGraphicsDisplay = False

# Rotate the geometry on the Y-axis
Graphics.Camera.Rotate(180, CameraAxisType.ScreenY)

# %%
# Create a function to display the image
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from matplotlib import image as mpimg
from matplotlib import pyplot as plt

# Directory to save the image
output_path = Path.cwd() / "out"


def display_image(image_name) -> None:
    """Display the image using matplotlib.

    Parameters
    ----------
    image_name : str
        The name of the image file to display.
    """
    # Create the full path to the image
    image_path = output_path / image_name

    # Plot the figure and display the image
    plt.figure(figsize=(16, 9))
    plt.imshow(mpimg.imread(str(image_path)))
    plt.xticks([])
    plt.yticks([])
    plt.axis("off")
    plt.show()


# %%
# Export and display the image
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Fit the geometry in the viewing area
Graphics.Camera.SetFit()

# Export the image
geometry_image = output_path / "geometry.png"
Graphics.ExportImage(str(geometry_image), image_export_format, settings_720p)

# Display the image
display_image(geometry_image.name)

# %%
# Clean up the downloaded files and app
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Delete the downloaded files
delete_downloads()

# Close the app
app.close()
