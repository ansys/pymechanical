.. _ref_user_guide:


User guide
==========

This section provides a general overview of PyMechanical and how you use it. It also contains
detailed how-to guides on specific topics. The user guide is divided into the following sections:

- **Mechanical Scripting** - Covers how to record scripts inside Mechanical, and threading.
- **How to** - Provides step-by-step instructions for configuring PyMechanical, using globals, logging, and more.
- **Command Line Interface (CLI)** - Details the CLI commands available for PyMechanical.
- **Remote session** - Explains how to use PyMechanical in a remote session.

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Mechanical Scripting

   scripting/overview
   scripting/threading


.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: How to

   howto/overview
   howto/configuration
   howto/globals
   howto/licensing
   howto/libraries
   howto/logging
   howto/pep8

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Command Line Interface (CLI)

   cli/ansys-mechanical
   cli/ansys-mechanical-ideconfig
   cli/find-mechanical
   cli/mechanical-env

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Remote session

   remote_session/overview
   remote_session/server-launcher
   remote_session/grpc_security
   remote_session/pool
