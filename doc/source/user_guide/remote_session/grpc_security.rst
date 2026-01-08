.. _grpc_security:

Secure gRPC connections
=======================

PyMechanical supports gRPC connections using mTLS, WNUA, or insecure modes.

**Transport mode comparison:**

- **mTLS**: Provides both authentication and encryption. Recommended for production environments.
- **WNUA** (Windows only): Provides authentication but not encryption.
- **Insecure**: No authentication or encryption. Not recommended.

See the table below for version-specific support and service pack requirements.

Version and service pack requirements
-------------------------------------

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
   **Breaking Change**: Version mismatch behavior on Linux

   **Windows users**: No breaking changes. The default WNUA mode works across all versions
   and does not require certificates or additional configuration.

   **Linux users**: Breaking change introduced due to mTLS default requiring certificates.

   When using ``launch_mechanical()`` on Linux without explicitly specifying ``transport_mode``:

   - If you have a **newer version of PyMechanical** (0.12.0+) with an **older version of Mechanical**
     (without required service pack), the connection will fail because PyMechanical defaults to mTLS
     but the old Mechanical version doesn't support it.
   - If you have an **older version of PyMechanical** (< 0.12.0) with a **newer version of Mechanical**
     (with required service pack), the connection may fail due to security mode mismatch.

   **Solution for Linux users**: Always explicitly specify ``transport_mode``:

   .. code-block:: python

      # For older Mechanical versions on Linux (241 or versions without required SP)
      mechanical = launch_mechanical(transport_mode="insecure")

      # For newer Mechanical versions on Linux with certificates configured
      mechanical = launch_mechanical(transport_mode="mtls", certs_dir="/path/to/certs")

   **Windows users** can continue using the default without changes:

   .. code-block:: python

      # Works on all Windows versions (WNUA default)
      mechanical = launch_mechanical()

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

.. note::
   **Environment Variable**: You can set the ``ANSYS_GRPC_CERTIFICATES`` environment variable
   to specify the default certificate directory for mTLS connections:

   - **Windows**: Set as a user-level environment variable only. System-level variables are ignored.
   - **Linux**: Can be set at any level (user or system).

   When this variable is set and ``certs_dir`` is not explicitly specified, PyMechanical will
   use the path from this environment variable.

   Example (Windows PowerShell):

   .. code-block:: powershell

      [System.Environment]::SetEnvironmentVariable('ANSYS_GRPC_CERTIFICATES', 'C:\path\to\certs', 'User')

   Example (Linux):

   .. code-block:: bash

      export ANSYS_GRPC_CERTIFICATES=/path/to/certs

**WNUA (Windows Named User Authentication)** - Platform-specific (Windows only, default mode).

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

   # Specify custom host for gRPC binding
   ansys-mechanical --port 10000 --transport-mode wnua --grpc-host 127.0.0.1

If ``--transport-mode`` is not specified, the platform default is used.

The ``--grpc-host`` option specifies the host address for the gRPC server to bind to.
It defaults to ``localhost`` for WNUA and insecure modes.

Connect to an existing instance
-------------------------------

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

When connecting via IP but certificate has ``CN=localhost``:

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