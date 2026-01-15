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

PyMechanical is a Python interface for Ansys Mechanical, enabling automation and integration
of complex simulation analysis workflows. It supports both remote sessions and embedded instances.

Installation
------------

Install from PyPI::

   pip install ansys-mechanical-core

**Requirements:**

* Licensed copy of `Ansys Mechanical <https://www.ansys.com/products/structures/ansys-mechanical>`_ (2024 R1+ on Windows/Linux)
* For embedded instances: Local Mechanical installation required
* For remote sessions: Network access to a running Mechanical instance
* Python 3.10 - 3.13

Quick start
-----------

**Remote session:**

.. code:: python

   import ansys.mechanical.core as pymechanical

   mechanical = pymechanical.launch_mechanical()
   result = mechanical.run_python_script("2+3")

**Embedded instance:**
.. code:: python

   import ansys.mechanical.core as pymechanical

   app = pymechanical.App()
   app.update_globals(globals())
   print(DataModel.Project.ProjectDirectory)

Documentation and support
-------------------------

* `Documentation <https://mechanical.docs.pyansys.com/>`_
* `Cheat sheet <https://cheatsheets.docs.pyansys.com/pymechanical_cheat_sheet.pdf>`_
* `Issues <https://github.com/ansys/pymechanical/issues>`_ - report bugs or request features
* `Discussions <https://github.com/ansys/pymechanical/discussions>`_ - ask questions
* `Contributing guide <https://mechanical.docs.pyansys.com/version/stable/contributing.html>`_