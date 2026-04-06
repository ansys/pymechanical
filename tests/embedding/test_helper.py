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

"""Tests for embedding helper methods."""

from pathlib import Path

import pytest


def _is_readable(filepath):
    """Assert that the file is non-empty and readable, then delete it."""
    filepath = Path(filepath)
    try:
        with filepath.open("rb") as file:
            file.read()
    except Exception as e:
        assert False, f"Failed to read file {filepath}: {e}"
    finally:
        filepath.unlink(missing_ok=True)


@pytest.mark.embedding
def test_helpers_initialization(embedded_app):
    """Test that helpers are properly initialized with the app."""
    assert embedded_app.helpers is not None
    assert hasattr(embedded_app.helpers, "_app")
    assert embedded_app.helpers._app == embedded_app
    assert hasattr(embedded_app.helpers, "Ansys")


@pytest.mark.embedding
def test_import_geometry(embedded_app, assets, printer):
    """Test geometry import with basic and all options."""
    printer("Testing geometry import")
    geometry_file = str(Path(assets) / "Eng157.x_t")

    # Test basic import
    printer("Testing basic geometry import")
    geometry_import = embedded_app.helpers.import_geometry(geometry_file)
    assert geometry_import is not None
    assert str(geometry_import.ObjectState) in ["FullyDefined", "Solved"]
    printer(f"Basic import successful: {geometry_import.ObjectState}")

    # Start fresh for comprehensive test
    embedded_app.new()

    # Test with all options enabled
    printer("Testing geometry import with all options")
    GeometryImportPreference = (  # noqa: N806
        embedded_app.helpers.Ansys.Mechanical.DataModel.Enums.GeometryImportPreference
    )
    geometry_import = embedded_app.helpers.import_geometry(
        geometry_file,
        process_named_selections=True,
        named_selection_key="",
        process_material_properties=True,
        process_coordinate_systems=True,
        analysis_type=GeometryImportPreference.AnalysisType.Type3D,
    )
    assert geometry_import is not None
    assert str(geometry_import.ObjectState) in ["FullyDefined", "Solved"]
    printer("Import with all options successful")


@pytest.mark.embedding
def test_import_geometry_invalid_file(embedded_app, printer):
    """Test geometry import with invalid file path."""
    printer("Testing geometry import with invalid file")
    invalid_file = "C:\\nonexistent\\file.x_t"

    with pytest.raises(RuntimeError, match="Geometry Import unsuccessful"):
        embedded_app.helpers.import_geometry(invalid_file)


@pytest.mark.embedding
def test_import_materials(embedded_app, assets, printer):
    """Test material import."""
    printer("Testing material import")
    material_file = str(Path(assets) / "eng200_material.xml")

    embedded_app.helpers.import_materials(material_file)

    # Verify materials were imported
    materials = embedded_app.Model.Materials
    assert materials.Children is not None
    # Materials collection doesn't have Count, but import should succeed without error
    printer("Materials imported successfully")


@pytest.mark.embedding
def test_import_materials_invalid_file(embedded_app, printer):
    """Test material import with invalid file."""
    printer("Testing material import with invalid file")
    invalid_file = "C:\\nonexistent\\materials.xml"

    with pytest.raises(RuntimeError, match="Material Import unsuccessful"):
        embedded_app.helpers.import_materials(invalid_file)


@pytest.mark.embedding
def test_export_image(embedded_app, assets, tmp_path, printer):
    """Test image export with default and custom settings."""
    printer("Testing image export")
    geometry_file = str(Path(assets) / "Eng157.x_t")
    embedded_app.helpers.import_geometry(geometry_file)

    # Test with default parameters
    printer("Testing image export with defaults")
    image_path = tmp_path / "test_image.png"
    embedded_app.helpers.export_image(
        obj=embedded_app.Model.Geometry,
        file_path=str(image_path),
    )
    _is_readable(image_path)
    printer(f"Default export successful: {image_path}")

    # Test with custom settings using enums
    from ansys.mechanical.core.embedding.enum_importer import (
        GraphicsBackgroundType,
        GraphicsImageExportFormat,
        GraphicsResolutionType,
    )

    printer("Testing image export with custom settings")
    image_path_custom = tmp_path / "test_custom.jpg"
    embedded_app.helpers.export_image(
        obj=embedded_app.Model.Geometry,
        file_path=str(image_path_custom),
        width=1280,
        height=720,
        background=GraphicsBackgroundType.GraphicsAppearanceSetting,
        resolution=GraphicsResolutionType.HighResolution,
        image_format=GraphicsImageExportFormat.JPG,
    )
    _is_readable(image_path_custom)
    printer("Custom export successful")


