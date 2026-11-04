.. _ref_troubleshooting:

Troubleshooting
===============

This page covers common issues when launching or connecting to Mechanical.


Manually set the executable location
-------------------------------------

If PyMechanical cannot find your installation, set the path manually:

**On Windows**

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    exec_loc = "C:/Program Files/ANSYS Inc/v261/aisol/bin/winx64/AnsysWBU.exe"
    mechanical = launch_mechanical(exec_file=exec_loc)

**On Linux**

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    exec_loc = "/usr/ansys_inc/v261/aisol/.workbench"
    mechanical = launch_mechanical(exec_file=exec_loc)

If Mechanical still fails to launch, pass ``verbose_mechanical=True`` to print
debug output to the Python console.


Debug from the command line
----------------------------

.. code:: console

    ansys-mechanical -g --port 10000

If this command doesn't launch Mechanical, common causes include:

- License server setup issues
- Running behind a VPN
- Missing dependencies


Licensing issues
-----------------

`PADT <https://www.padtinc.com/>`_ has an `Ansys <https://www.padtinc.com/simulation/ansys-simulation-products/>`_
product section. Posts about licensing are common.

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
