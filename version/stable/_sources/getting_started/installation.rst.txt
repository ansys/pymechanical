.. _ref_installation:

Installation guide
==================

To use PyMechanical, a licensed copy of Ansys Mechanical must be installed locally.
The installed version determines the available interface and features.
PyMechanical is compatible with Mechanical **2024 R1** and later on Windows
and Linux. If you face any issues while setting up or using PyMechanical,
see :ref:`FAQs <faq>` and :ref:`Known issues and limitations <ref_known_issues_and_limitation>`.

Install Mechanical
------------------

Mechanical is installed by default from the Ansys standard installer.
When you run the standard installer, look under the **Structural Mechanics**
heading to verify that the **Mechanical Products** checkbox is selected.
Although options in the standard installer might change, this image provides
a reference:

.. figure:: ../images/unified_install_2023R1.jpg
    :width: 400pt

Install the package
-------------------

The latest ``ansys.mechanical.core`` package supports Python 3.10 through
Python 3.14 on Windows, Linux, and Mac.

You should consider installing PyMechanical in a virtual environment.
For more information, see Python's
`venv -- Creation of virtual environments <https://docs.python.org/3/library/venv.html>`_.

Install the latest package from `PyPi
<https://pypi.org/project/ansys-mechanical-core/>`_ with this command:

.. code::

   pip install ansys-mechanical-core

Install offline
---------------

If you want to install PyMechanical on a computer without access to the internet,
you can download a wheelhouse archive that corresponds to your
machine architecture from the `Releases page <https://github.com/ansys/pymechanical/releases>`_
of the PyMechanical repository.

Each wheelhouse archive contains all the Python wheels necessary to install
PyMechanical from scratch on Windows and Linux for Python 3.10 through Python 3.14. You can install
a wheelhouse archive on an isolated system with a fresh Python installation or on a
virtual environment.

For example, on Linux with Python 3.10, unzip the wheelhouse archive and install it with
this code:

.. code::

   unzip ansys-mechanical-core-v0.12.dev0-wheelhouse-Linux-3.10 wheelhouse
   pip install ansys-mechanical-core -f wheelhouse --no-index --upgrade --ignore-installed

If you are on Windows with Python 3.10, unzip the ``ansys-mechanical-core-v0.12.dev0-wheelhouse-Windows-3.10``
wheelhouse archive to a ``wheelhouse`` directory and then install it using ``pip`` as
in the preceding example.

Verify your installation
------------------------

Verify that PyMechanical can find your Mechanical installation:

.. code:: pycon

   >>> from ansys.tools.common.path import find_mechanical
   >>> find_mechanical()
   ('C:/Program Files/ANSYS Inc/v261/aisol/bin/winx64/AnsysWBU.exe', 26.1)  # Windows
   ('/usr/ansys_inc/v261/aisol/.workbench', 26.1) # Linux

   >>> find_mechanical(version=261)  # for a specific version

If Ansys is installed in a non-default location, save the path manually:

.. code:: pycon

   >>> from ansys.tools.common.path import save_mechanical_path, get_mechanical_path
   >>> save_mechanical_path("/home/username/ansys_inc/v261/aisol/.workbench")
   >>> print(get_mechanical_path())
   /home/username/ansys_inc/v261/aisol/.workbench

Once the installation is found, verify that your chosen mode works:

.. tab-set::

    .. tab-item:: Remote Session

        .. code:: pycon

            >>> from ansys.mechanical.core import launch_mechanical
            >>> mechanical = launch_mechanical()
            >>> mechanical
            Ansys Mechanical [Ansys Mechanical Enterprise]
            Product Version:261
            Software build date: 02/03/2026 15:29:09

    .. tab-item:: Embedding

        .. code:: pycon

            >>> from ansys.mechanical.core import App
            >>> app = App()
            >>> print(app)
            Ansys Mechanical [Ansys Mechanical Enterprise]
            Product Version:261
            Software build date: 02/03/2026 15:29:09

        .. note::

           On Linux, prepend ``mechanical-env`` before starting Python:

           .. code:: shell

              $ mechanical-env python

If you are not sure which mode to choose, see :ref:`ref_choose_your_mode`.
