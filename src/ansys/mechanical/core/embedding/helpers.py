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
    >>> helpers.print_tree()
    """

    def __init__(self, app):
        """Initialize the Helpers class with the app instance."""
        self._app = app

        # Import Ansys module for use across helper methods
        from ansys.mechanical.core.embedding.global_importer import Ansys

        self.Ansys = Ansys

    def print_tree(self, node=None, max_lines=80):
        """
        Print the hierarchical tree representation of the Mechanical project structure.

        Parameters
        ----------
        node : DataModel object, optional
            The starting object of the tree. If not provided, starts from the Project.
        max_lines : int, optional
            The maximum number of lines to print. Default is 80.
            If set to -1, no limit is applied.

        Raises
        ------
        AttributeError
            If the node does not have the required attributes.

        Examples
        --------
        >>> from ansys.mechanical.core import App
        >>> app = App()
        >>> app.helpers.print_tree()
        ... ├── Project
        ... |  ├── Model
        ... |  |  ├── Geometry Imports (⚡︎)

        >>> app.helpers.print_tree(app.Model, max_lines=3)
        ... ├── Model
        ... |  ├── Geometry Imports (⚡︎)
        ... |  ├── Geometry (?)
        ... ... truncating after 3 lines
        """
        if node is None:
            node = self._app.DataModel.Project

        _print_tree(node, max_lines, 0, "")

    def import_geometry(self, file_path: str, process_named_selections: bool = True):
        r"""Import geometry file into the current Mechanical model.

        Parameters
        ----------
        file_path : str
            The path to the geometry file to be imported.
        process_named_selections : bool, optional
            Whether to process named selections during import. Default is True.

        Examples
        --------
        >>> from ansys.mechanical.core import App
        >>> app = App()
        >>> app.helpers.import_geometry("C:\\path\\to\\geometry.pmdb")

        >>> # Import without processing named selections
        >>> app.helpers.import_geometry(
        ...     "C:\\path\\to\\geometry.step", process_named_selections=False
        ... )
        """
        # Import Ansys and enums - same way as when App(globals=globals()) is used

        # Create a geometry import group for the model
        geometry_import_group = self._app.Model.GeometryImportGroup
        # Add the geometry import to the group
        geometry_import = geometry_import_group.AddGeometryImport()
        # Set the geometry import format
        geometry_import_format = (
            self.Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
        )
        # Set the geometry import preferences
        geometry_import_preferences = (
            self.Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
        )
        geometry_import_preferences.ProcessNamedSelections = process_named_selections
        try:
            geometry_import.Import(file_path, geometry_import_format, geometry_import_preferences)
            self._app.log_info(
                f"Imported geometry from {file_path} successfully."
                f"Object State: {geometry_import.ObjectState}"
            )
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
        >>> app = App()
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
        file_path: str = None,
        width: int = 1920,
        height: int = 1080,
        background: str = "white",
        resolution: str = "enhanced",
        current_graphics_display: bool = False,
        image_format: str = "png",
    ):
        r"""Export an image of the specified object.

        Parameters
        ----------
        obj : optional
            The object to activate and export. If None, exports the current graphics display.
            Can be any Mechanical object such as Geometry, Mesh, or Results.
        file_path : str, optional
            The path where the image will be saved. If None, defaults to "mechanical_export.png"
            in the project directory.
        width : int, optional
            The width of the exported image in pixels. Default is 1920.
        height : int, optional
            The height of the exported image in pixels. Default is 1080.
        background : str, optional
            Background type for the exported image. Options are:
            - "white": White background
            - "appearance": Use graphics appearance setting
            Default is "white".
        resolution : str, optional
            Resolution type for the exported image. Options are:
            - "normal": Normal resolution (1:1)
            - "enhanced": Enhanced resolution (2:1) - Default
            - "high": High resolution (4:1)
            Default is "enhanced".
        current_graphics_display : bool, optional
            Whether to use current graphics display. Default is False.
        image_format : str, optional
            Image format for export. Options are:
            - "png": PNG image format - Default
            - "jpg": JPG image format
            - "bmp": BMP image format
            - "tif": TIFF image format
            - "eps": EPS image format
            Default is "png".

        Examples
        --------
        >>> from ansys.mechanical.core import App
        >>> app = App()
        >>> # Export the geometry
        >>> app.helpers.export_image(app.Model.Geometry, "C:\\path\\to\\geometry.png")

        >>> # Export a specific result with custom settings
        >>> result = app.Model.Analyses[0].Solution.Children[0]
        >>> app.helpers.export_image(
        ...     result,
        ...     "C:\\path\\to\\result.jpg",
        ...     background="appearance",
        ...     resolution="high",
        ...     image_format="jpg",
        ... )
        """
        from pathlib import Path

        from ansys.mechanical.core.embedding.enum_importer import (
            GraphicsBackgroundType,
            GraphicsImageExportFormat,
            GraphicsResolutionType,
        )

        # Set default file path if not provided
        if file_path is None:
            raise ValueError("file_path must be provided for image export.")
        else:
            file_path = Path(file_path)
            # If only filename provided (no directory), save to current working directory
            if not file_path.parent or file_path.parent == Path():
                file_path = Path.cwd() / file_path.name

        # Convert to string for API call
        file_path = str(file_path)

        # Activate the object if provided
        if obj is not None:
            self._app.Tree.Activate([obj])

        # Create graphics image export settings
        graphics_image_export_settings = (
            self.Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
        )

        # Set resolution type
        resolution_lower = resolution.lower()
        if resolution_lower == "enhanced":
            graphics_image_export_settings.Resolution = GraphicsResolutionType.EnhancedResolution
        elif resolution_lower == "high":
            graphics_image_export_settings.Resolution = GraphicsResolutionType.HighResolution
        elif resolution_lower == "normal":
            graphics_image_export_settings.Resolution = GraphicsResolutionType.NormalResolution
        else:
            raise ValueError(
                f"Invalid resolution type: {resolution}. "
                "Valid options are 'Normal', 'Enhanced', or 'High'."
            )

        # Set background type
        if background.lower() == "white":
            graphics_image_export_settings.Background = GraphicsBackgroundType.White
        elif background.lower() == "appearance":
            graphics_image_export_settings.Background = (
                GraphicsBackgroundType.GraphicsAppearanceSetting
            )
        else:
            raise ValueError(
                f"Invalid background type: {background}. Valid options are 'White' or 'Appearance'."
            )

        # Set image format
        format_lower = image_format.lower()
        if format_lower == "png":
            export_format = GraphicsImageExportFormat.PNG
        elif format_lower == "jpg" or format_lower == "jpeg":
            export_format = GraphicsImageExportFormat.JPG
        elif format_lower == "bmp":
            export_format = GraphicsImageExportFormat.BMP
        elif format_lower == "tif" or format_lower == "tiff":
            export_format = GraphicsImageExportFormat.TIF
        elif format_lower == "eps":
            export_format = GraphicsImageExportFormat.EPS
        else:
            raise ValueError(
                f"Invalid image format: {image_format}. "
                "Valid options are 'PNG', 'JPG', 'BMP', 'TIF', or 'EPS'."
            )

        graphics_image_export_settings.CurrentGraphicsDisplay = current_graphics_display
        graphics_image_export_settings.Width = width
        graphics_image_export_settings.Height = height

        try:
            self._app.Graphics.ExportImage(file_path, export_format, graphics_image_export_settings)
            self._app.log_info(f"Exported image to {file_path} successfully.")
        except Exception as e:
            raise RuntimeError(f"Image export unsuccessful: {e}")

    def export_animation(
        self,
        obj=None,
        file_path: str = None,
        width: int = 1280,
        height: int = 720,
        animation_format: str = "gif",
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
        animation_format : str, optional
            Animation format for export. Options are:
            - "gif": GIF animation format - Default
            - "avi": AVI video format
            - "mp4": MP4 video format
            - "wmv": WMV video format
            Default is "gif".

        Examples
        --------
        >>> from ansys.mechanical.core import App
        >>> app = App()
        >>> # Export animation of a result
        >>> result = app.Model.Analyses[0].Solution.Children[0]
        >>> app.helpers.export_animation(result, "result_animation.gif")

        >>> # Export as MP4 with custom resolution
        >>> app.helpers.export_animation(
        ...     result, "result_animation.mp4", width=1920, height=1080, animation_format="mp4"
        ... )
        """
        from pathlib import Path

        from ansys.mechanical.core.embedding.enum_importer import (
            GraphicsAnimationExportFormat,
        )

        # Set default file path if not provided
        if file_path is None:
            raise ValueError("file_path must be provided for animation export.")
        else:
            file_path = Path(file_path)
            # If only filename provided (no directory), save to current working directory
            if not file_path.parent or file_path.parent == Path():
                file_path = Path.cwd() / file_path.name

        # Convert to string for API call
        file_path = str(file_path)

        # Activate the object if provided
        if obj is None:
            self._app.log_info(
                "No object provided for animation export; using first active object."
            )
            obj = self._app.Tree.FirstActiveObject

        # Create animation export settings
        animation_export_settings = self.Ansys.Mechanical.Graphics.AnimationExportSettings(
            width, height
        )

        # Set animation format
        format_lower = animation_format.lower()
        if format_lower == "gif":
            export_format = GraphicsAnimationExportFormat.GIF
        elif format_lower == "avi":
            export_format = GraphicsAnimationExportFormat.AVI
        elif format_lower == "mp4":
            export_format = GraphicsAnimationExportFormat.MP4
        elif format_lower == "wmv":
            export_format = GraphicsAnimationExportFormat.WMV
        else:
            raise ValueError(
                f"Invalid animation format: {animation_format}. "
                "Valid options are 'GIF', 'AVI', 'MP4', or 'WMV'."
            )

        try:
            self._app.Tree.Activate([obj])
            obj.ExportAnimation(file_path, export_format, animation_export_settings)
            self._app.log_info(f"Exported animation to {file_path} successfully.")
        except Exception as e:
            raise RuntimeError(f"Animation export unsuccessful: {e}")

    def setup_graphics(
        self,
        orientation: str = "iso",
        fit: bool = True,
        width: int = 1280,
        height: int = 720,
        resolution: str = "enhanced",
        background: str = "white",
        image_format: str = "png",
    ):
        """Configure graphics settings for image export.

        This is a convenience method that sets up camera orientation and creates
        pre-configured image export settings. Commonly used at the start of examples
        to prepare for exporting images.

        Parameters
        ----------
        orientation : str, optional
            Camera view orientation. Options are:
            - "iso": Isometric view - Default
            - "front": Front view
            - "back": Back view
            - "top": Top view
            - "bottom": Bottom view
            - "left": Left view
            - "right": Right view
            Default is "iso".
        fit : bool, optional
            Whether to fit the camera to the model. Default is True.
        width : int, optional
            Width of exported images in pixels. Default is 1280.
        height : int, optional
            Height of exported images in pixels. Default is 720.
        resolution : str, optional
            Resolution type for exported images. Options are:
            - "normal": Normal resolution (1:1)
            - "enhanced": Enhanced resolution (2:1) - Default
            - "high": High resolution (4:1)
            Default is "enhanced".
        background : str, optional
            Background type for exported images. Options are:
            - "white": White background - Default
            - "appearance": Use graphics appearance setting
            Default is "white".
        image_format : str, optional
            Default image format for exports. Options are:
            - "png": PNG image format - Default
            - "jpg": JPG image format
            - "bmp": BMP image format
            - "tif": TIFF image format
            - "eps": EPS image format
            Default is "png".

        Returns
        -------
        tuple
            A tuple containing (camera, settings, format) where:
            - camera: The configured camera object
            - settings: GraphicsImageExportSettings with specified parameters
            - format: GraphicsImageExportFormat enum value

        Examples
        --------
        >>> from ansys.mechanical.core import App
        >>> app = App()
        >>> # Set up graphics with default settings (Iso view, 720p)
        >>> camera, settings, img_format = app.helpers.setup_graphics()

        >>> # Set up graphics with custom orientation and 1080p resolution
        >>> camera, settings, img_format = app.helpers.setup_graphics(
        ...     orientation="front", width=1920, height=1080, resolution="high"
        ... )

        >>> # Use the configured settings to export an image
        >>> app.Graphics.ExportImage("output.png", img_format, settings)
        """
        from ansys.mechanical.core.embedding.enum_importer import (
            GraphicsBackgroundType,
            GraphicsImageExportFormat,
            GraphicsResolutionType,
            ViewOrientationType,
        )

        # Get graphics and camera
        graphics = self._app.Graphics
        camera = graphics.Camera

        # Set camera orientation
        orientation_lower = orientation.lower()
        if orientation_lower == "iso":
            camera.SetSpecificViewOrientation(ViewOrientationType.Iso)
        elif orientation_lower == "front":
            camera.SetSpecificViewOrientation(ViewOrientationType.Front)
        elif orientation_lower == "back":
            camera.SetSpecificViewOrientation(ViewOrientationType.Back)
        elif orientation_lower == "top":
            camera.SetSpecificViewOrientation(ViewOrientationType.Top)
        elif orientation_lower == "bottom":
            camera.SetSpecificViewOrientation(ViewOrientationType.Bottom)
        elif orientation_lower == "left":
            camera.SetSpecificViewOrientation(ViewOrientationType.Left)
        elif orientation_lower == "right":
            camera.SetSpecificViewOrientation(ViewOrientationType.Right)
        else:
            raise ValueError(
                f"Invalid orientation: {orientation}. "
                "Valid options are 'Iso', 'Front', 'Back', 'Top', 'Bottom', 'Left', or 'Right'."
            )

        # Fit camera if requested
        if fit:
            camera.SetFit()

        # Create graphics image export settings
        settings = self.Ansys.Mechanical.Graphics.GraphicsImageExportSettings()
        settings.Width = width
        settings.Height = height
        settings.CurrentGraphicsDisplay = False

        # Set resolution
        resolution_lower = resolution.lower()
        if resolution_lower == "enhanced":
            settings.Resolution = GraphicsResolutionType.EnhancedResolution
        elif resolution_lower == "high":
            settings.Resolution = GraphicsResolutionType.HighResolution
        elif resolution_lower == "normal":
            settings.Resolution = GraphicsResolutionType.NormalResolution
        else:
            raise ValueError(
                f"Invalid resolution: {resolution}. "
                "Valid options are 'Normal', 'Enhanced', or 'High'."
            )

        # Set background
        background_lower = background.lower()
        if background_lower == "white":
            settings.Background = GraphicsBackgroundType.White
        elif background_lower == "appearance":
            settings.Background = GraphicsBackgroundType.GraphicsAppearanceSetting
        else:
            raise ValueError(
                f"Invalid background: {background}. Valid options are 'White' or 'Appearance'."
            )

        # Set image format
        format_lower = image_format.lower()
        if format_lower == "png":
            img_format = GraphicsImageExportFormat.PNG
        elif format_lower == "jpg" or format_lower == "jpeg":
            img_format = GraphicsImageExportFormat.JPG
        elif format_lower == "bmp":
            img_format = GraphicsImageExportFormat.BMP
        elif format_lower == "tif" or format_lower == "tiff":
            img_format = GraphicsImageExportFormat.TIF
        elif format_lower == "eps":
            img_format = GraphicsImageExportFormat.EPS
        else:
            raise ValueError(
                f"Invalid image format: {image_format}. "
                "Valid options are 'PNG', 'JPG', 'BMP', 'TIF', or 'EPS'."
            )

        return camera, settings, img_format


