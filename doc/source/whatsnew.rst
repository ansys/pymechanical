.. _ref_whatsnew:

What's new
==========

Discover the latest updates in PyMechanical, including new features,
performance enhancements, and bug fixes designed to improve your experience.

v0.11.x
-------

Launch GUI
^^^^^^^^^^

Open the project files with Mechanical GUI.

.. code:: python

  launch_gui()

Opens up the saved ``.mechdb`` or ``.mechdat`` files.

Visualize geometry in 3D
^^^^^^^^^^^^^^^^^^^^^^^^

Visualize imported geometry in 3D. This feature is available only from 24R1 or later.

.. code:: python

  import ansys.mechanical.core as mech
  from ansys.mechanical.core.examples import delete_downloads, download_file

  app = mech.App(version=242)
  app.update_globals(globals())

  # Import the geometry

  # visualize
  app.plot()
