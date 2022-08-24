===============
Getting Started
===============
To use PyMechanical, you need to have a local installation of Mechanical.  The
version of Mechanical installed will dictate the interface and features
available to you.

Visit `Ansys <https://www.ansys.com/>`_ for more information on
getting a licensed copy of Mechanical.


.. toctree::
   :hidden:
   :maxdepth: 2

   running_mechanical
   versioning
   docker
   faq
   wsl

************
Installation
************

Python Module
~~~~~~~~~~~~~
The ``ansys.mechanical.core`` package currently supports Python 3.6 through
Python 3.9 on Windows, Mac OS, and Linux.

Install the latest release from `PyPi
<https://pypi.org/project/ansys-mechanical-core/>`_ with:

.. code::

   pip install ansys-mechanical-core

Alternatively, install the latest from `PyMechanical GitHub
<https://github.com/pyansys/pymechanical/issues>`_ via:

.. code::

   pip install git+https://github.com/pyansys/pymechanical.git


For a local "development" version, install with:

.. code::

   git clone https://github.com/pyansys/pymechanical.git
   cd pymechanical
   pip install -e .

This will allow you to install the pymechanical ``ansys-mechanical-core`` module
and modify it locally and have the changes reflected in your setup
after restarting the Python kernel.


Offline Installation
~~~~~~~~~~~~~~~~~~~~
If you lack an internet connection on your install machine, the recommended way
of installing PyMechanical is downloading the wheelhouse archive from the `Releases
Page <https://github.com/pyansys/pymechanical/releases>`_ for your corresponding
machine architecture.

Each wheelhouse archive contains all the python wheels necessary to install
PyMechanical from scratch on Windows and Linux for Python 3.7 and 3.9. You can install
this on an isolated system with a fresh python or on a virtual environment.

For example, on Linux with Python 3.7, unzip it and install it with the following:

.. code::

   unzip PyMechanical-v0.62.dev1-wheelhouse-Linux-3.7.zip wheelhouse
   pip install ansys-mechanical-core -f wheelhouse --no-index --upgrade --ignore-installed

If you're on Windows with Python 3.9, unzip to a ``wheelhouse`` directory and
install using the same command as above.

Consider installing using a `virtual environment
<https://docs.python.org/3/library/venv.html>`_.


Ansys Software Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~
For the latest features, you will need a copy of Mechanical 2023R1
installed locally, but PyMechanical is compatible with Mechanical 2023R1 and newer
on Windows and Linux.

.. note::

    The latest versions of Ansys provide significantly better support
    and features.


Verify Your Installation
~~~~~~~~~~~~~~~~~~~~~~~~
Check that you can start Mechanical from Python by running:

.. code:: python

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mechanical = launch_mechanical()
    >>> print(mechanical)

    Ansys Mechanical [Ansys Mechanical Enterprise]
    Product Version:231
    Software build date:Wednesday, August 10, 2022 4:28:15 PM

If you see a response from the server, congratulations!  You're ready
to get started using Mechanical as a service.  For details regarding the
PyMechanical interface, see :ref:`ref_mechanical_user_guide`.
