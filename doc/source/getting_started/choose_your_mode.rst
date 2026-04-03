.. _ref_choose_your_mode:

Choose your mode
================

PyMechanical offers two distinct modes for interacting with Ansys Mechanical.
This page helps you decide which mode is right for your workflow.


.. _choose_mode_at_a_glance:

At a glance
------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 35
   :class: mode-comparison-table

   * - Aspect
     - **Embedding** (``App``)
     - **Remote Session** (``launch_mechanical``)
   * - Process model
     - Mechanical runs inside your Python process
     - Mechanical runs as a separate server process
   * - Communication
     - Direct .NET CLR interop (Python.NET)
     - gRPC over TCP/IP
   * - API style
     - Direct object access (full CRUD data model)
     - String-based via ``run_python_script()``
   * - GUI support
     - No—runs in batch mode only
     - Optional—set ``batch=False`` for GUI
   * - Platform
     - Windows natively; Linux requires ``mechanical-env``
     - Windows and Linux
   * - Concurrency
     - One instance per Python process
     - Multiple instances with ``LocalMechanicalPool``
   * - Best for
     - Jupyter notebooks, interactive scripting, deep integration
     - CI/CD pipelines, Docker, distributed automation
   * - Startup speed
     - Faster (in-process)
     - Slower (new process + gRPC handshake)
   * - Object model access
     - Full—read, create, update, delete objects directly
     - Limited—send scripts as strings, receive results as strings


.. _choose_mode_decision:

Which mode to use?
-------------------------

Use the following questions to guide your choice:

.. list-table::
   :header-rows: 1
   :widths: 60 20 20
   :class: mode-comparison-table

   * - Question
     - **Embedding**
     - **Remote**
   * - Do you need the Mechanical **GUI**?
     -
     - **Yes**
   * - Are you running inside a **Jupyter notebook**?
     - **Yes**
     -
   * - Do you need **full object model** access (read properties, traverse tree)?
     - **Yes**
     -
   * - Are you deploying in **CI/CD**, **Docker**, or containers?
     -
     - **Yes**
   * - Do you need **multiple simultaneous** Mechanical instances?
     -
     - **Yes** (pool)
   * - Do you want the **fastest startup** with no network overhead?
     - **Yes**
     -
   * - Do you need to connect to Mechanical running on a **different machine**?
     -
     - **Yes**
   * - Are you building a **distributed** or multi-user system?
     -
     - **Yes**


Once you've chosen your mode, see :doc:`running_mechanical` for launch instructions
and code examples for each mode.


.. _choose_mode_architecture:

How the modes work
-------------------

**Embedding mode** embeds the entire Mechanical application in memory inside
your Python process using Python.NET (.NET CLR interop). There is no separate
process or network communication. The Mechanical data model is directly available
in Python, giving you full CRUD (Create, Read, Update, Delete) access to the
object model.

**Remote session mode** launches Mechanical as a separate server process and
communicates with gRPC (Remote Procedure Call). Python sends commands as strings
using the ``run_python_script()`` method and receives results as strings. This provides
process isolation but does not expose the full object model directly.

.. dropdown:: Why can't remote sessions expose the full object model?
   :animate: fade-in-slide-down

   The Mechanical API is an object model, not a command-based API. Object models
   are designed for in-process use where you can directly read and write properties.
   Exposing an object model remotely would require Remote Method Invocation (RMI),
   which does not scale well for distributed systems. For this reason, the remote
   interface uses a string-based API while the embedded interface provides
   direct object access.

   For a deeper discussion, see :ref:`ref_architecture`.

.. seealso::

   - :doc:`../architecture` — Detailed technical architecture
   - :doc:`installation` — Install PyMechanical
   - :doc:`running_mechanical` — Launch and connect to Mechanical
