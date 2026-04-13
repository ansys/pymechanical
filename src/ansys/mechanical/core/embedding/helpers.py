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

"""Helper functions for Embedded App."""


class Helpers:
    """Helper utilities for Mechanical embedding application.

    Parameters
    ----------
    app : App
        The Mechanical embedding application instance.

    Examples
    --------
    >>> from ansys.mechanical.core import App
    >>> app = App()
    >>> helpers = app.helpers
    """

    def __init__(self, app):
        """Initialize the Helpers class with the app instance."""
        self._app = app

        # Import Ansys module for use across helper methods
        from ansys.mechanical.core.embedding.global_importer import Ansys

        self.Ansys = Ansys

    def import_geometry(
        self,
        file_path: str,
        process_named_selections: bool = False,
        named_selection_key: str = "NS",
        process_material_properties: bool = False,
        process_coordinate_systems: bool = False,
        analysis_type=None,
    ):
        r"""Import geometry file into the current Mechanical model.

        Returns
        -------
        Ansys.ACT.Automation.Mechanical.GeometryImport
            The geometry import object.

        Parameters
        ----------
        file_path : str
            The path to the geometry file to be imported.
        process_named_selections : bool, optional
            Whether to process named selections during import. Default is False.
        named_selection_key : str, optional
            Named selection key for filtering. Default is "NS".
        process_material_properties : bool, optional
            Whether to process material properties during import. Default is False.
        process_coordinate_systems : bool, optional
            Whether to process coordinate systems during import. Default is False.
        analysis_type : GeometryImportPreference.AnalysisType, optional
            The analysis type enum for the geometry import. Default is
            ``GeometryImportPreference.AnalysisType.Type3D``.

        Examples
        --------
        >>> from ansys.mechanical.core import App
        >>> app = App()
        >>> app.helpers.import_geometry("C:\\path\\to\\geometry.pmdb")

        >>> # Import with 2D analysis type
        >>> from ansys.mechanical.core.embedding.enum_importer import GeometryImportPreference
        >>> app.helpers.import_geometry(
        ...     "C:\\path\\to\\geometry.agdb",
        ...     analysis_type=GeometryImportPreference.AnalysisType.Type2D,
        ... )

        >>> # Import with all options specified
        >>> app.helpers.import_geometry(
        ...     "C:\\path\\to\\geometry.pmdb",
        ...     process_named_selections=True,
        ...     named_selection_key="",
        ...     process_material_properties=True,
        ...     process_coordinate_systems=True,
        ... )
        """
        GeometryImportPreference = self.Ansys.Mechanical.DataModel.Enums.GeometryImportPreference  # noqa: N806

        if analysis_type is None:
            analysis_type = GeometryImportPreference.AnalysisType.Type3D

        geometry_import_group = self._app.Model.GeometryImportGroup
        geometry_import = geometry_import_group.AddGeometryImport()
        geometry_import_format = GeometryImportPreference.Format.Automatic
        geometry_import_preferences = (
            self.Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
        )
        geometry_import_preferences.ProcessNamedSelections = process_named_selections
        geometry_import_preferences.NamedSelectionKey = named_selection_key
        geometry_import_preferences.ProcessMaterialProperties = process_material_properties
        geometry_import_preferences.ProcessCoordinateSystems = process_coordinate_systems
        geometry_import_preferences.AnalysisType = analysis_type

        try:
            geometry_import.Import(file_path, geometry_import_format, geometry_import_preferences)
            self._app.log_info(
                f"Imported geometry from {file_path} successfully."
                f"Object State: {geometry_import.ObjectState}"
            )
            return geometry_import
        except Exception as e:
            raise RuntimeError(f"Geometry Import unsuccessful: {e}")

    def import_materials(self, file_path: str):
        r"""Import materials from a specified material database file.

        Parameters
        ----------
        file_path : str
            The path to the material database file to be imported.

        Examples
        --------
        >>> from ansys.mechanical.core import App
        >>> app.helpers.import_materials("C:\\path\\to\\materials.xml")
        """
        # Add materials to the model and import the material files
        materials = self._app.Model.Materials

        try:
            materials.Import(file_path)
            self._app.log_info(
                f"Imported materials from {file_path} successfully."
                f"Object State: {materials.ObjectState}"
            )
        except Exception as e:
            raise RuntimeError(f"Material Import unsuccessful: {e}")

    def export_image(
        self,
        obj=None,
        file_path: "str | None" = None,
        width: int = 1920,
        height: int = 1080,
        background=None,
        resolution=None,
        current_graphics_display: bool = False,
        image_format=None,
    ):
        r"""Export an image of the specified object.

        Parameters
        ----------
        obj : optional
            The object to activate and export. If None, exports the current graphics display.
            Can be any Mechanical object such as Geometry, Mesh, or Results.
        file_path : str, optional
            The path where the image will be saved.
        width : int, optional
            The width of the exported image in pixels. Default is 1920.
        height : int, optional
            The height of the exported image in pixels. Default is 1080.
        background : GraphicsBackgroundType, optional
            Background type for the exported image. Default is
            ``GraphicsBackgroundType.White``.
        resolution : GraphicsResolutionType, optional
            Resolution type for the exported image. Default is
            ``GraphicsResolutionType.EnhancedResolution``.
        current_graphics_display : bool, optional
            Whether to use current graphics display. Default is False.
        image_format : GraphicsImageExportFormat, optional
            Image format for export. Default is ``GraphicsImageExportFormat.PNG``.

        Examples
        --------
        >>> from ansys.mechanical.core import App
        >>> app = App()
        >>> app.helpers.export_image(app.Model.Geometry, "C:\\path\\to\\geometry.png")

        >>> from ansys.mechanical.core.embedding.enum_importer import (
        ...     GraphicsBackgroundType,
        ...     GraphicsImageExportFormat,
        ...     GraphicsResolutionType,
        ... )
        >>> result = app.Model.Analyses[0].Solution.Children[0]
        >>> app.helpers.export_image(
        ...     result,
        ...     "C:\\path\\to\\result.jpg",
        ...     background=GraphicsBackgroundType.GraphicsAppearanceSetting,
        ...     resolution=GraphicsResolutionType.HighResolution,
        ...     image_format=GraphicsImageExportFormat.JPG,
        ... )
        """
        from pathlib import Path

        from ansys.mechanical.core.embedding.enum_importer import (
            GraphicsBackgroundType,
            GraphicsImageExportFormat,
            GraphicsResolutionType,
        )

        if file_path is None:
            raise ValueError("file_path must be provided for image export.")

        resolved_path = Path(file_path)
        if not resolved_path.parent or resolved_path.parent == Path():
            resolved_path = Path.cwd() / resolved_path.name
        file_path = str(resolved_path)

        if obj is not None:
            self._app.Tree.Activate([obj])

        if background is None:
            background = GraphicsBackgroundType.White
        if resolution is None:
            resolution = GraphicsResolutionType.EnhancedResolution
        if image_format is None:
            image_format = GraphicsImageExportFormat.PNG

        graphics_image_export_settings = (
            self.Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
        )
        graphics_image_export_settings.Resolution = resolution
        graphics_image_export_settings.Background = background
        graphics_image_export_settings.CurrentGraphicsDisplay = current_graphics_display
        graphics_image_export_settings.Width = width
        graphics_image_export_settings.Height = height

        try:
            self._app.Graphics.ExportImage(file_path, image_format, graphics_image_export_settings)
            self._app.log_info(f"Exported image to {file_path} successfully.")
        except Exception as e:
            raise RuntimeError(f"Image export unsuccessful: {e}")

    def export_animation(
        self,
        obj=None,
        file_path: "str | None" = None,
        width: int = 1280,
        height: int = 720,
        animation_format=None,
    ):
        r"""Export an animation of the specified object.

        Parameters
        ----------
        obj : optional
            The object to activate and export animation. If None, exports animation of the
            current graphics display. Can be any Mechanical object that supports animation
            such as results with multiple time steps or modal analysis results.
        file_path : str, optional
            The path where the animation will be saved. If None, raises ValueError.
            If only a filename is provided, saves to current working directory.
        width : int, optional
            The width of the exported animation in pixels. Default is 1280.
        height : int, optional
            The height of the exported animation in pixels. Default is 720.
        animation_format : GraphicsAnimationExportFormat, optional
            Animation format for export. Default is ``GraphicsAnimationExportFormat.GIF``.

        Examples
        --------
        >>> from ansys.mechanical.core import App
        >>> app = App()
        >>> result = app.Model.Analyses[0].Solution.Children[0]
        >>> app.helpers.export_animation(result, "result_animation.gif")

        >>> from ansys.mechanical.core.embedding.enum_importer import (
        ...     GraphicsAnimationExportFormat,
        ... )
        >>> app.helpers.export_animation(
        ...     result,
        ...     "result_animation.mp4",
        ...     animation_format=GraphicsAnimationExportFormat.MP4,
        ... )
        """
        from pathlib import Path

        from ansys.mechanical.core.embedding.enum_importer import (
            GraphicsAnimationExportFormat,
        )

        if file_path is None:
            raise ValueError("file_path must be provided for animation export.")

        resolved_path = Path(file_path)
        if not resolved_path.parent or resolved_path.parent == Path():
            resolved_path = Path.cwd() / resolved_path.name
        file_path = str(resolved_path)

        if obj is None:
            self._app.log_info(
                "No object provided for animation export; using first active object."
            )
            obj = self._app.Tree.FirstActiveObject

        if animation_format is None:
            animation_format = GraphicsAnimationExportFormat.GIF

        animation_export_settings = self.Ansys.Mechanical.Graphics.AnimationExportSettings(
            width, height
        )

        try:
            self._app.Tree.Activate([obj])
            obj.ExportAnimation(file_path, animation_format, animation_export_settings)
            self._app.log_info(f"Exported animation to {file_path} successfully.")
        except Exception as e:
            raise RuntimeError(f"Animation export unsuccessful: {e}")

    def display_image(
        self,
        image_path: str,
        figsize: tuple = (16, 9),
        axis: str = "off",
    ):
        """Display an image using matplotlib.

        Parameters
        ----------
        image_path : str
            The path to the image file to display.
        figsize : tuple, optional
            The size of the figure in inches (width, height). Default is (16, 9).
        axis : str, optional
            The axis visibility setting ('on' or 'off'). Default is "off".

        Examples
        --------
        >>> from ansys.mechanical.core import App
        >>> app = App()
        >>> app.helpers.export_image(app.Model.Geometry, "geometry.png")
        >>> app.helpers.display_image("geometry.png")

        >>> # Display with custom figure size
        >>> app.helpers.display_image("result.png", figsize=(10, 6))
        """
        from matplotlib import image as mpimg, pyplot as plt

        # Set the figure size
        plt.figure(figsize=figsize)
        # Read and display the image
        plt.imshow(mpimg.imread(image_path))
        # Turn axis on or off
        plt.axis(axis)
        # Display the figure
        plt.show()
