PyMechanical
============
|pyansys| |python| |pypi| |GH-CI| |codecov| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/pypi/pyversions/ansys-mechanical-core?logo=pypi
   :target: https://pypi.org/project/ansys-mechanical-core
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-mechanical-core.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-mechanical-core
   :alt: PyPI

.. |codecov| image:: https://codecov.io/gh/pyansys/pymechanical/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/pyansys/ansys-mechanical-core
   :alt: Codecov

.. |GH-CI| image:: https://github.com/pyansys/pymechanical/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/pyansys/pymechanical/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black


Overview
--------
PyMechanical brings Ansys Mechanical to Python. It enables your Python programs to use
Mechanical within Python's ecosystem. It includes the ability to:

- Connect to a remote Mechanical session
- Embed an instance of Mechanical directly as a Python object


Install the package
-------------------

PyMechanical has three installation modes: user, developer, and offline.

Install in user mode
^^^^^^^^^^^^^^^^^^^^

Before installing PyMechanical in user mode, ensure that you have the latest
version of `pip`_ installed by running this command:

.. code:: bash

   python -m pip install -U pip

Then, install PyMechanical by running this command:

.. code:: bash

   python -m pip install ansys-mechanical-core

.. caution::

    PyMechanical is currently hosted in a private PyPI repository. You must provide the index
    URL to the private PyPI repository:

    * Index URL: ``https://pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple/``

    If access to this package registry is needed, email `pyansys.core@ansys.com <mailto:pyansys.core@ansys.com>`_
    to request access. The PyAnsys team can give you a read-only token to insert in ``${PRIVATE_PYPI_ACCESS_TOKEN}``.
    Once you have this token, run this command:

    .. code:: bash

        pip install ansys-mechanical-core --index-url=https://${PRIVATE_PYPI_ACCESS_TOKEN}@pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple/

Install in developer mode
^^^^^^^^^^^^^^^^^^^^^^^^^

Installing PyMechanical in developer mode allows
you to modify the source and enhance it.

.. note::

    Before contributing to the project, ensure that you are thoroughly familiar
    with the `PyAnsys Developer's Guide`_.

To install PyMechanical in developer mode, perform these steps:

#. Clone the ``pymechanical`` repository:

   .. code:: bash

      git clone https://github.com/pyansys/pymechanical

#. Access the ``pymechanical`` directory where the repository has been cloned:

   .. code:: bash

      cd pymechanical

#. Create a clean Python virtual environment and activate it:

   .. code:: bash

      # Create a virtual environment
      python -m venv .venv

      # Activate it in a POSIX system
      source .venv/bin/activate

      # Activate it in Windows CMD environment
      .venv\Scripts\activate.bat

      # Activate it in Windows Powershell
      .venv\Scripts\Activate.ps1

#. Ensure that you have the latest required build system tools:

   .. code:: bash

      python -m pip install -U pip tox flit twine

#. Install the project in editable mode:

   .. code:: bash

      # Install the minimum requirements
      python -m pip install -e .

      # Install the minimum + tests requirements
      python -m pip install -e .[tests]

      # Install the minimum + doc requirements
      python -m pip install -e .[doc]

      # Install all requirements
      python -m pip install -e .[tests,doc]

#. Verify your development installation:

    .. code:: bash

        tox


Install in offline mode
^^^^^^^^^^^^^^^^^^^^^^^

If you lack an internet connection on your installation machine (or
you do not have access to the private Ansys PyPI packages repository),
you should install PyMechanical by downloading the wheelhouse
archive from the `Releases Page <https://github.com/pyansys/pymechanical/releases>`_
for your corresponding machine architecture.

Each wheelhouse archive contains all the Python wheels necessary to install
PyMechanical from scratch on Windows, Linux, and MacOS from Python 3.7 to 3.11.
You can install a wheelhouse archive on an isolated system with a fresh Python
installation or on a virtual environment.

**On Linux**

This code shows how to unzip the wheelhouse archive and install PyMechanical on
Linux with Python 3.7:

.. code:: bash

    unzip ansys-mechanical-core-v0.7.dev3-wheelhouse-Linux-3.7.zip wheelhouse
    pip install ansys-mechanical-core -f wheelhouse --no-index --upgrade --ignore-installed


**On Windows**

If you're on Windows with Python 3.9, unzip the wheelhouse archive to a wheelhouse
directory and then install PyMechanical using the preceding command.

