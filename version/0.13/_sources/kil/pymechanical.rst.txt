.. _ref_kil_pymechanical:

PyMechanical
============

Known issues and limitations
----------------------------

It is suggested to use latest stable version of PyMechanical.
Any issues and limitations for previous versions are not currently documented.
If you find any other, create an issue `here <PyMechanical issue_>`_

Limitations in v0.13
^^^^^^^^^^^^^^^^^^^^

- When you initialize the ``App`` class with ``interactive=True`` in embedded mode on Windows,
  the Mechanical 26 R1 GUI remains on the loading screen
  (`#1484 <https://github.com/ansys/pymechanical/issues/1484>`_).

Limitations in v0.11
^^^^^^^^^^^^^^^^^^^^

- ``App.plot()`` visualization feature is available only for geometry. You cannot plot mesh or results
  but you can export these data as images or an animation.
