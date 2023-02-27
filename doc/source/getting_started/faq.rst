.. _faq:

**************************
Frequently asked questions
**************************

How do you report issues?
-------------------------

You can report issues with PyMechanical, such as bugs, feature requests,
and documentation errors, on the repository's `Issues
<https://github.com/pyansys/PyMechanical/issues>`_ page.

If you want to ask more open-ended questions or are seeking advice
from experts in the community, post on the `Discussions
<https://github.com/pyansys/PyMechanical/discussions>`_ page.


How is PyMechanical positioned with respect to other related tools?
-------------------------------------------------------------------

Users who want automation and extension of the Mechanical application should
consider the following tools:

* ACT in Mechanical
* Scripting in Mechanical
* PyMechanical

All of these tools work best in interactive mode, but there is increasing support
for batch mode. The first two can be used from the Workbench platform or from the
standalone Mechanical application.

ACT in Mechanical
^^^^^^^^^^^^^^^^^

In the Ansys Mechanical product, ACT is a customization framework. When specific
features are missing, users can add them using ACT. Of course, some of those
missing features might be automations/scripts of existing features. But in many
cases, these can be new capabilities, such as extensions to the data model of
Mechanical, the ability to connect to callbacks, and even integration of external
solvers.

Scripting in Mechanical
^^^^^^^^^^^^^^^^^^^^^^^

The python scripting capability within Mechanical was born out of the same development
that brought ACT to Mechanical. These APIs are the same as those used for PyMechanical,
but can only be run from inside the product. By default, these use IronPython 2.7,
but CPython 3.x based scripting is available with a feature flag in recent versions of
Mechanical. Mechanical offers an intuitive user interface for scripting, called the 
"Mechanical Scripting View" with features like script recording, autocomplete, and  a
snippet library. However - it is possible to use this feature in batch mode without the
User Interface.

PyMechanical
^^^^^^^^^^^^

PyMechanical allows you to write python scripts outside of mechanical, with tight
integration with other open source modules and Ansys products on your terms. This
means that you can freely import any module and tool that is supported in your
python environment. There is no dependency on opening the Mechanical User Interface.


What is the relationship with Ansys Workbench?
----------------------------------------------

Ansys Workbench is a no-code environment to set up Analysis systems that can be linked
together. It is part of the Ansys family of Process Automation and Design Exploration
software that now also includes Ansys OptiSLang. The most popular applications within
this environment is Ansys Mechanical, and for many years, Ansys Workbench was the only
environment from which to run Ansys Mechanical.

Because it is a no-code environment, a lot of the complexity around managing the data
transfer between applications and running parametric studies has been hidden from the user.

Using PyMechanical, and PyAnsys more broadly, for process automation and design Exploration
gives you much more control over how it works, but by avoiding workbench you also miss
out on what it handles under-the-hood.

How do you restart a script?
----------------------------
If you have trouble terminating a simulation, you do not have use the
following code to close Python, reopen it, and clear all previous data
such as the mesh.

.. code:: python

    import sys
    sys.modules[__name__].__dict__.clear()


Exiting Python should clear the solution within Python. This is because 
stopping the original process means that nothing should be in
a new process.

To clear all data from Mechanical in PyMechanical, if it is an embedded instance use the
:func:`app.new() <ansys.mechanical.core.embedding.Application.new>` method

or if it is a remote session either use the

:func:`Mechanical.clear() <ansys.mechanical.core.Mechanical.clear>` method or exit and restart Mechanical.
