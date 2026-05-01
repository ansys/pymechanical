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
- In the Mechanical scripting window, ``Model.DeleteParts()`` does not work when the
  CPython engine is used, while the same workflow works with IPython. This can be
  reproduced by building a list of ``GeoPart`` objects (for example with
  ``ExtAPI.DataModel.GeoData.GeoPartById()``) and passing it to ``Model.DeleteParts()``
  (`#1047 <https://github.com/ansys/pymechanical/issues/1047>`_).
24R2
^^^^

- In Read Only mode, the application does not display error messages when the geometry is imported in batch mode.
- Section planes cannot be added through batch mode.
- Mechanical is not thread safe.
- SpaceClaim geometry (.scdocx) cannot be imported on Linux platforms.
- On Linux based platforms, Ansys Motion and LSDYNA analysis support are limited.
- A fatal error currently exists when you are shutting down Mechanical on the
  Linux platform using Embedding (`#85 <https://github.com/ansys/pymechanical/issues/85>`_).
- Geometry children are not populated when running the cooling holes thermal analysis example,
  causing an ``ArgumentOutOfRangeException``. This was fixed in 25R2 and later versions
  (`#1549 <https://github.com/ansys/pymechanical/issues/1549>`_).

26R1
^^^^

- When calling ``ExportToXMLFile()`` on Harmonic Acoustics results (such as
  ``AcousticSPLFrequencyResponse``), Ansys Sound is opened each time the method is
  invoked. If Ansys Sound is not installed, an error dialog appears requiring manual
  dismissal. This prevents full automation of batch workflows
  (`#1400 <https://github.com/ansys/pymechanical/issues/1400>`_).
- In embedded mode, ``Graphics.LabelManager.CreateProbeLabel()`` causes a fatal crash
  (``AnsysWBU.exe`` encountered a problem). A fix is planned for a future release
  (`#1531 <https://github.com/ansys/pymechanical/issues/1531>`_).
- Using ``Graphics.Scene.Factory2D.CreateText()`` in embedded mode terminates the
  process with a ``StackOverflowException``. This issue was observed with Mechanical
  26R1 and a fix is planned for a future release.
  (`#1521 <https://github.com/ansys/pymechanical/issues/1521>`_).
- Creating a label on a figure with ``Graphics.LabelManager.CreateLabel()`` in
  embedded mode causes a fatal crash (``AnsysWBU.exe`` encountered a problem). This
  issue was observed with Mechanical 26R1 and a fix is planned for a future release
  (`#1520 <https://github.com/ansys/pymechanical/issues/1520>`_).
- Creating a section plane with ``Graphics.SectionPlanes.CreateSectionPlane()`` and a
  coordinate system in embedded mode does not behave reliably, even though the same
  script works in the Mechanical scripting window. This issue was observed with
  Mechanical 26R1 and a fix is planned for a future release
  (`#1497 <https://github.com/ansys/pymechanical/issues/1497>`_).
