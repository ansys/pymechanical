.. _ref_user_guide:


User guide
==========

This section contains in-depth guides organized by mode, plus shared scripting
fundamentals and CLI tools.

- **Embedding mode**—Using Mechanical directly in your Python process via the ``App`` class.
- **Remote session mode**—Launching Mechanical as a server and communicating via gRPC.
- **Scripting fundamentals**—Mechanical API concepts, recording, threading (applies to both modes).
- **CLI tools**—Command-line utilities for launching, discovering, and configuring Mechanical.

Not sure which mode to use? See :ref:`ref_choose_your_mode`.

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Embedding Mode

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
   :caption: Remote Session Mode

   remote_session/overview
   remote_session/server-launcher
   remote_session/grpc_security
   remote_session/pool

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Scripting Fundamentals (Both Modes)

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
