.. _ref_whatsnew:

What's new
==========

Discover the latest updates in PyMechanical, including new features,
performance enhancements, and bug fixes designed to improve your experience.

v0.11.x
-------

Launch GUI
^^^^^^^^^^

Open the current project with Mechanical GUI. 

.. code:: python

    from ansys.mechanical.core import App
    app = App()
    app.save()
    app.launch_gui()

Above code opens up the temporarily saved ``.mechdb`` or ``.mechdat`` files.
The files are deleted when GUI is closed . For more info check
`launch_gui() <../api/ansys/mechanical/core/embedding/launch_gui/index.html>`_ function

Opens up the specified project file.

.. code:: python

  launch_gui("path/to/project.mechdb")

Prints Mechanical project tree
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This feature let you see the heirachial Mechanical project tree.
It also shows whether an object is supressed or not.

.. code:: python

  import ansys.mechanical.core as mech
  app = mech.App()
  app.update_globals(globals())
  app.print_tree()

.. code:: shell

  ... ├── Project
  ... |  ├── Model
  ... |  |  ├── Geometry Imports
  ... |  |  ├── Geometry
  ... |  |  ├── Materials
  ... |  |  ├── Coordinate Systems
  ... |  |  |  ├── Global Coordinate System
  ... |  |  ├── Remote Points
  ... |  |  ├── Mesh

v0.10.x
-------

Visualize geometry in 3D
^^^^^^^^^^^^^^^^^^^^^^^^

Visualize imported geometry in 3D. This feature is available only from 24R1 or later.

.. code:: python

  import ansys.mechanical.core as mech

  app = mech.App(version=242)
  app.update_globals(globals())

  # Import the geometry

  # visualize
  app.plot()