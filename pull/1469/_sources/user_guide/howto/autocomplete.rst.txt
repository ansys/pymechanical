.. _ref_autocomplete:

Autocomplete
============

The ``ansys-mechanical-stubs`` package provides typehints for Mechanical scripting.
This package is automatically installed when you install PyMechanical.

Setting up autocomplete in VS Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``ansys-mechanical-ideconfig`` command prints the settings that are necessary for
autocomplete to work with the ``ansys-mechanical-stubs`` dependency. This command takes in
three arguments: ``--ide vscode``, ``--target user`` or ``--target workspace``,
and ``--revision <version>``. If the revision is not provided, ``ansys-tools-common``
retrieves the Mechanical version from your system.

Usage:

.. code:: shell

    ansys-mechanical-ideconfig --ide vscode --target user --revision 252

Terminal output for Windows user's settings.json file:

.. code:: shell

    Update C:\Users\{username}\AppData\Roaming\Code\User\settings.json with the following information:

    {
        "python.autoComplete.extraPaths": [
            "{project_directory}\\.venv\\Lib\\site-packages\\ansys\\mechanical\\stubs\\v252"
        ],
        "python.analysis.extraPaths": [
            "{project_directory}\\.venv\\Lib\\site-packages\\ansys\\mechanical\\stubs\\v252"
        ]
    }

Paste the output from the command into your VS Code ``settings.json`` file to activate autocomplete.

Limitations
^^^^^^^^^^^

- Autocomplete is only supported in VS Code.
- Mechanical scripting autocomplete is only available for phrases starting with ``Ansys``.
- Not all Mechanical scripting APIs are currently supported. If some are missing that you need,
  create an issue `here <https://github.com/ansys/pymechanical-stubs/issues>`_.
