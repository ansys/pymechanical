.. _ref_embedding_user_guide_helpers:

Helpers
=======

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
       analysis_type="3d"
   )

**2D analysis**

For 2D analyses, specify the analysis type:

.. code:: python

   geometry_import = app.helpers.import_geometry(
       "path/to/geometry.agdb",
       analysis_type="2d"
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

Control image dimensions, resolution, background, and format:

.. code:: python

   app.helpers.export_image(
       obj=app.Model.Geometry,
       file_path="custom_image.jpg",
       width=1920,
       height=1080,
       background="appearance",  # or "white"
       resolution="high",  # "normal", "enhanced", or "high"
       image_format="jpg"  # "png", "jpg", "bmp", "tif", or "eps"
   )

**Export current graphics display**

Export whatever is currently displayed without specifying an object:

.. code:: python

   app.helpers.export_image(
       file_path="current_view.png",
       current_graphics_display=True
   )

**Supported formats**

- **PNG** - Recommended for technical documentation (lossless)
- **JPG** - Good for photographs and presentations (compressed format)
- **BMP** - Uncompressed bitmap
- **TIF** - Tagged image format (lossless)
- **EPS** - Vector format for publications

**Resolution options**

- **normal** - 1:1 pixel ratio (fastest)
- **enhanced** - 2:1 pixel ratio (default, good quality)
- **high** - 4:1 pixel ratio (best quality, slower)

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

   app.helpers.export_animation(
       obj=result,
       file_path="deformation.mp4",
       width=1920,
       height=1080,
       animation_format="mp4"  # "gif", "avi", "mp4", or "wmv"
   )

**Supported animation formats**

- **GIF** - Widely supported, good for web
- **AVI** - Uncompressed video
- **MP4** - Compressed video, good for presentations
- **WMV** - Windows Media Video format

.. note::
   Animation export requires that the result has been solved and has multiple steps or modes
   to animate. Attempting to export an animation of unsolved results raises a ``RuntimeError``.

Setting up camera views
-----------------------

The ``setup_view()`` method configures the camera orientation and view settings for your graphics
display. This is particularly useful before exporting images to ensure consistent viewpoints.

**Basic view orientations**

.. code:: python

   from ansys.mechanical.core import App

   app = App(globals=globals())
   # Import geometry first
   app.helpers.import_geometry("path/to/geometry.x_t")

   # Set isometric view
   app.helpers.setup_view(orientation="iso")

   # Set front view
   app.helpers.setup_view(orientation="front")

**Available orientations**

- ``"iso"`` - Isometric view (default)
- ``"front"`` - Front view
- ``"back"`` - Back view
- ``"top"`` - Top view
- ``"bottom"`` - Bottom view
- ``"left"`` - Left side view
- ``"right"`` - Right side view

**View with rotation**

Add rotation to any standard view:

.. code:: python

   # Isometric view rotated 45 degrees around X axis
   app.helpers.setup_view(orientation="iso", rotation=45, axis="x")

   # Front view rotated 90 degrees around Y axis
   app.helpers.setup_view(orientation="front", rotation=90, axis="y")

   # Top view rotated 180 degrees around Z axis
   app.helpers.setup_view(orientation="top", rotation=180, axis="z")

**Controlling camera fit**

.. code:: python

   # Set view and fit to model (default)
   app.helpers.setup_view(orientation="iso", fit=True)

   # Set view without auto-fit
   app.helpers.setup_view(orientation="iso", fit=False)

**Advanced: Scene height**

Control the zoom level by setting the scene height:

.. code:: python

   # Requires Quantity type from Mechanical
   app.update_globals(globals())

   app.helpers.setup_view(
       orientation="iso",
       scene_height=Quantity(2.0, "in")
   )

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

   # Step 3: Set up the view
   app.helpers.setup_view(orientation="iso", fit=True)

   # Step 4: Export image
   app.helpers.export_image(
       obj=app.Model.Geometry,
       file_path="bracket_iso.png",
       width=1920,
       height=1080,
       resolution="enhanced"
   )

   # Step 5: Display it
   app.helpers.display_image("bracket_iso.png")

**Multiple view angles**

Export images from different angles for documentation:

.. code:: python

   from ansys.mechanical.core import App

   app = App(globals=globals())
   app.helpers.import_geometry("part.step")

   views = ["front", "top", "iso"]
   for view in views:
       app.helpers.setup_view(orientation=view)
       app.helpers.export_image(
           obj=app.Model.Geometry,
           file_path=f"part_{view}.png"
       )



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

**Invalid options**

.. code:: python

   try:
       app.helpers.setup_view(orientation="invalid")
   except ValueError as e:
       print(f"Invalid orientation: {e}")

Best practices
--------------

1. **Always check paths**: Use absolute paths or ``pathlib.Path`` objects for file operations
   to avoid path-related errors.

2. **Set up views before exporting**: Use ``setup_view()`` before ``export_image()`` to ensure
   consistent viewpoints across multiple exports.

3. **Use appropriate image formats**: PNG for technical documentation, JPG for presentations,
   EPS for publications.

4. **Handle errors gracefully**: Wrap helper method calls in try-except blocks to handle
   potential failures gracefully in production scripts.

5. **Verify imports**: After importing geometry or materials, verify the object state:

   .. code:: python

      geometry_import = app.helpers.import_geometry("part.x_t")
      if str(geometry_import.ObjectState) == "FullyDefined":
          print("Geometry imported successfully")
      else:
          print(f"Warning: Geometry state is {geometry_import.ObjectState}")
