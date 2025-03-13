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

Export image and display
"""

# %%
# Import necessary libraries
# ~~~~~~~~~~~~~~~~~~~~~~~~~~

import os

from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

# %%
# Embed Mechanical and set global variables

app = App()
app.update_globals(globals())
print(app)


# %%
# Download and import geometry
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Download geometry

geometry_path = download_file("Valve.pmdb", "pymechanical", "embedding")

# %%
# Import geometry

geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import.Import(geometry_path)

# %%
# Configure graphics for image export
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Orientation
Graphics.Camera.SetSpecificViewOrientation(ViewOrientationType.Iso)

# Export format
image_export_format = GraphicsImageExportFormat.PNG

# Resolution and background
settings_720p = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
settings_720p.Resolution = GraphicsResolutionType.EnhancedResolution
settings_720p.Background = GraphicsBackgroundType.White
settings_720p.Width = 1280
settings_720p.Height = 720
settings_720p.CurrentGraphicsDisplay = False

# Rotate the geometry if needed
ExtAPI.Graphics.Camera.Rotate(180, CameraAxisType.ScreenY)


# %%
# Custom function for displaying the image
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from matplotlib import image as mpimg
from matplotlib import pyplot as plt

# Temporary directory to save the image
cwd = os.path.join(os.getcwd(), "out")


def display_image(image_name):
    plt.figure(figsize=(16, 9))
    plt.imshow(mpimg.imread(os.path.join(cwd, image_name)))
    plt.xticks([])
    plt.yticks([])
    plt.axis("off")
    plt.show()


# %%
# Export and display the image
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Fits the geometry in the viewing area
Graphics.Camera.SetFit()

Graphics.ExportImage(os.path.join(cwd, "geometry.png"), image_export_format, settings_720p)

# Display the image using matplotlib
display_image("geometry.png")

# %%
# Cleanup
# ~~~~~~~

delete_downloads()
app.new()
