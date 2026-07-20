.. _ref_mcp_integration:

MCP integration
===============

`PyMechanical-MCP <https://mechanical-mcp.docs.pyansys.com/>`_ is a companion package that
exposes PyMechanical as a `Model Context Protocol (MCP) <https://modelcontextprotocol.io/>`_
server, letting AI assistants such as GitHub Copilot, Claude, and others automate Mechanical
simulations through natural language.

Install
-------

Install PyMechanical with the ``mcp`` optional extra:

.. note::

   ``ansys-mechanical-mcp`` requires Python 3.11 or later. On Python 3.10, the
   package is skipped silently during installation and the MCP server is unavailable.

.. code-block:: bash

   pip install ansys-mechanical-core[mcp]

Usage
-----

Start the MCP server (STDIO transport, default for VS Code and Claude Code):

.. code-block:: bash

   ansys-mechanical-mcp

For remote or server-style deployments use streamable HTTP transport:

.. code-block:: bash

   ansys-mechanical-mcp --transport http --http-host 127.0.0.1 --http-port 8080

To auto-connect to a running Mechanical instance on startup:

.. code-block:: bash

   ansys-mechanical-mcp --connect-on-startup --ip 127.0.0.1 --port 10000

.. warning::

   When using ``--connect-on-startup``, the server locks the connection and disables the
   ``launch_mechanical``, ``connect_to_mechanical``, and ``disconnect_from_mechanical`` tools
   for the duration of the session.

See the `PyMechanical-MCP documentation <https://mechanical-mcp.docs.pyansys.com/>`_ for full
setup, IDE configuration, and available tools.
