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

"""Image and animation export tests"""

import os

import pytest

try:
    from ansys.mechanical.core import global_variables
except:
    # No embedding - this import breaks test collection
    global_variables = {}

from .test_qk_eng_wb2 import get_assets_folder


@pytest.mark.embedding
def test_image_animation(printer, selection, embedded_app):
    """Tests to check image and animation exports

    ref:  Mechanical/QK_ENG_WB2/QK_ENG_WB2_005
    """
    globals().update(global_variables(embedded_app, True))
    Model.AddStaticStructuralAnalysis()
    geometry_file = os.path.join(get_assets_folder(), "Eng157.x_t")
    geometry_import = Model.GeometryImportGroup.AddGeometryImport()
    geometry_import.Import(geometry_file)
    printer("Running test")

    ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardBIN
    MODEL = Model
    MODEL.Geometry.ElementControl = ElementControl.Manual
    STAT_STRUC = MODEL.Analyses[0]
    selection.UpdateSelection(ExtAPI, [26], SelectionTypeEnum.GeometryEntities)
    FIX_SUP = STAT_STRUC.AddFixedSupport()
    selection.UpdateSelection(ExtAPI, [25], SelectionTypeEnum.GeometryEntities)
    FRC = STAT_STRUC.AddForce()
    FRC.DefineBy = LoadDefineBy.Components
    FRC.ZComponent.Output.SetDiscreteValue(0, Quantity("-1 [lbf]"))
    ExtAPI.SelectionManager.ClearSelection()
    DIR_DEF_STAT_STRUC = STAT_STRUC.Solution.AddDirectionalDeformation()
    STAT_STRUC.Solution.Solve(True)
    assert STAT_STRUC.Solution.ObjectState == ObjectState.Solved

    printer("Image export")
    Tree.Activate([DIR_DEF_STAT_STRUC])
    ExtAPI.Graphics.Camera.SetFit()
    image_export_format = GraphicsImageExportFormat.PNG
    settings_720p = Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
    settings_720p.Resolution = GraphicsResolutionType.EnhancedResolution
    settings_720p.Background = GraphicsBackgroundType.White
    settings_720p.Width = 1280
    settings_720p.Height = 720
    image_file = os.path.join(os.getcwd(), "geometry.png")
    ExtAPI.Graphics.ExportImage(image_file, image_export_format, settings_720p)
    assert os.path.isfile(image_file)
    os.remove(image_file)

    animation_formats = ["GIF", "AVI", "MP4", "WMV"]
    settings_720p = Ansys.Mechanical.Graphics.AnimationExportSettings()
    settings_720p.Width = 1280
    settings_720p.Height = 720
    for animation_format in animation_formats:
        printer(f"{animation_format} animation export")
        animation_file = os.path.join(os.getcwd(), f"animation.{animation_format}")
        animation_export_format = getattr(
            Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat, animation_format
        )
        DIR_DEF_STAT_STRUC.ExportAnimation(animation_file, animation_export_format, settings_720p)
        assert os.path.isfile(animation_file)
        with open(animation_file, "rb") as file:
            try:
                file.read()
            except Exception as e:
                assert False, f"Failed to read file {animation_file}: {e}"
        os.remove(animation_file)
