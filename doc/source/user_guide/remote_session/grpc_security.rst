.. _grpc_security:

Securing gRPC Connections
==========================

PyMechanical supports secure gRPC connections using mTLS, WNUA, or insecure modes.

.. warning::
   Secure connections (mTLS, WNUA) require Ansys 24R2 SP4+ or Ansys 26R1+.
   Earlier versions only support insecure mode.

Version Support
---------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Version
     - Service Pack
     - Windows
     - Linux
   * - < 24R2 SP4
     - Any
     - insecure only
     - insecure only
   * - 24R2+ / 25R1+ / 25R2+
     - SP4+
     - insecure, **wnua**, mtls
     - insecure, mtls
   * - 26R1+
     - All
     - insecure, **wnua**, mtls
     - insecure, mtls

Transport Modes
---------------

**mTLS (Mutual TLS)** - Recommended for production. Uses certificates for mutual authentication.

.. code-block:: python

   mechanical = launch_mechanical(
       port=10000,
       transport_mode="mtls",
       certs_dir="/path/to/certs"
   )

Certificate directory must contain: ``ca.crt``, ``client.crt``, ``client.key``.
See `PyAnsys mTLS guide <https://tools.docs.pyansys.com/version/stable/user_guide/secure_grpc.html#generating-certificates-for-mtls>`_.

**WNUA (Windows Named User Authentication)** - Windows only. Uses Windows credentials.

.. code-block:: python

   mechanical = launch_mechanical(port=10000, transport_mode="wnua")

**Insecure** - No encryption. Development/testing only.

.. code-block:: python

   mechanical = launch_mechanical(port=10000, transport_mode="insecure")

CLI Usage
---------

.. code-block:: bash

   # Windows with WNUA
   ansys-mechanical --port 10000 --transport-mode wnua

   # Linux with mTLS
   ansys-mechanical --port 10000 --transport-mode mtls --certs-dir /path/to/certs

   # Insecure mode
   ansys-mechanical --port 10000 --transport-mode insecure

Connecting to Existing Instance
--------------------------------

Use ``launch_mechanical()`` with ``start_instance=False``:

.. code-block:: python

   # Connect with matching transport mode
   mechanical = launch_mechanical(
       start_instance=False,
       ip="127.0.0.1",
       port=10000,
       transport_mode="wnua"  # Must match server mode
   )

Or use the ``connect_to_mechanical()`` convenience function:

.. code-block:: python

   from ansys.mechanical.core import connect_to_mechanical

   # WNUA mode
   mechanical = connect_to_mechanical(
       ip="127.0.0.1",
       port=10000,
       transport_mode="wnua"
   )

   # mTLS mode
   mechanical = connect_to_mechanical(
       ip="127.0.0.1",
       port=10000,
       transport_mode="mtls",
       certs_dir="/path/to/certs"
   )

   # Insecure mode
   mechanical = connect_to_mechanical(
       ip="127.0.0.1",
       port=10000,
       transport_mode="insecure"
   )
