.. _ref_getting_started:

Getting started
===============

PyMechanical is part of the broader `PyAnsys <pyansys_>`_ initiative,
enabling the use of Ansys technologies directly from Python.
It allows users to integrate the Mechanical multiphysics solver
into custom applications via ``ansys-mechanical-core``, which provides a Python-friendly
interface to drive the software that facilitates the use of
:ref:`ref_user_guide_scripting` commands.


.. grid:: 1 2 2 2

    .. grid-item-card:: Background
        :padding: 2 2 2 2
        :link: ../architecture
        :link-type: doc
        :text-align: left

        Information on the application architecture of Mechanical and why there are two Python interfaces.

    .. grid-item-card:: Installation guide
        :padding: 2 2 2 2
        :link: installation
        :link-type: doc
        :text-align: left

        Instructions to install and verify PyMechanical.

    .. grid-item-card:: Launching PyMechanical
        :padding: 2 2 2 2
        :link: running_mechanical
        :link-type: doc
        :text-align: left

        Steps to run PyMechanical.

    .. grid-item-card:: Docker setup
        :padding: 2 2 2 2
        :link: docker
        :link-type: doc
        :text-align: left

        How to create Mechanical docker images.

    .. grid-item-card:: Windows Subsystem for Linux (WSL)
        :padding: 2 2 2 2
        :link: wsl
        :link-type: doc
        :text-align: left

        Using PyMechanical with Windows Subsystem for Linux.



.. toctree::
   :hidden:
   :maxdepth: 2

   ../architecture
   installation
   running_mechanical
   docker
   wsl