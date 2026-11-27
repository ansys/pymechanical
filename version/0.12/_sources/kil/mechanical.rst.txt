.. _ref_kil_mechanical:

Mechanical standalone
=====================

In addition to Standalone Mechanical known issues and limitations given below,
refer to:

- `Mechanical API known issues and limitations`_.
- `ACT known issues and limitations`_.

Known issues and limitations
----------------------------

.. vale Google.Headings = NO

24R2
^^^^

.. vale Google.Headings = YES

- In Read Only mode, the application does not display error messages when the geometry is imported in batch mode.
- Section planes can not be added through batch mode.
- Mechanical is not thread safe.
- Spaceclaim geometry (.scdocx) can not be imported on Linux platform.
- On Linux based platforms, Ansys Motion and LSDYNA analysis support are limited.
- A fatal error currently exists when you are shutting down Mechanical on the
  Linux platform using Embedding (`#85 <https://github.com/ansys/pymechanical/issues/85>`_).
