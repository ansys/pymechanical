.. _ref_embedding_user_guide_helpers:

Helpers methods
===============

The `Helpers <../api/ansys/mechanical/core/embedding/helpers/Helpers.html#ansys.mechanical.core.embedding.helpers.Helpers>`_ class provides
convenient utility methods for common Mechanical operations. These helpers simplify tasks such as
importing geometry and materials, exporting images and animations, configuring views, and
visualizing the project tree structure.

The Helpers class is accessible through the ``helpers`` attribute of the
`App <../api/ansys/mechanical/core/embedding/app/App.html#ansys.mechanical.core.embedding.app.App>`_ instance:

.. code:: python

   from ansys.mechanical.core import App

   app = App(globals=globals())
   helpers = app.helpers

All helper methods are designed to work seamlessly with the embedded Mechanical instance and
provide clear error messages when operations fail.


Importing geometry
------------------

The ``import_geometry()`` method simplifies importing geometry files into your Mechanical model.
It supports various CAD formats and provides options for processing named selections, material
properties, and coordinate systems.

**Basic geometry import**

.. code:: python

   from ansys.mechanical.core import App

   app = App(globals=globals())
   geometry_import = app.helpers.import_geometry("path/to/geometry.x_t")

**Import with named selections**

Process named selections from the geometry file:

.. code:: python

   geometry_import = app.helpers.import_geometry(
       "path/to/geometry.pmdb",
       process_named_selections=True,
       named_selection_key="NS"
   )

**Import with all options**

Import geometry with material properties and coordinate systems:

.. code:: python

   geometry_import = app.helpers.import_geometry(
       "path/to/geometry.step",
       process_named_selections=True,
       named_selection_key="",
       process_material_properties=True,
       process_coordinate_systems=True,
   )

**2D analysis**

For 2D analyses, specify the analysis type using the ``GeometryImportPreference`` enum:

.. code:: python

   from ansys.mechanical.core.embedding.enum_importer import GeometryImportPreference

   geometry_import = app.helpers.import_geometry(
       "path/to/geometry.agdb",
       analysis_type=GeometryImportPreference.AnalysisType.Type2D
   )

.. note::
   The method automatically determines the geometry format and returns the geometry import object.
   If the import fails, a ``RuntimeError`` is raised with details about the failure.

Importing materials
-------------------

The ``import_materials()`` method imports materials from XML material database files.

.. code:: python

   from ansys.mechanical.core import App

   app = App(globals=globals())
   app.helpers.import_materials("path/to/materials.xml")

This method adds the materials to the ``Model.Materials`` collection. If the import fails,
a ``RuntimeError`` is raised.

Exporting images
----------------

The ``export_image()`` method exports high-quality images of your model, geometry, mesh, or results.
It provides extensive control over image resolution, format, and appearance.

**Basic image export**

.. code:: python

   from ansys.mechanical.core import App

   app = App(globals=globals())
   # Import geometry first
   app.helpers.import_geometry("path/to/geometry.x_t")

   # Export an image of the geometry
   app.helpers.export_image(
       obj=app.Model.Geometry,
       file_path="geometry_image.png"
   )

**Custom image settings**

Control image dimensions, resolution, background, and format using Mechanical enums:

.. code:: python

   from ansys.mechanical.core.embedding.enum_importer import (
       GraphicsBackgroundType,
       GraphicsImageExportFormat,
       GraphicsResolutionType,
   )

   app.helpers.export_image(
       obj=app.Model.Geometry,
       file_path="custom_image.jpg",
       width=1920,
       height=1080,
       background=GraphicsBackgroundType.GraphicsAppearanceSetting,
       resolution=GraphicsResolutionType.HighResolution,
       image_format=GraphicsImageExportFormat.JPG,
   )

**Export current graphics display**

Export whatever is currently displayed without specifying an object:

.. code:: python

   app.helpers.export_image(
       file_path="current_view.png",
       current_graphics_display=True
   )

**Supported image formats (``GraphicsImageExportFormat``)**

- ``GraphicsImageExportFormat.PNG`` - Recommended for technical documentation (lossless, default)
- ``GraphicsImageExportFormat.JPG`` - Good for photographs and presentations
- ``GraphicsImageExportFormat.BMP`` - Uncompressed bitmap
- ``GraphicsImageExportFormat.TIF`` - Tagged image format (lossless)
- ``GraphicsImageExportFormat.EPS`` - Vector format for publications

**Resolution options (``GraphicsResolutionType``)**