Consider installing into a `virtual environment <https://docs.python.org/3/library/venv.html>`_.

Dependencies
------------

You must have a licensed copy of Ansys Mechanical installed. When using an embedded instance,
that installation must be runnable from the same computer as your Python program. When using
a remote session, a connection to that session must be reachable from your Python program.


Getting started
---------------

PyMechanical uses the built-in scripting capabilities of Mechanical. For information on the
scripting APIs available, see the `Scripting in Mechanical Guide
<https://ansyshelp.ansys.com/Views/Secured/corp/v231/en/act_script/act_script.html>`_ in the
Ansys Help.

Configuring the Mechanical installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
On a Windows system, the environment variable ``AWP_ROOT<ver>`` is configured when Mechanical is
installed, where ``<ver>`` is the Mechanical release number, such as ``231`` for release 2023 R1.
PyMechanical automatically uses this environment variable (or variables if there are multiple
installations of different versions) to locate the latest Mechanical installation. On a Linux
system, you must configure the ``AWP_ROOT<ver>`` environment variable to point to the
absolute path of a Mechanical installation.

Starting a remote session
^^^^^^^^^^^^^^^^^^^^^^^^^
To start a remote session of Mechanical on your computer from Python, use the ``launch_mechanical()``
method. This methods returns an object representing the connection to the session:

.. code:: python

   import ansys.mechanical.core as pymechanical

   mechanical = pymechanical.launch_mechanical()

Running commands on the remote session
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Given a connection to a remote session, you can send an IronPython script. This uses the built-in
scripting capabilities of Mechanical. Here is an example:

.. code:: python

    result = mechanical.run_python_script("2+3")
    result = mechanical.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")


Using an embedded instance of Mechanical as a Python object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PyMechanical also supports directly embedding an instance of Mechanical as a Python object.
In this mode, there is no externally running instance of Mechanical. This feature is supported
on Windows for version 2023 R1 and later, and it will be supported on Linux for version 2023 R2
and later. Here is an example:

.. code:: python

   import ansys.mechanical.core as pymechanical

   app = pymechanical.App()
   result = app.ExtAPI.DataModel.Project.ProjectDirectory

Testing
-------

This project takes advantage of `tox`_. This tool automates common
development tasks (similar to Makefile), but it is oriented towards Python
development.

Using ``tox``
^^^^^^^^^^^^^

While Makefile has rules, ``tox`` has environments. In fact, ``tox`` creates its
own virtual environment so that anything being tested is isolated from the project
to guarantee the project's integrity.

The following environment commands are provided:

- **tox -e style**: Checks for coding style quality.
- **tox -e py**: Checks for unit tests.
- **tox -e py-coverage**: Checks for unit testing and code coverage.
- **tox -e doc**: Checks for documentation-building process.


Raw testing
^^^^^^^^^^^

If required, from the command line, you can call style commands like
`black`_, `isort`_, and `flake8`_. You can also call unit testing commands like `pytest`_.
However, running these commands do not guarantee that your project is being tested
in an isolated environment, which is the reason why tools like ``tox`` exist.


Using ``pre-commit``
^^^^^^^^^^^^^^^^^^^^

The style checks implemented for PyMechanical take advantage of `pre-commit`_.
Developers are not forced but are encouraged to install this tool by running this
command:

.. code:: bash

    python -m pip install pre-commit && pre-commit install


Documentation
-------------

For building documentation, you can run the usual rules provided in the
`Sphinx`_ ``make`` file. Here is an example:

.. code:: bash

    #  build and view the doc from the POSIX system
    make -C doc/ html && your_browser_name doc/html/index.html

    # build and view the doc from CMD / PowerShell environment
    .\doc\make.bat clean
    .\doc\make.bat html
    start .\doc\_build\html\index.html


However, the recommended way of checking documentation integrity is to use
``tox``:

.. code:: bash

    tox -e doc && your_browser_name .tox/doc_out/index.html


Distributing
------------

If you would like to create either source or wheel files, start by installing
the building requirements and then executing the build module:

.. code:: bash

    python -m pip install -U pip
    python -m flit build
    python -m twine check dist/*


.. LINKS AND REFERENCES
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _pip: https://pypi.org/project/pip/
.. _pre-commit: https://pre-commit.com/
.. _PyAnsys Developer's Guide: https://dev.docs.pyansys.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _tox: https://tox.wiki/
