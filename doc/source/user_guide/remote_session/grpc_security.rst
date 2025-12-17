.. _grpc_security:

Securing gRPC Connections
==========================

PyMechanical supports secure gRPC connections for remote Mechanical sessions. When
connecting to a Mechanical instance, it is important to ensure that the connection
is secure to protect sensitive data and comply with organizational security policies.

.. warning::
   **Secure connection compatibility**

   Secure connections (mTLS, WNUA) are only available starting from Ansys 24R2 with
   Service Pack 04 (SP4) or later. Starting from Ansys 26R1, secure connections are
   available out-of-the-box without requiring additional Service Packs.

   If you are using an Ansys release prior to 24R2 SP4, you must use insecure
   connections.

Version Support
---------------

.. list-table:: Transport Mode Support by Version and Platform
   :header-rows: 1
   :widths: 20 20 30 30

   * - Version
     - Service Pack
     - Windows Support
     - Linux Support
   * - 24R1 (241)
     - All
     - insecure only
     - insecure only
   * - 24R2 (242)
     - SP0-SP3
     - insecure only
     - insecure only
   * - 24R2 (242)
     - **SP4+**
     - insecure, **wnua**, mtls
     - insecure, mtls
   * - 25R1 (251)
     - SP0-SP3
     - insecure only
     - insecure only
   * - 25R1 (251)
     - **SP4+**
     - insecure, **wnua**, mtls
     - insecure, mtls
   * - 25R2 (252)
     - SP0-SP3
     - insecure only
     - insecure only
   * - 25R2 (252)
     - **SP4+**
     - insecure, **wnua**, mtls
     - insecure, mtls
   * - 26R1 (261)
     - All
     - insecure, **wnua**, mtls
     - insecure, mtls

Transport Modes
---------------

PyMechanical supports the following transport modes for gRPC connections.
For more information on securing gRPC connections in PyAnsys, see
`Securing gRPC connections <https://tools.docs.pyansys.com/version/stable/user_guide/secure_grpc.html>`_
in the PyAnsys Tools documentation.

mTLS (Mutual TLS)
~~~~~~~~~~~~~~~~~

Mutual Transport Layer Security (mTLS) is a security protocol that ensures both the
client and server authenticate each other using digital certificates, providing a
high level of security for the connection.

.. note::
   mTLS is recommended for production use, especially when connecting over networks.

.. code-block:: python

   from ansys.mechanical.core import launch_mechanical

   # Option 1: Connect using mTLS with certificates
   mechanical = launch_mechanical(
       port=10000,
       transport_mode="mtls",
       certs_dir="/path/to/certificates"
   )

**Use cases:**

- Cross-platform secure connections (Windows and Linux)
- High-security requirements
- Remote connections over networks
- Linux-based deployments

For information on generating the required certificates, see
`Generating certificates for mTLS <https://tools.docs.pyansys.com/version/stable/user_guide/secure_grpc.html#generating-certificates-for-mtls>`_.
Ensure certificate files (``ca.crt``, ``client.crt``, ``client.key``) are placed in the
directory specified by ``certs_dir``.

WNUA (Windows Named User Authentication)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Windows Named User Authentication (WNUA) provides a secure connection mechanism
for Windows machines using built-in Windows credentials to verify that the service
owner and client connection owner are the same.

.. note::
   WNUA is only supported on Windows-based systems. It is the default transport mode
   for Windows with SP4+ or 26R1+.

.. code-block:: python

   from ansys.mechanical.core import launch_mechanical

   # Option 1: Connect using WNUA (Windows only)
   mechanical = launch_mechanical(port=10000, transport_mode="wnua")

**Use cases:**

- Windows-based local or remote deployments
- Enterprise environments with Windows authentication
- Simplified secure connections without certificate management

Insecure Mode
~~~~~~~~~~~~~

Insecure mode does not provide any security measures to protect data transmitted
between the client and server.

.. warning::
   Insecure connections do not encrypt data and should only be used in trusted
   environments for development and testing purposes. This mode is **not recommended
   for production use**.

.. code-block:: python

   from ansys.mechanical.core import launch_mechanical

   # Option 1: Connect using insecure mode (all versions)
   mechanical = launch_mechanical(port=10000, transport_mode="insecure")

**Use cases:**

- Development and testing in trusted environments
- Legacy versions without SP4 support (pre-24R2 SP4)
- Debugging connection issues

Connecting with Secure Transport Modes
---------------------------------------

Using launch_mechanical()
~~~~~~~~~~~~~~~~~~~~~~~~~~

The :func:`~ansys.mechanical.core.launch_mechanical` function accepts the following
security-related parameters:

.. code-block:: python

   from ansys.mechanical.core import launch_mechanical

   mechanical = launch_mechanical(
       port=10000,                        # Port number
       transport_mode="wnua",             # One of: insecure, wnua, mtls
       grpc_host="localhost",             # gRPC host (default: localhost)
       certs_dir="/path/to/certs"         # Certificate directory (required for mtls)
   )

**Parameters:**

- ``port`` (int): Port number for gRPC server.
- ``transport_mode`` (str): One of ``"insecure"``, ``"wnua"``, or ``"mtls"``.
  Default is ``"wnua"`` on Windows with SP4+, ``"mtls"`` on Linux with SP4+, or
  ``"insecure"`` for older versions.
- ``grpc_host`` (str): Host address for gRPC connection (default: ``"localhost"``).
- ``certs_dir`` (str): Path to certificate directory (required for mTLS mode).

