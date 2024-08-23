.. image:: /_static/logo/pymechanical-logo-light.png
   :class: only-light
   :alt: PyMechanical Logo

.. image:: /_static/logo/pymechanical-logo-dark.png
   :class: only-dark
   :alt: PyMechanical

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
   :target: https://codecov.io/gh/ansys/ansys-mechanical-core
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


Python API to interact with `Ansys Mechanical`_ (FEA software for structural engineering) from **2023R2** and later versions.

.. toctree::
   :hidden:
   :maxdepth: 3

   getting_started/index
   examples/index
   user_guide_session/index
   user_guide_embedding/index
   user_guide_scripting/index
   kil/index
   api/index
   contributing
   changelog

Introduction
------------

PyMechanical is part of the broader `PyAnsys <pyansys_>`_ initiative,
enabling the use of Ansys technologies directly from Python.
This allows users to integrate the Mechanical multiphysics solver
into custom applications.
The ``ansys-mechanical-core`` package presents a Python-friendly
interface to drive the software that facilitates the use of
:ref:`ref_user_guide_scripting` commands.

Install the latest package from `PyPi <https://pypi.org/project/ansys-mechanical-core/>`_ with command:

.. code::

   pip install ansys-mechanical-core

Mechanical scripting
--------------------

You can already perform scripting of Mechanical with Python from inside
Mechanical. PyMechanical leverages the same APIs as Mechanical but allows
you to run your automation from outside Mechanical. For more information
on using these APIs, see :ref:`ref_user_guide_scripting`.

Background
----------

PyMechanical contains two interfaces: a remote session and an embedded instance.
For information on the application architecture of Mechanical and why there are
two Python interfaces, see :ref:`ref_architecture`.

Remote session
^^^^^^^^^^^^^^

PyMechanical's  remote session is based on `gRPC <https://grpc.io/>`_.
Mechanical runs as a server, ready to respond to any clients.
PyMechanical provides a client to connect and make API
calls to this Mechanical server. For information on using a remote session, see
:ref:`ref_user_guide_session`.

Embedded instance
^^^^^^^^^^^^^^^^^

.. vale off

PyMechanical's embedded instance is based on `Python.NET <http://pythonnet.github.io/>`_.
Rather than starting a new process for Mechanical, a Mechanical object (which is
implemented in .NET) is directly loaded into Python memory using Python.NET. From
there, Mechanical's entire data model is available for use from Python code.
For information on using an embedded instance, see :ref:`ref_user_guide_embedding`.

.. vale on

Documentation and issues
------------------------

In the top right corner of the title bar, you can switch between the latest stable release,
development version, and previous versions of the documentation.

On the `PyMechanical Issues <https://github.com/ansys/pymechanical/issues>`_ page,
you can create issues to report bugs and request new features. On the `PyMechanical Discussions
<https://github.com/ansys/pymechanical/discussions>`_ page or the `Discussions <https://discuss.ansys.com/>`_
page on the Ansys Developer portal, you can post questions, share ideas, and get community feedback.

To reach the project support team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.

Contributions to this open source library are welcome. For more information,
see :ref:`ref_contributing`.