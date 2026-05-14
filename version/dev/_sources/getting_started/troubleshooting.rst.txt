.. _ref_troubleshooting:

Troubleshooting
===============

This page covers common issues when launching or connecting to Mechanical.


Manually set the executable location
-------------------------------------

If PyMechanical cannot find your installation, set the path manually:

**On Windows**

.. code-block:: python

    from ansys.mechanical.core import launch_mechanical

    exec_loc = "C:/Program Files/ANSYS Inc/v261/aisol/bin/winx64/AnsysWBU.exe"
    mechanical = launch_mechanical(exec_file=exec_loc)

**On Linux**

.. code-block:: python

    from ansys.mechanical.core import launch_mechanical

    exec_loc = "/usr/ansys_inc/v261/aisol/.workbench"
    mechanical = launch_mechanical(exec_file=exec_loc)

If Mechanical still fails to launch, pass ``verbose_mechanical=True`` to print
debug output to the Python console.


Debug from the command line
----------------------------

.. code-block:: console

    ansys-mechanical -g --port 10000

If this command doesn't launch Mechanical, common causes include:

- License server setup issues
- Running behind a VPN
- Missing dependencies

.. _debug-embedding-vscode-linux:

Debug with Visual Studio Code on Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On Linux, the Python debugger must see the same environment that the ``mechanical-env`` scripts
set when you run ``mechanical-env python``. You can capture that environment once, store it in a
file, and point Visual Studio Code at it.

#. Install the `Python extension`_ for Visual Studio Code (provides the Python Debugger).

#. From your project root, write the prepared environment to ``.vscode/.env``. Use the same
   ``-r`` or ``-p`` options you use for normal runs:

   .. code-block:: console

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

   Regenerate ``.vscode/.env`` if you change the Ansys version, installation path, or ``mechanical-env``
   options. Add ``.env`` to ``.gitignore`` to avoid committing local environment settings to version control.

.. _`Python extension`: https://marketplace.visualstudio.com/items?itemName=ms-python.python


Licensing issues
-----------------

`PADT <https://www.padtinc.com/>`_ maintains an `Ansys <https://www.padtinc.com/simulation/ansys-simulation-products/>`_
product section that includes posts about licensing.

If you are responsible for maintaining an Ansys license or have a personal installation
of Ansys, you likely can access the
`Licensing <https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/prod_page.html?pn=Licensing&pid=Licensing&lang=en>`_
section of the Ansys Help, where you can view or download the *Ansys, Inc. Licensing Guide* for
comprehensive licensing information.


VPN issues
-----------

Sometimes, Mechanical has issues starting when VPN software is running. For more information,
see the `Mechanical Users Guide`_
in the Ansys Help.
