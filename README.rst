.. image:: https://raw.githubusercontent.com/ansys/pymechanical/main/doc/source/_static/logo/pymechanical-logo.png
   :alt: PyMechanical logo
   :width: 580px


|pyansys| |pypi| |python| |GH-CI| |codecov| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-mechanical-core.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-mechanical-core
   :alt: PyPI

.. |python| image:: https://img.shields.io/pypi/pyversions/ansys-mechanical-core?logo=pypi
   :target: https://pypi.org/project/ansys-mechanical-core
   :alt: Python

.. |codecov| image:: https://codecov.io/gh/ansys/pymechanical/branch/main/graph/badge.svg
   :target: https://app.codecov.io/gh/ansys/pymechanical
   :alt: Codecov

.. |GH-CI| image:: https://github.com/ansys/pymechanical/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/pymechanical/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black

.. |pre-commit| image:: https://results.pre-commit.ci/badge/github/ansys/pymechanical/main.svg?style=flat
   :target: https://results.pre-commit.ci/latest/github/ansys/pymechanical/main
   :alt: pre-commit

Overview
--------

PyMechanical brings Ansys Mechanical to Python. It enables your Python programs to use
Mechanical within Python's ecosystem. It includes the ability to:

- Connect to a remote Mechanical session
- Embed an instance of Mechanical directly as a Python object


Install the package
-------------------

Install PyMechanical using ``pip`` with::

   pip install ansys-mechanical-core

For more information, see `Install the package <https://mechanical.docs.pyansys.com/version/stable/getting_started/index.html>`_
in the PyMechanical documentation.


Dependencies
------------

You must have a licensed copy of `Ansys Mechanical <https://www.ansys.com/products/structures/ansys-mechanical>`_
installed. When using an embedded instance, that installation must be runnable from the
same computer as your Python program. When using a remote session, a connection to that
session must be reachable from your Python program.

Getting started
---------------

PyMechanical uses the built-in scripting capabilities of Mechanical. For information on the
scripting APIs available, see the `Scripting in Mechanical Guide
<https://ansyshelp.ansys.com/Views/Secured/corp/v242/en/act_script/act_script.html>`_ in the
Ansys Help.

Configuring the mechanical installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On a Windows system, the environment variable ``AWP_ROOT<ver>`` is configured when Mechanical is
installed, where ``<ver>`` is the Mechanical release number, such as ``242`` for release 2024 R2.
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
on Windows and Linux for version 2023 R2 and later. Here is an example:

.. code:: python

   import ansys.mechanical.core as pymechanical

   app = pymechanical.App()
   app.update_globals(globals())
   project_dir = DataModel.Project.ProjectDirectory

Documentation and issues
------------------------

Documentation for the latest stable release of PyMechanical is hosted at `PyMechanical documentation
<https://mechanical.docs.pyansys.com/>`_.

In the upper right corner of the documentation's title bar, there is an option for switching from
viewing the documentation for the latest stable release to viewing the documentation for the
development version or previously released versions.

You can also `view <https://cheatsheets.docs.pyansys.com/pymechanical_cheat_sheet.png>`_ or
`download <https://cheatsheets.docs.pyansys.com/pymechanical_cheat_sheet.pdf>`_ the
PyMechanical cheat sheet. This one-page reference provides syntax rules and commands
for using PyMechanical.

On the `PyMechanical Issues <https://github.com/ansys/pymechanical/issues>`_ page,
you can create issues to report bugs and request new features. On the `PyMechanical Discussions
<https://github.com/ansys/pymechanical/discussions>`_ page or the `Discussions <https://discuss.ansys.com/>`_
page on the Ansys Developer portal, you can post questions, share ideas, and get community feedback.

To reach the project support team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.

Testing and development
-----------------------

If you would like to test or contribute to the development of PyMechanical, see
`Contribute <https://mechanical.docs.pyansys.com/version/stable/contributing.html>`_ in
the PyMechanical documentation.