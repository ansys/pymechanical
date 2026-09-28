.. _ref_licensing:

License management
==================

Overview
--------

PyMechanical provides comprehensive license management capabilities through the ``LicenseManager`` class
for embedded Mechanical applications. This feature enables fine-grained control over Ansys Mechanical
licenses, including the ability to:

- Start applications without checking out a license (read-only mode)
- Choose specific licenses to check out
- Change the order of license preferences
- Enable or disable specific licenses
- Manage licenses dynamically during a session

.. note::
   License management features are available starting from **Ansys Mechanical 2025 R2 (version 252)** and later.

What's new
----------

Recent enhancements to PyMechanical include:

- **License Selection at Startup**: New ``start_license`` parameter in the ``App`` constructor allows you to
  specify which license to check out when starting the application.
- **Read-Only Mode**: New ``readonly`` parameter enables starting Mechanical without checking out a license.
- **License Manager API**: New ``LicenseManager`` class provides programmatic control over license preferences
  and session licenses.

These features provide greater flexibility for workflows that require specific licensing configurations or
need to minimize license usage.

License keywords and products
------------------------------

When using the ``start_license`` parameter, you can specify licenses using license keywords. The following
table shows the available license keywords and their corresponding Ansys products:

Solver licenses
~~~~~~~~~~~~~~~

These licenses provide full solve capabilities:

.. list-table:: Solver License Keywords
   :header-rows: 1
   :widths: 20 80

   * - Keyword
     - Product
   * - ``ansys``
     - Ansys Mechanical Enterprise
   * - ``mech_1``
     - Ansys Mechanical Pro
   * - ``mech_2``
     - Ansys Mechanical Premium
   * - ``meba``
     - Ansys Mechanical Enterprise Solver
   * - ``dyna``
     - Ansys LS-DYNA

PrepPost (non-solver) licenses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These licenses provide pre-processing and post-processing capabilities without solver access:

.. list-table:: PrepPost License Keywords
   :header-rows: 1
   :widths: 20 80

   * - Keyword
     - Product
   * - ``preppost``
     - Ansys Mechanical Enterprise PrepPost
   * - ``dynapp``
     - Ansys LS-DYNA PrepPost
   * - ``acdi_adprepost``
     - Ansys AUTODYN PrepPost

.. note::
   When specifying a license keyword with ``start_license``, use only the keyword (for example, ``start_license="meba"``).
   The license names returned by ``get_all_licenses()`` use the full product names (for example, "Ansys Mechanical Premium").

Starting the application
-------------------------

Without a license (read-only mode)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can start Mechanical in read-only mode without checking out a license. This is useful for viewing
results or exploring projects without consuming a license:

.. code-block:: python

    from ansys.mechanical.core import App

    # Start in read-only mode
    app = App(readonly=True, version=252)

    # Verify read-only status
    print(f"Read-only mode: {app.readonly}")  # Output: True

.. note::
   In read-only mode, you cannot modify the model or perform operations that require write access.

With a specific license
~~~~~~~~~~~~~~~~~~~~~~~~

You can specify which license to check out when starting the application using the ``start_license`` parameter:

.. code-block:: python

    from ansys.mechanical.core import App

    # Start with Mechanical Enterprise Solver license
    app = App(start_license="meba", version=252)

    # Start with Mechanical Premium license
    app = App(start_license="mech_2", version=252)

    # Start with Mechanical Pro license
    app = App(start_license="mech_1", version=252)

    # Start with Mechanical Enterprise license
    app = App(start_license="ansys", version=252)

.. tip::
   Refer to the :ref:`License Keywords and Products <ref_licensing>` section above for a complete list
   of available license keywords.

.. warning::
   The ``start_license`` parameter is ignored when ``readonly=True``.

With default license
~~~~~~~~~~~~~~~~~~~~

By default, when neither ``readonly`` nor ``start_license`` is specified, Mechanical checks out the
first enabled license in the preference order:

.. code-block:: python

    from ansys.mechanical.core import App

    # Start with default license behavior
    app = App(version=252)

    # Check which license was checked out
    print(app.license_manager.get_all_licenses())

License manager API
-------------------

The ``LicenseManager`` class provides comprehensive license management capabilities. Access it through
the ``license_manager`` property of the ``App`` instance:

.. code-block:: python

    from ansys.mechanical.core import App

    app = App(version=252)
    license_mgr = app.license_manager

Viewing available licenses
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get a list of all available licenses:

.. code-block:: python

    # Get all licenses in preference order
    licenses = license_mgr.get_all_licenses()
    print(licenses)
    # Output: ['Ansys Mechanical Enterprise', 'Ansys Mechanical Premium', 'Ansys Mechanical Pro']

Display license status information:

