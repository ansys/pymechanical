.. _using_standard_install:

Launching PyMechanical
======================

PyMechanical requires either a local or
remote instance of Mechanical to communicate with. This page describes
how to launch Mechanical in each mode.

.. tip::

   If you are not sure which mode to use, see :ref:`ref_choose_your_mode`.


.. _launch_remote_session:

Remote session mode
-------------------

In remote session mode, Mechanical runs as a separate server process and
uses gRPC to communicate with Python.

Launch from Python
~~~~~~~~~~~~~~~~~~

Use the
`launch_mechanical() <../api/ansys/mechanical/core/mechanical/index.html#mechanical.launch_mechanical>`_
method to launch and connect automatically:

.. code:: pycon

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mechanical = launch_mechanical()
    >>> mechanical


    Ansys Mechanical [Ansys Mechanical Enterprise]
    Product Version:261
    Software build date: 02/03/2026 15:29:09

To select a specific version:

.. code:: python

    exec_file_path = "C:/Program Files/ANSYS Inc/v261/aisol/bin/win64/AnsysWBU.exe"
    mechanical = launch_mechanical(exec_file=exec_file_path)

Launch from the command line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start Mechanical in server mode and connect manually:

.. code:: console

    $ ansys-mechanical --port 10000

For all CLI options, run ``ansys-mechanical --help`` or see :doc:`../user_guide/cli/ansys-mechanical`.

Connect to a running instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Connect to a local or remote Mechanical server:

.. code:: python

    from ansys.mechanical.core import Mechanical

    # Local — default IP (127.0.0.1) and port (10000)
    mechanical = Mechanical()

    # Remote — by IP address
    mechanical = Mechanical("192.168.0.1", port=10000)

    # Remote — by hostname
    mechanical = Mechanical("myremotemachine", port=10000)

Alternatively, use the
`connect_to_mechanical() <../api/ansys/mechanical/core/mechanical/index.html#mechanical.connect_to_mechanical>`_ method:

.. code:: python

    from ansys.mechanical.core import connect_to_mechanical
    mechanical = connect_to_mechanical("192.168.0.1", port=10000)

For more on remote sessions, see the :ref:`Remote session user guide <ref_user_guide_session>`.


.. _launch_embedding:

Embedding mode
--------------

In embedding mode, Mechanical uses `Python.NET <https://pythonnet.github.io/>`__.
to run directly inside your Python process. This gives you full object-model access with no network overhead.

Launch on Windows
~~~~~~~~~~~~~~~~~

.. code:: pycon

    >>> from ansys.mechanical.core import App
    >>> app = App()
    >>> app
    Ansys Mechanical [Ansys Mechanical Enterprise]
    Product Version:261
    Software build date: 02/03/2026 15:29:09

Launch on Linux
~~~~~~~~~~~~~~~

On Linux, certain environment variables must be set before Python starts.
Use the ``mechanical-env`` script shipped with PyMechanical:

.. code:: shell

   $ mechanical-env python

.. _debug-embedding-vscode-linux:

Debug with Visual Studio Code on Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On Linux, the Python debugger must see the same environment that ``mechanical-env`` sets when
you run ``mechanical-env python``. You can capture that environment once, store it in a file, and
point Visual Studio Code at it.

#. Install the `Python extension`_ for VS Code (provides the **debugpy** debugger).

#. From your project root, write the prepared environment to ``.vscode/.env``. Use the same
   ``-r`` or ``-p`` options you use for normal runs:

   .. code:: shell

      $ mechanical-env -r 261 env > .vscode/.env

#. Create ``.vscode/launch.json`` with a launch configuration that loads that file:

   .. code-block:: json

      {
          "version": "0.2.0",
          "configurations": [
              {
                  "name": "Python Debugger: Current File",
                  "type": "debugpy",
                  "request": "launch",
                  "program": "${file}",
                  "console": "integratedTerminal",
                  "envFile": "${workspaceFolder}/.vscode/.env"
              }
          ]
      }

#. Start **Run and Debug**, choose **Python Debugger: Current File**, and run your script.

.. note::

   Regenerate ``.vscode/.env`` if you change Ansys version, installation path, or ``mechanical-env``
   options. Consider adding ``.env`` to ``.gitignore`` if the file should not be shared.

.. _`Python extension`: https://marketplace.visualstudio.com/items?itemName=ms-python.python

Licensing issues
----------------

`PADT <https://www.padtinc.com/>`_ has an `Ansys <https://www.padtinc.com/simulation/ansys-simulation-products/>`_
product section. Posts about licensing are common.

If you are responsible for maintaining an Ansys license or have a personal installation
of Ansys, you likely can access the
`Licensing <https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/prod_page.html?pn=Licensing&pid=Licensing&lang=en>`_
section of the Ansys Help, where you can view or download the *Ansys, Inc. Licensing Guide* for
comprehensive licensing information.

VPN issues
----------

Sometimes, Mechanical has issues starting when VPN software is running. For more information,
access the `Mechanical Users Guide`_
in the Ansys Help.
