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

    .. grid-item-card:: :fas:`fa-regular fa-screwdriver-wrench` Installation guide
        :padding: 2 2 2 2
        :link: installation
        :link-type: doc
        :text-align: center

        How to install and verify PyMechanical.

    .. grid-item-card:: :fas:`fa-solid fa-gears` Launching PyMechanical
        :padding: 2 2 2 2
        :link: running_mechanical
        :link-type: doc
        :text-align: center

        Steps to run PyMechanical.

    .. grid-item-card:: :fab:`fa-brands fa-docker` Docker setup
        :padding: 2 2 2 2
        :link: docker
        :link-type: doc
        :text-align: center

        How to create mechanical docker images.

    .. grid-item-card:: :fab:`fa-brands fa-ubuntu` WSL
        :padding: 2 2 2 2
        :link: wsl
        :link-type: doc
        :text-align: center

        Installing PyMechanical on Linux via WSL.


Mechanical scripting
--------------------

You can already perform scripting of Mechanical with Python from inside
Mechanical. PyMechanical leverages the same APIs as Mechanical but allows
you to run your automation from outside Mechanical. For more information
on using these APIs, see :ref:`ref_user_guide_scripting`.

Background
----------

.. grid:: 1 3 3 3

    .. grid-item-card:: :fas:`fa-regular fa-screwdriver-wrench` Architecture
        :padding: 2 2 2 2
        :link: ../architecture
        :link-type: doc
        :text-align: center

        Explains the need of 2 different interfaces such as remote session and embedded instance

    .. grid-item-card:: :fas:`fa-solid fa-gears` Remote session
        :padding: 2 2 2 2
        :link: ../user_guide_session/index
        :link-type: doc
        :text-align: center

        Based on gRPC. Mechanical runs as a server, ready to respond to any clients.
        PyMechanical provides a client to connect and make API calls to this Mechanical server.

    .. grid-item-card:: :fab:`fa-brands fa-docker` Embedded instance
        :padding: 2 2 2 2
        :link: /../user_guide_embedding/index
        :link-type: doc
        :text-align: center

        Based on Python.NET. Rather than starting a new process for Mechanical, a Mechanical object (which is implemented in .NET)
        is directly loaded into Python memory using Python.NET. 
        From there, Mechanical entire data model is available for use from Python code


.. grid:: 2
    :gutter: 2 2 3 4

    .. grid-item-card:: :fas:`fa-solid fa-clipboard-question` FAQs
        :link: faq
        :link-type: doc
        :text-align: center

        Frequently asked questions and answers.

    .. grid-item-card:: :fas:`fa-solid fa-bug` Known issues and limitations
        :link: ../kil/index
        :link-type: doc
        :text-align: center

        Known issues and limitations of Mechanical and PyMechanical.

.. toctree::
   :hidden:
   :maxdepth: 2

   installation
   running_mechanical
   docker
   wsl
   ../kil/index
   faq