.. code-block:: python

    # Show all licenses with their status
    license_mgr.show()
    # Output:
    # Ansys Mechanical Enterprise - Enabled
    # Ansys Mechanical Premium - Enabled
    # Ansys Mechanical Pro - Disabled

Checking license status
~~~~~~~~~~~~~~~~~~~~~~~~

Check if a specific license is enabled or disabled:

.. code-block:: python

    # Get status of a specific license
    status = license_mgr.get_license_status("Ansys Mechanical Premium")
    print(status)  # Output: LicenseStatus.Enabled or LicenseStatus.Disabled

Enabling and disabling licenses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enable or disable specific licenses in your preference list:

.. code-block:: python

    # Disable a license so it won't be checked out
    license_mgr.set_license_status("Ansys Mechanical Pro", False)

    # Enable a license
    license_mgr.set_license_status("Ansys Mechanical Premium", True)

.. note::
   Changes made with ``set_license_status`` are persisted to user preferences and affect future sessions.

Changing license order
~~~~~~~~~~~~~~~~~~~~~~

Change the priority order of licenses. Mechanical attempts to check out licenses in order from
index 0 (highest priority):

.. code-block:: python

    # Move Ansys Mechanical Premium to first priority (index 0)
    license_mgr.move_to_index("Ansys Mechanical Premium", 0)

    # Verify the new order
    licenses = license_mgr.get_all_licenses()
    print(licenses)
    # Output: ['Ansys Mechanical Premium', 'Ansys Mechanical Enterprise', 'Ansys Mechanical Pro']

.. note::
   License order changes are saved to user preferences.

Resetting license preferences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Reset all license preferences (order and status) to default values:

.. code-block:: python

    # Reset to default license preferences
    license_mgr.reset_preference()

    # Verify preferences were reset
    licenses = license_mgr.get_all_licenses()
    print(licenses)

Session license management
--------------------------

Session licenses are temporary license checkouts that only affect the current Mechanical session.
Unlike preference changes, session license changes are not persisted.

Disabling session license
~~~~~~~~~~~~~~~~~~~~~~~~~~

Disable the currently checked-out license to put the application in read-only mode:

.. code-block:: python

    from ansys.mechanical.core import App

    app = App(version=252)

    # Initially not in read-only mode
    print(app.readonly)  # Output: False

    # Disable the session license
    app.license_manager.disable_session_license()

    # Now in read-only mode
    print(app.readonly)  # Output: True

Enabling session license
~~~~~~~~~~~~~~~~~~~~~~~~~

Enable a license for the current session. This is useful for temporarily checking out a license
when the application is in read-only mode:

.. code-block:: python

    # Enable default license (first enabled in preference order)
    app.license_manager.enable_session_license()

    print(app.readonly)  # Output: False

Enable a specific license:

.. code-block:: python

    # Enable a specific license
    app.license_manager.enable_session_license("Ansys Mechanical Premium")

    print(app.readonly)  # Output: False

Enable multiple licenses with priority order:

.. code-block:: python

    # Try to check out licenses in the specified order
    app.license_manager.enable_session_license([
        "Ansys Mechanical Enterprise",
        "Ansys Mechanical Premium"
    ])

    print(app.readonly)  # Output: False

Advanced workflows
------------------

Choosing a specific license (workaround)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to ensure a specific license is checked out when multiple licenses are available,
you can use the read-only workaround:

.. code-block:: python

    from ansys.mechanical.core import App

    # Method 1: Using start_license parameter (recommended)
    app = App(start_license="meba", version=252)  # Forces Mechanical Premium

    # Method 2: Using read-only workaround
    app = App(readonly=True, version=252)  # Start without license

    # Modify license order
    app.license_manager.move_to_index("Ansys Mechanical Premium", 0)

    # Enable the desired license
    app.license_manager.enable_session_license("Ansys Mechanical Premium")

    # Now using the specific license
    print(app.readonly)  # Output: False

Changing license mid-session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can change which license is checked out during a session:

.. code-block:: python

    from ansys.mechanical.core import App

    app = App(version=252)

    # Check current license status
    print("Currently using:")
    app.license_manager.show()

    # Switch to read-only (releases current license)
    app.license_manager.disable_session_license()
    print(f"\nRead-only mode: {app.readonly}")

    # Change license preference order
    app.license_manager.move_to_index("Ansys Mechanical Pro", 0)

    # Check out the new preferred license
    app.license_manager.enable_session_license()

    print("\nAfter license change:")
    app.license_manager.show()
    print(f"Read-only mode: {app.readonly}")

Minimizing license usage
~~~~~~~~~~~~~~~~~~~~~~~~~

For workflows that involve long periods of data processing or waiting, you can temporarily
release the license:

