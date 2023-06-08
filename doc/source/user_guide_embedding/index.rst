.. _ref_user_guide_embedding:

==================
Embedded instances
==================
This section provides an overview of how you use PyMechanical to embed
an instance of Mechanical in Python.


..
   This toctreemust be a top-level index to get it to show up in
   pydata_sphinx_theme.

.. toctree::
   :maxdepth: 1
   :hidden:

   configuration
   globals
   logging


Overview
========
The :class:`Application <ansys.mechanical.core.embedding.Application>` class provides
a Mechanical instance:

.. code:: python

   from ansys.mechanical.core import App

   app = App()
   ns = app.DataModel.Project.Model.AddNamedSelection()

The :class:`Application <ansys.mechanical.core.embedding.Application>` class has access
to the global scripting entry points that are available from built-in Mechanical scripting:

* ExtAPI: ``Application.ExtAPI``
* DataModel: ``Application.DataModel``
* Model: ``Application.DataModel.Project.Model``
* Tree: ``Application.DataModel.Tree``
* Graphics: ``Application.ExtAPI.Graphics``

Besides scripting entry points, many other types and objects are available from
built-in Mechanical scripting. To learn how to import scripting entry points,
namespaces, and types, see :ref:`ref_embedding_user_guide_globals`.

Additional configuration
------------------------
By default, an instance of the :class:`Application <ansys.mechanical.core.embedding.Application>` class
is configured in the same way as Mechanical. To customize an instance, see
:ref:`ref_embedding_user_guide_configuration`.

Diagnosing problems with embedding
----------------------------------
In some cases, debugging why the embedded Mechanical instance isn't working requires additional logging.
See the :ref:`ref_embedding_user_guide_logging` for instructions on how to configure logging.

Running PyMechanical embedding scripts inside Mechanical with IronPython
------------------------------------------------------------------------
If your PyMechanical embedding script does not use any other third-party Python package, such as `NumPy`,
it is possible to adapt it so that it can run inside of Mechanical with IronPython. With scripting inside
Mechanical's command line interface. For instance, the following script:

.. code:: python

  from ansys.mechanical.core import App, global_variables

  app = App()
  globals().update(global_variables(app))
  ns = DataModel.Project.Model.AddNamedSelection()
  ns.Name = "Jarvis"

can be converted to a Python file, such as "file.py" with the following content:

.. code:: python

  ns = DataModel.Project.Model.AddNamedSelection()
  ns.Name = "Jarvis"

and run inside mechanical using the command line

**On Windows**

Open a command prompt and run this command:

.. code::

    "C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/AnsysWBU.exe -DSApplet -AppModeMech -script file.py"

.. note::
   PowerShell users can run the preceding command without including the opening and
   closing quotation marks.


**On Linux**

.. code::

    /usr/ansys_inc/v231/aisol/.workbench -DSApplet -AppModeMech -nosplash -notabctrl -script file.py

Add the command line argument `-b` to run the script in batch mode.
