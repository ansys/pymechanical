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
Install PyMechanical using `pip` with::

   pip install ansys-mechanical-core

For more details, see `PyMechanical - Install the package <https://mechanical.docs.pyansys.com/version/stable/getting_started/index.html>`_


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

Testing and Development
-----------------------
If you would like to test or contribute to the development of PyMechanical, please visit
`PyMechanical - Contributing <https://mechanical.docs.pyansys.com/version/stable/contributing.html>`_.

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
