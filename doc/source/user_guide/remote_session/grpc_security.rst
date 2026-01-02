.. _grpc_security:

Secure gRPC connections
=======================

PyMechanical supports secure gRPC connections using mTLS, WNUA, or insecure modes.

.. warning::
   Secure connections (mTLS, WNUA) require specific service packs for each version.
   Versions without the required service pack only support insecure mode.

Version and service pack requirements
--------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 30 30

   * - Version
     - Required SP for Secure
     - Windows (default: **wnua**)
     - Linux (default: **mtls**)
   * - 2024 R1 (241)
     - Not supported
     - insecure only
     - insecure only
   * - 2024 R2 (242)
     - **SP05+**
     - insecure, **wnua**, mtls
     - insecure, **mtls**
   * - 2025 R1 (251)
     - **SP04+**
     - insecure, **wnua**, mtls
     - insecure, **mtls**
   * - 2025 R2 (252)
     - **SP03+**
     - insecure, **wnua**, mtls
     - insecure, **mtls**
   * - 2026 R1+ (261+)
     - All SPs
     - insecure, **wnua**, mtls
     - insecure, **mtls**

.. note::
   - Ansys 2024 R1 (241) and earlier versions **only support insecure mode**.
   - If your installation does not have the required service pack listed above,
     only insecure mode is available.
   - To check your service pack version, look at the ``builddate.txt`` file in your
     Ansys installation directory.

.. warning::
   **Breaking Change**: Version mismatch behavior

   When using ``launch_mechanical()`` without explicitly specifying ``transport_mode``:

   - If you have a **newer version of PyMechanical** with an **older version of Mechanical**
     that doesn't support secure connections, the connection will fail.
   - If you have an **older version of PyMechanical** with a **newer version of Mechanical**
     that requires secure connections by default, the connection will fail.

   **Solution**: Always explicitly specify ``transport_mode`` to avoid compatibility issues:

   .. code-block:: python

      # For older Mechanical versions (241 or versions without required SP)
      mechanical = launch_mechanical(transport_mode="insecure")

      # For newer Mechanical versions with secure support
      mechanical = launch_mechanical(transport_mode="wnua")  # Windows
      mechanical = launch_mechanical(transport_mode="mtls")  # Linux

Transport modes
---------------

PyMechanical automatically selects the default transport mode based on your platform:
- **Windows**: WNUA (Windows Named User Authentication) - default
- **Linux**: mTLS (Mutual TLS) - default

You can override the default by explicitly specifying ``transport_mode``.

**mTLS (Mutual TLS)** - Recommended for production and default on Linux. Uses certificates for mutual authentication.

.. code-block:: python

   mechanical = launch_mechanical(
       port=10000,
       transport_mode="mtls",
       certs_dir="/path/to/certs"
   )

Certificate directory must contain: ``ca.crt``, ``client.crt``, ``client.key``.
See `PyAnsys mTLS guide <https://tools.docs.pyansys.com/version/stable/user_guide/secure_grpc.html#generating-certificates-for-mtls>`_.

**WNUA (Windows Named User Authentication)** - Windows only, default on Windows.

.. code-block:: python

   mechanical = launch_mechanical(port=10000, transport_mode="wnua")

**Insecure** - No encryption. Not recommended.

.. code-block:: python

   mechanical = launch_mechanical(port=10000, transport_mode="insecure")

CLI usage
---------

.. code-block:: bash

   # Windows with WNUA
   ansys-mechanical --port 10000 --transport-mode wnua

   # Linux with mTLS
   ansys-mechanical --port 10000 --transport-mode mtls --certs-dir /path/to/certs

   # Insecure mode
   ansys-mechanical --port 10000 --transport-mode insecure

If ``--transport-mode`` is not specified, the platform default is used.

Connect to an existing instance
--------------------------------

When connecting to an existing Mechanical instance, the transport mode must match the server's mode.

.. note::
   - **Windows**: Default is WNUA. You can also use mTLS or insecure.
   - **Linux**: Default is mTLS (WNUA is not available). You can also use insecure.
   - If you don't specify ``transport_mode``, the platform default is used.

Use ``launch_mechanical()`` with ``start_instance=False``:

.. code-block:: python

   # Connect with matching transport mode
   mechanical = launch_mechanical(
       start_instance=False,
       ip="127.0.0.1",
       port=10000,
       transport_mode="wnua"  # Must match server mode (Windows only)
   )

Or use the ``connect_to_mechanical()`` convenience function:

.. code-block:: python

   from ansys.mechanical.core import connect_to_mechanical

   # WNUA mode (Windows only, default on Windows)
   mechanical = connect_to_mechanical(
       ip="127.0.0.1",
       port=10000,
       transport_mode="wnua"
   )

   # mTLS mode (cross-platform, default on Linux)
   mechanical = connect_to_mechanical(
       ip="127.0.0.1",
       port=10000,
       transport_mode="mtls",
       certs_dir="/path/to/certs"
   )

   # Insecure mode (cross-platform, for development only)
   mechanical = connect_to_mechanical(
       ip="127.0.0.1",
       port=10000,
       transport_mode="insecure"
   )

Custom gRPC options
-------------------

Use ``grpc_options`` to pass custom channel options for advanced scenarios.

**Common use case**: Certificate hostname mismatch with ``grpc.default_authority``

When connecting via IP but certificate has CN=localhost:

.. code-block:: python

   mechanical = launch_mechanical(
       transport_mode="mtls",
       certs_dir="./certs",
       ip="127.0.0.1",  # Connecting via IP
       grpc_options=[("grpc.default_authority", "localhost")]  # Match certificate CN
   )

**Other options**:

.. code-block:: python

   mechanical = launch_mechanical(
       grpc_options=[
           ("grpc.keepalive_time_ms", 10000),
           ("grpc.keepalive_timeout_ms", 5000),
           ("grpc.http2.max_pings_without_data", 0),
       ]
   )

.. note::
   ``grpc.max_receive_message_length`` is automatically set and cannot be overridden.