.. code-block:: python

    from ansys.mechanical.core import App
    import time

    app = App(version=252)

    # Perform operations requiring a license
    # ... your modeling operations ...

    # Release license during long computation
    app.license_manager.disable_session_license()

    # Perform operations that don't require write access
    # ... data processing, waiting for user input, etc. ...
    time.sleep(300)  # 5 minutes of processing

    # Re-acquire license for further modeling
    app.license_manager.enable_session_license()

    # Continue with modeling operations
    # ... more operations ...

Testing license availability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test if specific licenses are available before starting:

.. code-block:: python

    from ansys.mechanical.core import App

    app = App(readonly=True, version=252)  # Start without checking out a license

    # Check which licenses are available
    licenses = app.license_manager.get_all_licenses()
    print("Available licenses:", licenses)

    # Try to enable a preferred license
    preferred_licenses = [
        "Ansys Mechanical Enterprise",
        "Ansys Mechanical Premium",
        "Ansys Mechanical Pro"
    ]

    for lic in preferred_licenses:
        if lic in licenses:
            status = app.license_manager.get_license_status(lic)
            print(f"{lic}: {status}")

    # Enable with fallback priority
    app.license_manager.enable_session_license(preferred_licenses)
    print(f"Read-only mode: {app.readonly}")

Troubleshooting
---------------

License not available
~~~~~~~~~~~~~~~~~~~~~

If you try to enable a license that is not available:

.. code-block:: python

    app.license_manager.enable_session_license("Ansys Mechanical Premium")

    # If license is not available, app will remain in read-only mode
    if app.readonly:
        print("Warning: Requested license not available. Application is in read-only mode.")
        # Try alternative license
        app.license_manager.enable_session_license("Ansys Mechanical Pro")

Checking read-only status
~~~~~~~~~~~~~~~~~~~~~~~~~~

Always verify the read-only status before performing write operations:

.. code-block:: python

    if app.readonly:
        print("Application is in read-only mode. No write operations possible.")
    else:
        print("Application has an active license. Write operations allowed.")

Version compatibility
~~~~~~~~~~~~~~~~~~~~~

License management features require Mechanical 2025 R2 or later:

.. code-block:: python

    from ansys.mechanical.core import App

    app = App(version=242)  # Older version

    try:
        license_mgr = app.license_manager
    except Exception as e:
        print(e)
        # Output: "LicenseManager is only available for version 252 and later."

Best practices
--------------

1. **Use start_license for predictable startup**: When you know which license you need, use the
   ``start_license`` parameter instead of manipulating preferences.

2. **Release Licenses When Idle**: Use ``disable_session_license()`` during long idle periods to
   free up licenses for other users.

3. **Test License Availability**: In multi-user environments, start in read-only mode and check
   license availability before attempting to check out a license.

4. **Preserve User Preferences**: Be aware that ``set_license_status()`` and ``move_to_index()``
   modify user preferences permanently. Use ``reset_preference()`` to restore defaults if needed.

5. **Handle license failures gracefully**: Always check ``app.readonly`` status before attempting
   write operations to handle license unavailability.

Example: Complete license management workflow
----------------------------------------------

Here's a complete example demonstrating various license management scenarios:

.. code-block:: python

    from ansys.mechanical.core import App

    # Start in read-only mode to inspect license options
    app = App(readonly=True, version=252)

    print("=== Available Licenses ===")
    app.license_manager.show()

    print("\n=== Configure License Preferences ===")
    # Set preferred license order
    app.license_manager.move_to_index("Ansys Mechanical Premium", 0)
    app.license_manager.move_to_index("Ansys Mechanical Enterprise", 1)

    # Disable a license we don't want to use
    app.license_manager.set_license_status("Ansys Mechanical Pro", False)

    print("\nUpdated license order:")
    licenses = app.license_manager.get_all_licenses()
    for idx, lic in enumerate(licenses):
        status = app.license_manager.get_license_status(lic)
        print(f"  {idx}: {lic} - {status}")

    print("\n=== Check Out License ===")
    # Enable the preferred license
    app.license_manager.enable_session_license()

    if not app.readonly:
        print("License checked out successfully")
        # Perform modeling operations
        print("Performing modeling operations...")
        # ... your code here ...
    else:
        print("Failed to check out license")

    print("\n=== Release License Temporarily ===")
    app.license_manager.disable_session_license()
    print(f"Read-only mode: {app.readonly}")

    # Perform operations that don't need a license
    print("Performing read-only operations...")

    print("\n=== Re-acquire License ===")
    app.license_manager.enable_session_license()
    print(f"Read-only mode: {app.readonly}")

    print("\n=== Reset to Defaults ===")
    app.license_manager.reset_preference()
    print("License preferences reset to default")


Additional resources
--------------------

- :ref:`FAQ: How do you check if a license is active with PyMechanical? <faq>`
- `Ansys Licensing Guide <https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/prod_page.html?pn=Licensing&pid=Licensing&lang=en>`_