# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Graphics export tests."""

from pathlib import Path

import pytest


def _is_readable(filepath: str):
    filepath = Path(filepath)
    try:
        with filepath.open("rb") as file:
            file.read()
    except Exception as e:
        assert False, f"Failed to read file {filepath}: {e}"
    finally:
        filepath.unlink(missing_ok=True)


@pytest.mark.embedding
@pytest.mark.parametrize("image_format", ["PNG", "JPG", "BMP"])
def test_graphics_export_image(printer, embedded_app, image_format, graphics_test_mechdb_file):
    """Tests to check image export."""
    printer(f"{image_format} export")
    embedded_app.update_globals(globals())
    embedded_app.open(graphics_test_mechdb_file)
    image_settings = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
    image_format = getattr(GraphicsImageExportFormat, image_format)
    image_settings.Resolution = GraphicsResolutionType.EnhancedResolution
    image_settings.Background = GraphicsBackgroundType.White
    image_settings.Width = 1280
    image_settings.Height = 720
    dir_deformation = DataModel.GetObjectsByType(DataModelObjectCategory.DeformationResult)[0]
    Tree.Activate([dir_deformation])
    ExtAPI.Graphics.Camera.SetFit()
    image_file = str(Path.cwd() / f"image.{image_format}")
    ExtAPI.Graphics.ExportImage(image_file, image_format, image_settings)
    _is_readable(image_file)


@pytest.mark.embedding
@pytest.mark.parametrize("animation_format", ["GIF", "AVI", "MP4", "WMV"])
def test_graphics_export_animation(
    printer, embedded_app, animation_format, graphics_test_mechdb_file
):
    """Tests to check animation export."""
    printer(f"{animation_format} export")
    embedded_app.update_globals(globals())
    embedded_app.open(graphics_test_mechdb_file)
    animation_settings = Ansys.Mechanical.Graphics.AnimationExportSettings()
    animation_format = getattr(GraphicsAnimationExportFormat, animation_format)
    animation_settings.Width = 1280
    animation_settings.Height = 720
    dir_deformation = DataModel.GetObjectsByType(DataModelObjectCategory.DeformationResult)[0]
    Tree.Activate([dir_deformation])
    ExtAPI.Graphics.Camera.SetFit()
    animation_file = str(Path.cwd() / f"animation.{animation_format}")
    dir_deformation.ExportAnimation(animation_file, animation_format, animation_settings)
    _is_readable(animation_file)
