.. _app:

App
==============

This section has helper scripts for  Embedded App .


.. contents::
   :local:
   :depth: 4

Create an embedded instance of Ansys Mechanical(and open an existing Mechanical File)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    from ansys.mechanical.core import App

    mechdat_path =r"D:\path\to\folder\bracket.mechdat" # or a mechdb file 

    print("about to launch pymechanical .....")
    # Create an instance of the app, extract the global API entry points
    # and merge them into your Python global variables.
    app = App(db_file = mechdat_path , version=251, globals=globals())
    print(app)


Create an embedded instance of Ansys Mechanical(and import a Geometry File)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    import os
    from ansys.mechanical.core import App

    print("about to launch pymechanical .....")
    # Create an instance of the app, extract the global API entry points
    # and merge them into your Python global variables.
    app = App( version=251, globals=globals())
    print(app)

    geom_file_path = r"D:\path\to\folder\frame.stp"


    geometry_import = Model.GeometryImportGroup.AddGeometryImport()
    geometry_import_format = (Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic)
    geometry_import_preferences = (    Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences())
    geometry_import_preferences.ProcessLines = True
    geometry_import_preferences.NamedSelectionKey = ""
    geometry_import_preferences.ProcessNamedSelections = True
    geometry_import_preferences.ProcessMaterialProperties = True
    geometry_import.Import(    geom_file_path, geometry_import_format, geometry_import_preferences)

    app.save(os.path.join(os.getcwd(),"temp", "frame.mechdb" ))

To Plot and Print the Tree (To check model so far)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    app.plot()

.. code:: python

    app.print_tree(Model)


To Launch UI (To check model so far)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    app.save()

    app.launch_gui()
    # Launch the GUI and do not keep the temporary `.mechdb` file when the GUI is closed
    # app.launch_gui(delete_tmp_on_close=True)

    # Manually Close GUI after checking.