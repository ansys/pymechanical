.. _ref_user_guide:


User guide
==========

This section contains in-depth guides organized by mode, plus shared scripting
fundamentals and CLI tools.

- **Embedding mode**: Use Mechanical directly in your Python process with the ``App`` class.
- **Remote session mode**: Launch Mechanical as a server and communicate with gRPC.
- **Scripting fundamentals**: Explore Mechanical API concepts, recording, and threading, which
  are all topics applying to both modes.
- **CLI tools**: Discover command-line utilities for launching, discovering, and configuring Mechanical.

If you are not sure which mode to use, see :ref:`ref_choose_your_mode`.

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Embedding mode

   embedding/overview
   embedding/configuration
   embedding/globals
   embedding/licensing
   embedding/libraries
   embedding/logging
   embedding/pep8
   embedding/autocomplete

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Remote session mode

   remote_session/overview
   remote_session/server-launcher
   remote_session/grpc_security
   remote_session/pool

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Scripting fundamentals (both modes)

   scripting/overview
   scripting/threading

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Command Line Interface (CLI)

   cli/ansys-mechanical
   cli/ansys-mechanical-ideconfig
   cli/find-mechanical
   cli/mechanical-env
