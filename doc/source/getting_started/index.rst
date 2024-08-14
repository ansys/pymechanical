.. _ref_getting_started:

Getting started
===============

PyMechanical is part of the broader `PyAnsys <pyansys_>`_ initiative,
enabling the use of Ansys technologies directly from Python.
This allows users to integrate the Mechanical multiphysics solver
into custom applications.
The ``ansys-mechanical-core`` package presents a Python-friendly
interface to drive the software that facilitates the use of
:ref:`ref_user_guide_scripting` commands.


.. grid:: 1 2 2 2

    .. grid-item-card:: :fas:`fa-regular fa-screwdriver-wrench` Background
        :padding: 2 2 2 2
        :link: ../architecture
        :link-type: doc
        :text-align: left

        Information on the application architecture of Mechanical and why there are two Python interfaces.

    .. grid-item-card:: :fas:`fa-regular fa-screwdriver-wrench` Mechanical Scripting
        :padding: 2 2 2 2
        :link: ../user_guide_scripting/index
        :link-type: doc
        :text-align: left

        PyMechanical uses the same Mechanical scripting APIs,
        allowing automation from outside Mechanical.

    .. grid-item-card:: :fas:`fa-regular fa-screwdriver-wrench` Installation guide
        :padding: 2 2 2 2
        :link: installation
        :link-type: doc
        :text-align: left

        How to install and verify PyMechanical.

    .. grid-item-card:: :fas:`fa-solid fa-gears` Launching PyMechanical
        :padding: 2 2 2 2
        :link: running_mechanical
        :link-type: doc
        :text-align: left

        Steps to run PyMechanical.

    .. grid-item-card:: :fab:`fa-brands fa-docker` Docker setup
        :padding: 2 2 2 2
        :link: docker
        :link-type: doc
        :text-align: left

        How to create mechanical docker images.

    .. grid-item-card:: :fab:`fa-brands fa-ubuntu` WSL
        :padding: 2 2 2 2
        :link: wsl
        :link-type: doc
        :text-align: left

        Installing PyMechanical on Linux via WSL.



.. toctree::
   :hidden:
   :maxdepth: 2

   installation
   running_mechanical
   docker
   wsl
   ../kil/index
   faq