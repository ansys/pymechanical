.. _ref_getting_started:

Getting started
===============

PyMechanical is part of the broader `PyAnsys <pyansys_>`_ initiative,
enabling the use of Ansys technologies directly from Python.
It provides two modes for working with Mechanical:
**embedding mode** (in-process, full API access) and
**remote session mode** (separate process, gRPC).


.. grid:: 1 2 2 2

    .. grid-item-card:: Installation guide
        :padding: 2 2 2 2
        :link: installation
        :link-type: doc
        :text-align: left

        Install and verify PyMechanical.

    .. grid-item-card:: Choose your mode
        :padding: 2 2 2 2
        :link: choose_your_mode
        :link-type: doc
        :text-align: left

        Compare embedding and remote session modes. Pick the right one for your workflow.

    .. grid-item-card:: Launching PyMechanical
        :padding: 2 2 2 2
        :link: running_mechanical
        :link-type: doc
        :text-align: left

        Launch, connect, and run your first script in either mode.

    .. grid-item-card:: Docker setup
        :padding: 2 2 2 2
        :link: docker
        :link-type: doc
        :text-align: left

        Run Mechanical in Docker containers (remote session mode).

    .. grid-item-card:: Windows Subsystem for Linux (WSL)
        :padding: 2 2 2 2
        :link: wsl
        :link-type: doc
        :text-align: left

        Install and run PyMechanical on Linux via WSL.

    .. grid-item-card:: Troubleshooting
        :padding: 2 2 2 2
        :link: troubleshooting
        :link-type: doc
        :text-align: left

        Fix common launch, licensing, and VPN issues.

.. toctree::
   :hidden:
   :maxdepth: 2

   installation
   choose_your_mode
   running_mechanical
   troubleshooting
   docker
   wsl
   ../architecture
