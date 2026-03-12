.. _grpc_security:

Secure gRPC connections
=======================

PyMechanical supports gRPC connections using mTLS, WNUA, or insecure modes.

.. _transport_modes:

Transport mode comparison
^^^^^^^^^^^^^^^^^^^^^^^^^

.. _mtls_mode:

**mTLS (Mutual TLS)**

Provides certificate-based mutual authentication and encryption. Both server and client must possess valid certificates signed by the same Certificate Authority (CA). This mode is platform-independent and recommended for production deployments requiring strong security.

*Authentication mechanism:* Both parties validate each other's certificates against a trusted CA. The connection is rejected if either certificate is invalid or untrusted.

*Encryption:* All data transmitted is encrypted using TLS protocol.

*Cross-platform:* Works on Windows and Linux.

*Network scope:* Can operate across any network including the internet, cloud deployments, and remote connections.

.. _wnua_mode:

**WNUA (Windows Named User Authentication)**

Windows-only mode that authenticates using the current Windows user's credentials through SSPI/Negotiate protocol. Provides authentication based on Windows identity but does not encrypt the data channel.

*Authentication mechanism:* The client authenticates as the currently logged-in Windows user. Only the same Windows user account can connect to the server, regardless of which machine they're connecting from within the domain/workgroup.

*Encryption:* Authentication is secure, but the data channel is **not encrypted**.

*Platform restriction:* Windows only. Both server and client must be Windows systems.

*Network scope:* Limited to Windows domain/workgroup networks. Does not work across domain boundaries without proper trust relationships.

*Access control:* Only the same Windows user who started the server can connect, even from different machines.

.. _insecure_mode:

**Insecure**

Provides no authentication or encryption. Any client that can reach the network port can connect without credentials.

*Authentication mechanism:* None. Any client can connect.

*Encryption:* None. All data is transmitted in plaintext.

*Security risk:* Suitable only for local development on trusted machines. Never use in production or on untrusted networks.

.. _host_and_ip:

Host binding
^^^^^^^^^^^^

The server's host address determines which network interfaces accept connections:

- **127.0.0.1 (localhost)**: Listens only on loopback. Only same-machine clients can connect. Traffic never leaves the machine.

- **0.0.0.0 (all interfaces)**: Listens on all network interfaces. Any client that can route to the machine can attempt connection, subject to transport mode authentication.

- **Specific IP** (e.g., 192.168.1.100): Listens only on that interface. Only clients that can route to that specific IP can attempt connection.

.. _ip_connectivity:

Client connectivity by IP and transport mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Server on 0.0.0.0 (all interfaces):**

- **mTLS**: Any client from any network with valid certificates can connect. Access controlled by certificate validation.
- **WNUA**: Only same Windows user can connect, from same or different machines within domain/workgroup. Different users blocked.
- **Insecure**: Anyone who can reach the port can connect. No restrictions. High security risk.

**Server on 127.0.0.1 (localhost only):**

- **mTLS**: Only local clients with valid certificates can connect.
- **WNUA**: Only same Windows user on same machine can connect.
- **Insecure**: Only local clients can connect. Relatively safe for development.

**Server on specific IP:**

- **mTLS**: Clients that can route to that IP with valid certificates can connect.
- **WNUA**: Same Windows user from machines that can route to that IP can connect.
- **Insecure**: Anyone who can route to that IP can connect. Security risk on shared networks.

**Summary table:**

.. list-table::
   :header-rows: 1
   :widths: 20 30 25 25

   * - Transport Mode
     - Authentication
     - Encryption
     - Connectivity Scope
   * - mTLS
     - Certificate-based
     - Yes (TLS)
     - Any network with valid certs
   * - WNUA
     - Windows user identity
     - No
     - Same Windows user only
   * - Insecure
     - None
     - No
     - Unrestricted (dangerous)

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
   **Breaking Change for Linux Users**

   If you have the **latest PyMechanical** with an **older version of Mechanical**
   that doesn't support secure connections (pre-2024 R2 or without required service pack):

   - **Linux**: The default transport mode is ``mtls``. Calling ``launch_mechanical()``
     without explicitly specifying ``transport_mode="insecure"`` **will fail** because
     old Mechanical versions don't support mtls.

   - **Windows**: The default transport mode is ``wnua``. A warning is issued and the
     connection **automatically falls back to insecure mode**. The connection succeeds,
     but you should explicitly specify ``transport_mode="insecure"`` to avoid the warning.

   **Required Action for Linux**: Always explicitly specify ``transport_mode="insecure"``
   when using old Mechanical versions:

   .. code-block:: python

      # Required for Mechanical 241 or versions without required SP
      mechanical = launch_mechanical(transport_mode="insecure")

.. note::
   **Forward Compatibility**

   If you have an **older version of PyMechanical** with a **newer version of Mechanical**
   that supports secure connections by default, you may need to update PyMechanical to
   take advantage of secure transport modes.

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

   When this variable is set and ``certs_dir`` is not explicitly specified, PyMechanical
   uses the path from this environment variable.

   Example (Windows PowerShell):

   .. code-block:: powershell

      [System.Environment]::SetEnvironmentVariable('ANSYS_GRPC_CERTIFICATES', 'C:\path\to\certs', 'User')

   Example (Linux):

   .. code-block:: bash

      export ANSYS_GRPC_CERTIFICATES=/path/to/certs

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