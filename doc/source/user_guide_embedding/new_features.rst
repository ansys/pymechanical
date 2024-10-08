.. _ref_embedding_user_guide_new_features:

New features
============

This page showcases new features of the embedding instance of PyMechanical

* :ref:`The launch_gui function`
* :ref:`The ansys-mechanical-autocomplete command`

The launch_gui function
-----------------------

The `launch_gui() <../api/ansys/mechanical/core/embedding/launch_gui/index.html>`_ function
graphically launches the current state of the embedded instance the
`App <../api/ansys/mechanical/core/embedding/app/App.html>`_ has been saved.

Process
~~~~~~~

#. Save the active mechdb file.
#. Save a new mechdb file with a temporary name.
#. Open the original mechdb file from step 1.
#. Launch the GUI for the mechdb file with a temporary name from step 2.
#. Determine what to do with the temporary mechdb file.

   * Delete the temporary file (default option).
      * Remove the temporary mechdb file and folder when the GUI is closed.

   * Keep the temporary file.
      * Let the user know that the GUI mechdb will not automatically get cleaned up.

This setup automatically deletes the temporary mechdb file when the GUI is closed:

.. code:: python

    import ansys.mechanical.core as pymechanical

    app = pymechanical.App()
    app.save()
    app.launch_gui()

This setup does not delete the temporary mechdb file when the GUI is closed:

.. code:: python

    import ansys.mechanical.core as pymechanical

    app = pymechanical.App()
    app.save()
    app.launch_gui(delete_tmp_on_close=False)


The ansys-mechanical-autocomplete command
-----------------------------------------

Description about command