# Helper function to print the tree recursively
def _print_tree(node, max_lines, lines_count, indentation):
    """Recursively print till provided maximum lines limit.

    Each object in the tree is expected to have the following attributes:
        - Name: The name of the object.
        - Suppressed : Print as suppressed, if object is suppressed.
        - Children: Checks if object have children.
        Each child node is expected to have the all these attributes.

    Parameters
    ----------
    lines_count: int, optional
        The current count of lines printed. Default is 0.
    indentation: str, optional
        The indentation string used for printing the tree structure. Default is "".
    """
    if lines_count >= max_lines and max_lines != -1:
        print(f"... truncating after {max_lines} lines")
        return lines_count

    if not hasattr(node, "Name"):
        raise AttributeError("Object must have a 'Name' attribute")

    node_name = node.Name
    if hasattr(node, "Suppressed") and node.Suppressed is True:
        node_name += " (Suppressed)"
    if hasattr(node, "ObjectState"):
        if str(node.ObjectState) == "UnderDefined":
            node_name += " (?)"
        elif str(node.ObjectState) == "Solved" or str(node.ObjectState) == "FullyDefined":
            node_name += " (✓)"
        elif str(node.ObjectState) == "NotSolved" or str(node.ObjectState) == "Obsolete":
            node_name += " (⚡︎)"
        elif str(node.ObjectState) == "SolveFailed":
            node_name += " (✕)"
    print(f"{indentation}├── {node_name}")
    lines_count += 1

    if lines_count >= max_lines and max_lines != -1:
        print(f"... truncating after {max_lines} lines")
        return lines_count

    if hasattr(node, "Children") and node.Children is not None and node.Children.Count > 0:
        for child in node.Children:
            lines_count = _print_tree(child, max_lines, lines_count, indentation + "|  ")
            if lines_count >= max_lines and max_lines != -1:
                break

    return lines_count
