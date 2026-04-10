.. image:: https://raw.githubusercontent.com/ansys/pymechanical/main/doc/source/_static/logo/pymechanical-logo.png
   :alt: PyMechanical logo
   :width: 580px


|pyansys| |pypi| |python| |GH-CI| |codecov| |MIT| |ruff| |pre-commit| |deep-wiki|

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

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://github.com/astral-sh/ruff
   :alt: Ruff

.. |pre-commit| image:: https://results.pre-commit.ci/badge/github/ansys/pymechanical/main.svg?style=flat
   :target: https://results.pre-commit.ci/latest/github/ansys/pymechanical/main
   :alt: pre-commit

.. |deep-wiki| image:: https://deepwiki.com/badge.svg
   :target: https://deepwiki.com/ansys/pymechanical
   :alt: Ask DeepWiki

Overview
--------

PyMechanical is a Python interface for `Ansys Mechanical <https://www.ansys.com/products/structures/ansys-mechanical>`_
(FEA software for structural engineering), enabling automation and integration
of simulation workflows from **2024 R2** and later.

PyMechanical provides two distinct modes of interaction:

* **Embedding mode** — Run Mechanical directly in your Python process via the ``App`` class.
  Full object-model access, fast startup, ideal for Jupyter notebooks and interactive scripting.
* **Remote session mode** — Launch Mechanical as a separate server process and communicate via gRPC.
  Process isolation, optional GUI, ideal for CI/CD, Docker, and automation.


Compatibility
~~~~~~~~~~~~~

* **Python**: 3.10 – 3.13
* **Mechanical**: 2024 R2 (v242) and later
* **Platforms**: Windows, Linux

Installation
------------

Install from PyPI::

   pip install ansys-mechanical-core

For graphics support::

   pip install ansys-mechanical-core[graphics]

For RPC functionality::

   pip install ansys-mechanical-core[rpc]

**Requirements:**

* Licensed copy of Ansys Mechanical (2024 R2 or later).
* For embedded mode: Local Mechanical installation required.
* For remote session mode: Network access to a running Mechanical instance.

Quick start
-----------

**Embedding mode:**

.. code:: python

   from ansys.mechanical.core import App

   app = App(globals=globals())
   print(app)

   # Access Mechanical objects directly
   Model.AddStaticStructuralAnalysis()

**Remote session mode:**

.. code:: python

   from ansys.mechanical.core import launch_mechanical

   mechanical = launch_mechanical()
   result = mechanical.run_python_script("2+3")
   print(result)  # Output: 5
   mechanical.exit()

**Connect to existing instance:**

.. code:: python

   from ansys.mechanical.core import connect_to_mechanical

   mechanical = connect_to_mechanical(port=10000)
   result = mechanical.run_python_script("Model.Name")
   print(result)


Troubleshooting
---------------

* **Connection refused**: Ensure Mechanical is running and the port is accessible.
* **License error**: Verify your Ansys license is properly configured.
* **Import error**: Check that ``ansys-pythonnet`` is installed (not ``pythonnet``).
* **Linux embedding**: Use ``mechanical-env`` to run Python scripts for embedded mode.

Documentation and support
-------------------------

* `Documentation <https://mechanical.docs.pyansys.com/>`_
* `Cheat sheet <https://cheatsheets.docs.pyansys.com/pymechanical_cheat_sheet.pdf>`_
* `Issues <https://github.com/ansys/pymechanical/issues>`_ — report bugs or request features
* `Discussions <https://github.com/ansys/pymechanical/discussions>`_ — ask questions
* `Contributing guide <https://mechanical.docs.pyansys.com/version/stable/contributing.html>`_