- ``GraphicsResolutionType.NormalResolution`` - 1:1 pixel ratio (fastest)
- ``GraphicsResolutionType.EnhancedResolution`` - 2:1 pixel ratio (default, good quality)
- ``GraphicsResolutionType.HighResolution`` - 4:1 pixel ratio (best quality, slower)

Exporting animations
--------------------

The ``export_animation()`` method exports animations of results that have multiple time steps
or mode shapes, such as transient analyses or modal analyses.

.. code:: python

   from ansys.mechanical.core import App

   app = App(globals=globals())
   # Set up and solve an analysis...
   analysis = app.Model.AddStaticStructuralAnalysis()
   result = analysis.Solution.AddTotalDeformation()

   # After solving, export animation
   app.helpers.export_animation(
       obj=result,
       file_path="deformation.gif"
   )

**Custom animation settings**

.. code:: python

   from ansys.mechanical.core.embedding.enum_importer import GraphicsAnimationExportFormat

   app.helpers.export_animation(
       obj=result,
       file_path="deformation.mp4",
       width=1920,
       height=1080,
       animation_format=GraphicsAnimationExportFormat.MP4,
   )

**Supported animation formats (``GraphicsAnimationExportFormat``)**

- ``GraphicsAnimationExportFormat.GIF`` - Widely supported, good for web (default)
- ``GraphicsAnimationExportFormat.AVI`` - Uncompressed video
- ``GraphicsAnimationExportFormat.MP4`` - Compressed video, good for presentations
- ``GraphicsAnimationExportFormat.WMV`` - Windows Media Video format

.. note::
   Animation export requires that the result has been solved and has multiple steps or modes
   to animate. If no ``obj`` is provided, the method falls back to the first active object in
   the tree. Attempting to export an animation of unsolved results raises a ``RuntimeError``.


Displaying images
-----------------

The ``display_image()`` method uses ``matplotlib`` to display exported images directly in your
Python environment. This is particularly useful in Jupyter notebooks or interactive sessions.

.. code:: python

   from ansys.mechanical.core import App

   app = App(globals=globals())
   # Export an image
   app.helpers.export_image(
       obj=app.Model.Geometry,
       file_path="geometry.png"
   )

   # Display it
   app.helpers.display_image("geometry.png")

**Custom display settings**

.. code:: python

   app.helpers.display_image(
       "geometry.png",
       figsize=(12, 8),  # Figure size in inches
       axis="off"  # Hide axes completely
   )

Workflow examples
-----------------

**Complete geometry visualization workflow**

.. code:: python

   from ansys.mechanical.core import App

   app = App(globals=globals())

   # Step 1: Import geometry
   app.helpers.import_geometry("bracket.x_t")

   # Step 2: Import materials
   app.helpers.import_materials("materials.xml")

   # Step 3: Export image
   from ansys.mechanical.core.embedding.enum_importer import GraphicsResolutionType

   app.helpers.export_image(
       obj=app.Model.Geometry,
       file_path="bracket_iso.png",
       width=1920,
       height=1080,
       resolution=GraphicsResolutionType.EnhancedResolution,
   )

   # Step 4: Display it
   app.helpers.display_image("bracket_iso.png")



Error handling
--------------

All helper methods raise descriptive exceptions when operations fail:

**Geometry import errors**

.. code:: python

   from ansys.mechanical.core import App

   app = App(globals=globals())
   try:
       app.helpers.import_geometry("nonexistent.x_t")
   except RuntimeError as e:
       print(f"Geometry import failed: {e}")

**Image export errors**

.. code:: python

   try:
       app.helpers.export_image(
           obj=app.Model.Geometry,
           file_path=None  # Missing required parameter
       )
   except ValueError as e:
       print(f"Invalid parameter: {e}")

Best practices
--------------

1. **Always check paths**: Use absolute paths or ``pathlib.Path`` objects for file operations
   to avoid path-related errors.


2. **Use appropriate image formats**: PNG for technical documentation, JPG for presentations,
   EPS for publications.

3. **Handle errors gracefully**: Wrap helper method calls in try-except blocks to handle
   potential failures gracefully in production scripts.

4. **Verify imports**: After importing geometry or materials, verify the object state:

   .. code:: python

      geometry_import = app.helpers.import_geometry("part.x_t")
      if str(geometry_import.ObjectState) == "FullyDefined":
          print("Geometry imported successfully")
      else:
          print(f"Warning: Geometry state is {geometry_import.ObjectState}")