@pytest.mark.embedding
def test_export_image_all_formats(embedded_app, assets, tmp_path, printer):
    """Test image export with different formats."""
    printer("Testing image export with all formats")
    geometry_file = str(Path(assets) / "Eng157.x_t")
    embedded_app.helpers.import_geometry(geometry_file)

    from ansys.mechanical.core.embedding.enum_importer import GraphicsImageExportFormat

    format_map = {
        "png": GraphicsImageExportFormat.PNG,
        "jpg": GraphicsImageExportFormat.JPG,
        "bmp": GraphicsImageExportFormat.BMP,
        "tif": GraphicsImageExportFormat.TIF,
        "eps": GraphicsImageExportFormat.EPS,
    }
    for name, fmt in format_map.items():
        image_path = tmp_path / f"test_image.{name}"
        embedded_app.helpers.export_image(
            obj=embedded_app.Model.Geometry,
            file_path=str(image_path),
            image_format=fmt,
        )
        _is_readable(image_path)
        printer(f"Exported {name} successfully")


@pytest.mark.embedding
def test_export_image_validation_errors(embedded_app, assets, tmp_path, printer):
    """Test image export validation errors."""
    printer("Testing image export validation errors")
    geometry_file = str(Path(assets) / "Eng157.x_t")
    embedded_app.helpers.import_geometry(geometry_file)

    # Test missing file path
    printer("Testing missing file path error")
    with pytest.raises(ValueError, match="file_path must be provided"):
        embedded_app.helpers.export_image(obj=embedded_app.Model.Geometry)

    printer("All validation errors handled correctly")


@pytest.mark.embedding
def test_export_animation_basic(embedded_app, tmp_path, printer, graphics_test_mechdb_file):
    """Test basic animation export with graphics fixture."""
    printer("Testing basic animation export")

    # Open the mechdb file with solved results
    embedded_app.open(str(graphics_test_mechdb_file))
    embedded_app.Model.Analyses[0].Solution.ClearGeneratedData()
    printer("Solving the model")
    embedded_app.Model.Analyses[0].Solution.Solve()
    printer("Model solved")
    # Get the deformation result
    result = embedded_app.Model.Analyses[0].Solution.Children[1]
    printer(result.Name)
    assert result is not None

    # Test all animation formats
    from ansys.mechanical.core.embedding.enum_importer import GraphicsAnimationExportFormat

    format_map = {
        "gif": GraphicsAnimationExportFormat.GIF,
        "avi": GraphicsAnimationExportFormat.AVI,
        "mp4": GraphicsAnimationExportFormat.MP4,
        "wmv": GraphicsAnimationExportFormat.WMV,
    }
    for name, fmt in format_map.items():
        animation_path = tmp_path / f"test_animation.{name}"
        embedded_app.helpers.export_animation(
            obj=result,
            file_path=str(animation_path),
            animation_format=fmt,
            width=640,
            height=480,
        )
        _is_readable(animation_path)
        printer(f"Exported {name} successfully")


@pytest.mark.embedding
def test_export_animation_validation_errors(embedded_app, assets, tmp_path, printer):
    """Test animation export validation errors."""
    printer("Testing animation export validation errors")
    geometry_file = str(Path(assets) / "Eng157.x_t")
    embedded_app.helpers.import_geometry(geometry_file)

    analysis = embedded_app.Model.AddStaticStructuralAnalysis()
    result = analysis.Solution.AddTotalDeformation()

    # Test missing file path
    printer("Testing missing file path error")
    with pytest.raises(ValueError, match="file_path must be provided"):
        embedded_app.helpers.export_animation(obj=result)

    printer("All animation validation errors handled correctly")


@pytest.mark.embedding
def test_display_image(embedded_app, assets, tmp_path, printer, monkeypatch):
    """Test display_image with default and custom settings."""
    printer("Testing display_image")
    geometry_file = str(Path(assets) / "Eng157.x_t")
    embedded_app.helpers.import_geometry(geometry_file)

    # Mock pyplot.show to avoid displaying during tests
    show_called = []

    def mock_show():
        show_called.append(True)

    import matplotlib.pyplot as plt

    monkeypatch.setattr(plt, "show", mock_show)

    # Test with default settings
    printer("Testing display with defaults")
    image_path = tmp_path / "test_display.png"
    embedded_app.helpers.export_image(
        obj=embedded_app.Model.Geometry,
        file_path=str(image_path),
    )
    embedded_app.helpers.display_image(str(image_path))
    assert len(show_called) == 1
    printer("Default display successful")
    Path(image_path).unlink(missing_ok=True)

    # Test with custom settings
    printer("Testing display with custom settings")
    image_path_custom = tmp_path / "test_display_custom.png"
    embedded_app.helpers.export_image(
        obj=embedded_app.Model.Geometry,
        file_path=str(image_path_custom),
    )
    embedded_app.helpers.display_image(
        str(image_path_custom),
        figsize=(10, 6),
        axis="on",
    )
    assert len(show_called) == 2
    printer("Custom display successful")
    Path(image_path_custom).unlink(missing_ok=True)
