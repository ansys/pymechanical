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