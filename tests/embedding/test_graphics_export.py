# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

"""Graphics export tests"""

import os

import pytest

try:
    from ansys.mechanical.core import global_variables
except:
    # No embedding - this import breaks test collection
    global_variables = {}

from ansys.mechanical.core.examples import delete_downloads, download_file


@pytest.mark.embedding
@pytest.mark.parametrize("image_formats", ["PNG", "JPG", "BMP"])
def test_image_export(printer, embedded_app, image_formats):
    """Tests to check image export."""
    printer(f"{image_formats} export")
    globals().update(global_variables(embedded_app, True))
    mechdb_file = download_file("graphics_test.mechdb", "pymechanical", "test_files")
    embedded_app.open(mechdb_file)
    image_settings = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
    image_format = getattr(
        Ansys.Mechanical.DataModel.Enums.GraphicsImageExportFormat, image_formats
    )
    image_settings.Resolution = GraphicsResolutionType.EnhancedResolution
    image_settings.Background = GraphicsBackgroundType.White
    image_settings.Width = 1280
    image_settings.Height = 720

    STAT_STRUC = Model.Analyses[0]
    STAT_STRUC_SOLN = STAT_STRUC.Solution
    DEF = STAT_STRUC_SOLN.Children[1]
    Tree.Activate([DEF])
    ExtAPI.Graphics.Camera.SetFit()
    image_file = os.path.join(os.getcwd(), f"image.{image_format}")
    ExtAPI.Graphics.ExportImage(image_file, image_format, image_settings)
    with open(image_file, "rb") as file:
        try:
            file.read()
        except Exception as e:
            assert False, f"Failed to read file {image_file}: {e}"
    os.remove(image_file)
    delete_downloads()


@pytest.mark.embedding
@pytest.mark.parametrize("animation_formats", ["GIF", "AVI", "MP4", "WMV"])
def test_animation_export(printer, embedded_app, animation_formats):
    """Tests to check animation export."""
    printer(f"{animation_formats} export")
    globals().update(global_variables(embedded_app, True))
    mechdb_file = download_file("graphics_test.mechdb", "pymechanical", "test_files")
    embedded_app.open(mechdb_file)
    animation_settings = Ansys.Mechanical.Graphics.AnimationExportSettings()
    animation_format = getattr(
        Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat, animation_formats
    )
    animation_settings.Width = 1280
    animation_settings.Height = 720

    STAT_STRUC = Model.Analyses[0]
    STAT_STRUC_SOLN = STAT_STRUC.Solution
    DEF = STAT_STRUC_SOLN.Children[1]
    Tree.Activate([DEF])
    ExtAPI.Graphics.Camera.SetFit()
    animation_file = os.path.join(os.getcwd(), f"animation.{animation_format}")
    DEF.ExportAnimation(animation_file, animation_format, animation_settings)
    with open(animation_file, "rb") as file:
        try:
            file.read()
        except Exception as e:
            assert False, f"Failed to read file {animation_file}: {e}"
    os.remove(animation_file)
    delete_downloads()
