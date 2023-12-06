.. _ref_getting_started:

===============
Getting Started
===============

To run PyMechanical, you must have a licensed copy of Ansys Mechanical
installed locally. The version installed dictates the interface and
features that are available to you.

PyMechanical is compatible with Mechanical 2023 R1 and later on Windows
and Linux. Later releases provide significantly better support and features.

For more information, see the `Ansys Mechanical <https://www.ansys.com/products/structures/ansys-mechanical>`_
page on the Ansys website.

.. grid:: 2

    .. grid-item-card:: Installation guide  :fas:`fa-regular fa-screwdriver-wrench`
        :link: installation
        :link-type: doc
        :text-align: center

        Instructions for installing and setting up PyMechanical

    .. grid-item-card:: Versioning :fas:`fa-solid fa-code-compare`
        :link: versioning
        :link-type: doc
        :text-align: center


        Explains what are supported versions of Ansys Mechanical

.. grid:: 1

    .. grid-item-card:: Running standalone mechanical :fas:`fa-solid fa-gears`
        :link: running_mechanical
        :link-type: doc
        :text-align: center


        Mechanical -- how to run it and what to expect

.. grid:: 2

    .. grid-item-card:: Docker setup  :fab:`fa-brands fa-docker`
        :link: docker
        :link-type: doc
        :text-align: center


        Instructions for creating mechanical docker images

    .. grid-item-card:: WSL :fab:`fa-brands fa-ubuntu`
        :link: wsl
        :link-type: doc
        :text-align: center


        Installation with Windows Subsystem for Linux

.. grid:: 1

    .. grid-item-card:: Frequently Asked questions (FAQs) :fas:`fa-solid fa-clipboard-question`
        :link: faq
        :link-type: doc
        :text-align: center


        Frequently asked questions and answers


.. toctree::
   :hidden:
   :maxdepth: 2

   running_mechanical
   versioning
   docker
   faq
   wsl