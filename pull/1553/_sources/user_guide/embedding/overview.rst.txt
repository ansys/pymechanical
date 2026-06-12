.. _ref_embedding_user_guide:


Overview
========

.. tip::

   **When to use embedding mode:** You want full object-model access, need fast
   in-process startup, are working in Jupyter notebooks or interactive scripting,
   or need to read and traverse the Mechanical data model directly in Python.
   For GUI support, process isolation, or CI/CD deployments, see
   :ref:`Remote session mode <ref_user_guide_session>` instead.

The :class:`App <ansys.mechanical.core.embedding.app.App>` class embeds an entire
instance of Mechanical directly in your Python process. There is no separate server
process or network communication. The Mechanical data model is directly accessible
from Python.

Here is how you create an embedded instance:

.. code:: python

   from ansys.mechanical.core import App

   app = App()
   ns = app.DataModel.Project.Model.AddNamedSelection()

To access Mechanical's global scripting entry points directly (without ``app.`` prefix),
pass ``globals()`` to the constructor:

.. code:: python

   from ansys.mechanical.core import App

   app = App(globals=globals())
   ns = DataModel.Project.Model.AddNamedSelection()
   ns.Name = "Jarvis"

The :class:`App <ansys.mechanical.core.embedding.app.App>` class has access to the
global scripting entry points that are available from built-in Mechanical scripting:

* ``ExtAPI``: ``Application.ExtAPI``
* ``DataModel``: ``Application.DataModel``
* ``Model``: ``Application.DataModel.Project.Model``
* ``Tree``: ``Application.DataModel.Tree``
* ``Graphics``: ``Application.ExtAPI.Graphics``

Besides scripting entry points, many other types and objects are available from
built-in Mechanical scripting. To learn how to import scripting entry points,
namespaces, and types, see :ref:`ref_embedding_user_guide_globals`.

The :class:`App <ansys.mechanical.core.embedding.app.App>` class supports much more
than basic object access. It includes higher-level wrapping that provides for better
scripting and interaction with Mechanical. For information on advanced methods, see
:ref:`ref_examples`.

.. seealso::

   Looking for remote session mode instead? See :ref:`ref_user_guide_session`.


Running PyMechanical embedding scripts inside Mechanical with IronPython
------------------------------------------------------------------------

If your PyMechanical embedding script does not use any other third-party Python package, such as `NumPy`,
it is possible to adapt it so that it can run inside of Mechanical with IronPython.
The scripting occurs inside Mechanical's command line interface. For instance, consider the following PyMechanical code:

.. code:: python

  from ansys.mechanical.core import App

  app = App(globals=globals())
  ns = DataModel.Project.Model.AddNamedSelection()
  ns.Name = "Jarvis"

The above code can be written as a Python file, such as ``file.py`` with only the following content:

.. code:: python

  ns = DataModel.Project.Model.AddNamedSelection()
  ns.Name = "Jarvis"

Because the file does not contain the PyMechanical import statements, you can run
``file.py`` using the command line inside Mechanical.

**Using command line interface (CLI)**

This can be achieved on both the Windows and Linux platforms using
``ansys-mechanical`` cli from the virtual environment where ``ansys-mechanical-core``
has been installed. Activate the virtual environment and then use CLI to run the scripts.
If multiple Mechanical versions are installed in the same system,
versions can be specified using ``-r`` flag. Use ``-h`` for more information.

.. code::

    ansys-mechanical -i file.py

.. note::

   Alternately user can use the following commands in the command prompt of Windows and the terminal
   for Linux systems.

   **On Windows**

   .. code::

      "C:/Program Files/ANSYS Inc/v261/aisol/bin/winx64/AnsysWBU.exe -DSApplet -AppModeMech -script file.py"

   PowerShell users can run the preceding command without including the opening and
   closing quotation marks.

   **On Linux**

   .. code::

      /usr/ansys_inc/v261/aisol/.workbench -DSApplet -AppModeMech -script file.py

   On either Windows or Linux, add the command line argument ``-b`` to run the script in batch mode.
