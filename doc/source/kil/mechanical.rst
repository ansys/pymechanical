.. _ref_kil_mechanical:

Mechanical standalone
=====================

In addition to Standalone Mechanical known issues and limitations given below,
please refer

- `Mechanical API known issues and limitations`_.
- `ACT known issues and limitations`_.

Known issues and limitations
----------------------------

24R2
^^^^

- In Readonly mode, Mechanical does not throw any exception when geometry is imported in batch mode.
- Section planes can not be added through batch mode.


24R1
^^^^

- `Python libraries <https://mechanical.docs.pyansys.com/version/stable/user_guide_embedding/libraries.html>`_
  that are distributed with the installation of Mechanical does not work when there are syntax differences
  between IronPython and CPython (`#515 <https://github.com/ansys/pymechanical/issues/515>`_).
- Trace Import fails with PyMechanical Embedding with only ``python 3.10``.

23R2
^^^^

-
-


