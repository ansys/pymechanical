.. _ref_kil_mechanical:

Mechanical standalone
=====================

In addition to Standalone Mechanical known issues and limitations given below,
please refer

- `Mechanical API known issues and limitations`_.
- `ACT known issues and limitations`_.

Known issues and limitations
----------------------------

- The ``Background`` property of ``AnimationExportSettings`` has no effect when using
  ``ExportAnimation()``. The background color cannot be changed programmatically for
  exported animations (`#1406 <https://github.com/ansys/pymechanical/issues/1406>`_).

24R2
^^^^

- In Read Only mode, the application does not display error messages when the geometry is imported in batch mode.
- Section planes can not be added through batch mode.
- Mechanical is not thread safe.
- Spaceclaim geometry (.scdocx) can not be imported on Linux platform.
- On Linux based platforms, Ansys Motion and LSDYNA analysis support are limited.
- A fatal error currently exists when you are shutting down Mechanical on the
  Linux platform using Embedding (`#85 <https://github.com/ansys/pymechanical/issues/85>`_).
- Geometry children are not populated when running the cooling holes thermal analysis example,
  causing an ``ArgumentOutOfRangeException``. This was fixed in 25R2 and later versions
  (`#1549 <https://github.com/ansys/pymechanical/issues/1549>`_).
