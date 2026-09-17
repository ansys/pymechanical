
mechanical-env
==============

The ``mechanical-env`` command-line tool configures the environment for **Ansys Mechanical**
and runs a specified command within that environment. It simplifies setting up environment
variables for automation, scripting, or launching custom tools.

.. note::

   This CLI is intended **for Linux systems only**.

Usage
------

.. code-block:: bash

   mechanical-env [-r <version>] [-p <path to installation>] [COMMAND]

Arguments
----------

``-r, --version <version>``
   Specify the version of Ansys Mechanical to use. Example: ``251`` or ``252``.

``-p, --path <path>``
   Specify the installation path of Ansys Mechanical if not using the default path.

``COMMAND``
   The command to execute once the environment is prepared. This could be
   ``python``, or a script such as ``python my_script.py``.

Examples
---------

Run Python with a specific version:

.. code-block:: bash

   mechanical-env -r 251 python

Run Python with a custom installation path:

.. code-block:: bash

   mechanical-env -p /usr/install/ansys_inc/v251 python

Run a Python script using a specific version:

.. code-block:: bash

   mechanical-env -r 252 python my_script.py
