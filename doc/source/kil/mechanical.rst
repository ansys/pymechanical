.. _ref_kil_mechanical:

Mechanical standalone
=====================

In addition to Standalone Mechanical known issues and limitations given below,
refer to:

- `Mechanical API known issues and limitations`_.
- `ACT known issues and limitations`_.

Known issues and limitations
----------------------------

- The ``Background`` property of ``AnimationExportSettings`` has no effect when using
  ``ExportAnimation()``. The background color cannot be changed programmatically for
  exported animations (`#1406 <https://github.com/ansys/pymechanical/issues/1406>`_).
- In embedded mode, ``Model.DeleteParts()`` fails when passed a list of ``GeoPart``
  objects (for example, built using ``ExtAPI.DataModel.GeoData.GeoPartById()``). The
  same workflow succeeds in the Mechanical scripting window and in batch mode
  (`#1047 <https://github.com/ansys/pymechanical/issues/1047>`_).


24R2
^^^^


- In Read Only mode, the app does not display error messages when the geometry is imported in batch mode.
- Section planes can not be added through batch mode.
- Mechanical is not thread safe.
- SpaceClaim geometry (.scdocx) cannot be imported on Linux platforms.
- On Linux based platforms, Ansys Motion and LSDYNA analysis support are limited.https://github.com/ansys/pymechanical/pull/1591/conflicts
- A fatal error currently exists when you are shutting down Mechanical on the
  Linux platform using Embedding (`#85 <https://github.com/ansys/pymechanical/issues/85>`_).
- Geometry children are not populated when running the cooling holes thermal analysis example,
  causing an ``ArgumentOutOfRangeException``. This was fixed in 25R2 and later versions
  (`#1549 <https://github.com/ansys/pymechanical/issues/1549>`_).


26R1
^^^^

- When ``ExportToXMLFile()`` is called on Harmonic Acoustics results (such as
  ``AcousticSPLFrequencyResponse``), Ansys Sound opens on every invocation. If Ansys
  Sound is not installed, an error dialog requires manual dismissal, preventing full
  automation of batch workflows
  (`#1400 <https://github.com/ansys/pymechanical/issues/1400>`_).
- Calling ``Graphics.LabelManager.CreateProbeLabel()`` in embedded mode causes a fatal
  crash (``AnsysWBU.exe`` encountered a problem). A fix is planned for a future release
  (`#1531 <https://github.com/ansys/pymechanical/issues/1531>`_).
- ``Graphics.Scene.Factory2D.CreateText()`` terminates the process with a
  ``StackOverflowException`` when called in embedded mode. This is a known Ansys
  Mechanical defect and will be addressed in a future release
  (`#1521 <https://github.com/ansys/pymechanical/issues/1521>`_).
- A fatal crash (``AnsysWBU.exe`` encountered a problem) occurs when
  ``Graphics.LabelManager.CreateLabel()`` is called on a figure in embedded mode.
  A fix is planned for an upcoming release
  (`#1520 <https://github.com/ansys/pymechanical/issues/1520>`_).
- ``Graphics.SectionPlanes.CreateSectionPlane()`` with a coordinate system does not
  behave reliably in embedded mode, even though the same script succeeds in the
  Mechanical scripting window. This will be addressed in a future release
  (`#1497 <https://github.com/ansys/pymechanical/issues/1497>`_).
