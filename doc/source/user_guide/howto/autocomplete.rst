.. _ref_autocomplete:

Autocomplete
============

*Available in version 0.11.8 or later.*

The ``ansys-mechanical-ideconfig`` command prints the settings that are necessary for
autocomplete to work with the ``ansys-mechanical-stubs`` dependency. This command takes in
three arguments: ``--ide vscode``, ``--target user`` or ``--target workspace``,
and ``--revision <version>``. If the revision is not provided, ``ansys-tools-path``
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