Using the CLI
~~~~~~~~~~~~~

The ``ansys-mechanical`` command-line interface supports the same security options:

.. code-block:: bash

   # Windows with WNUA (SP4+ required)
   ansys-mechanical -r 242 --port 10000 --transport-mode wnua

   # Linux with mTLS (SP4+ required)
   ansys-mechanical -r 242 --port 10000 --transport-mode mtls --certs-dir /path/to/certs

   # Insecure mode (all versions)
   ansys-mechanical -r 241 --port 10000 --transport-mode insecure

**CLI Options:**

- ``--port PORT``: Port number for gRPC server
- ``--transport-mode {wnua,mtls,insecure}``: Transport security mode
- ``--grpc-host HOST``: gRPC host address (default: ``localhost``)
- ``--certs-dir PATH``: Certificate directory path (required for mTLS)

Usage Examples
--------------

Example 1: Secure Connection on Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ansys.mechanical.core import launch_mechanical

   # On Windows with SP4+, defaults to WNUA
   mechanical = launch_mechanical(port=10000)

   # Or explicitly specify WNUA
   mechanical = launch_mechanical(port=10000, transport_mode="wnua")

Example 2: Secure Connection with mTLS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ansys.mechanical.core import launch_mechanical

   # mTLS with certificate directory
   mechanical = launch_mechanical(
       port=10000,
       transport_mode="mtls",
       certs_dir="/opt/mechanical/certs"
   )

Example 3: Insecure Mode for Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ansys.mechanical.core import launch_mechanical

   # For development/testing only
   mechanical = launch_mechanical(port=10000, transport_mode="insecure")

Example 4: Custom Host and Port
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ansys.mechanical.core import launch_mechanical

   # Bind to specific network interface
   mechanical = launch_mechanical(
       port=50051,
       grpc_host="0.0.0.0",
       transport_mode="wnua"
   )

Certificate Management
----------------------

When using mTLS mode, the certificate directory specified by ``certs_dir`` must contain
the following files:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - File
     - Description
   * - ``ca.crt``
     - Certificate Authority (CA) certificate to verify server certificates
   * - ``client.crt``
     - Client identity certificate
   * - ``client.key``
     - Client private key

For instructions on generating these certificates using OpenSSL, see
`Generating certificates for mTLS <https://tools.docs.pyansys.com/version/stable/user_guide/secure_grpc.html#generating-certificates-for-mtls>`_.

Refer to your organization's security policies for certificate generation and management.

Troubleshooting
---------------

Version Detection Issues
~~~~~~~~~~~~~~~~~~~~~~~~

If you see warnings about version detection:

.. code-block:: text

   Warning: Unable to detect version. Using insecure mode.

**Solution:** Specify the version explicitly:

.. code-block:: python

   mechanical = launch_mechanical(
       version=242,
       port=10000,
       transport_mode="wnua"
   )

Service Pack Not Supported
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you see errors about transport mode not being supported:

.. code-block:: text

   Version 242 does not support wnua transport mode. Only 'insecure' mode is available.

**Solution:** This indicates your Mechanical installation does not have Service Pack 04 or later.
Either upgrade to SP4+ or use insecure mode:

.. code-block:: python

   mechanical = launch_mechanical(port=10000, transport_mode="insecure")

WNUA on Linux
~~~~~~~~~~~~~

If you try to use WNUA on Linux:

.. code-block:: text

   'wnua' transport mode is not available on Linux.

**Solution:** Use mTLS or insecure mode instead:

.. code-block:: python

   # Use mTLS on Linux
   mechanical = launch_mechanical(
       port=10000,
       transport_mode="mtls",
       certs_dir="/path/to/certs"
   )

Missing Certificates for mTLS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you see errors about missing certificates:

.. code-block:: text

   --certs-dir is required when using 'mtls' transport mode.

**Solution:** Provide the path to your certificate directory:

.. code-block:: python

   mechanical = launch_mechanical(
       port=10000,
       transport_mode="mtls",
       certs_dir="/path/to/certificates"
   )

Best Practices
--------------

Use Secure Modes in Production
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Always use ``wnua`` (Windows) or ``mtls`` (Linux) in production environments.
Reserve ``insecure`` mode for development and testing in trusted networks only.

Explicitly Specify Transport Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For clarity and maintainability, explicitly specify the transport mode:

.. code-block:: python

   mechanical = launch_mechanical(port=10000, transport_mode="wnua")

Verify Service Pack Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ensure your Mechanical installation has Service Pack 04 or later (or 26R1+)
before attempting to use secure transport modes (``wnua`` or ``mtls``).

Secure Certificate Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using mTLS, store certificates securely and follow your organization's
security policies for certificate management. Never commit certificates to
version control.

Support Multiple Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~

If your code needs to support multiple Mechanical versions, detect the version
and choose the appropriate transport mode:

.. code-block:: python

   from ansys.mechanical.core import launch_mechanical
   from ansys.mechanical.core.misc import has_grpc_service_pack

   version = 242
   supports_sp4 = has_grpc_service_pack(version)

   if supports_sp4:
       mechanical = launch_mechanical(port=10000, transport_mode="wnua")
   else:
       mechanical = launch_mechanical(port=10000, transport_mode="insecure")

API Reference
-------------

For detailed API documentation, see:

- :func:`ansys.mechanical.core.launch_mechanical`
- :func:`ansys.mechanical.core.misc.has_grpc_service_pack`
