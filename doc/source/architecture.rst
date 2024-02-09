.. _ref_architecture:

=========================
PyMechanical Architecture
=========================

PyMechanical is a Python interface to the Mechanical application.
Mechanical is a polyglot [#f1]_ desktop application whose graphical
user interface (GUI) can run on both windows and linux.

For several years now, Mechanical has had Python scripting capabilities
using a scripting API. Like many other applications developed by Ansys,
scripting became heavily used for the purpose of *automation*. A user who
would spend time doing the same thing over and over again with the GUI
could instead write a script to do the same thing, saving time and effort.

Also like many other applications, Mechanical's API served another purpose.
That is, it was used for *customization*. Users could use the API as a way
to add capabilities to Mechanical. It has been used to add buttons to the
User Interface, add custom objects to the data model, even as far as adding
third party solvers that can take advantage of the powerful and intuitive
pre and post processing of Mechanical.

Because the API serves the needs of both *automation* and *customization*,
it did not use a version of the *command pattern*. More on this later.
Instead, the API provides the object model directly as the API.

Mechanical API Architecture
---------------------------

=============================
Remote interfaces in the wild
=============================




.. rubric:: Footnotes

.. [#f1] This means that it is implemented using more than one programming language.
.. [#f2] Text of the second footnote.