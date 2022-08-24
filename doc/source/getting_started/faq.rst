.. _faq:

**************************
Frequently Asked Questions
**************************

A collection of frequently asked questions and their answers.

How should I report issues?
---------------------------

Issues with pyansys such as bugs, feature requests, and documentation
errors can be reported on the `GitHub page
<https://github.com/pyansys/PyMechanical/issues>`_ as new issues.

If you wish to ask more open-ended questions or wish to pick the
brains of the community you can visit the `Discussions section
<https://github.com/pyansys/PyMechanical/discussions>`_ of our GitHub
repository.


What are the pros and cons of pyansys vs Ansys ACT?
---------------------------------------------------

It depends on your pipeline and software approach. Ansys Act is a
workbench dependent approach where extensions are built from within
the ACT App Builder and then run from within Ansys Mechanical.  If you
intend to vary parameters, you'll then need to use Ansys optiSLang to
vary those parameters and batch your solutions.

The main advantages that PyAnsys has over Ansys ACT are:

* Tight integration with python tools and open source modules
  alongside Ansys software.
* Scripts are written in python. ACT uses .net and you can call
  IronPython, and potentially other tools available within Ansys
  Mechanical.
* Being outside of Ansys Mechanical means that you can call our
  application workflow without opening up the GUI for user
  interaction.
* It is compatible with modern Python (3), whereas ACT is only
  compatible with IronPython (Python 2)

The best approach will depend on your workflow needs and how you'd
like to develop software.


What are the main reasons to use this over other Ansys products like Workbench?
-------------------------------------------------------------------------------
There will always be tasks where it's better to use one or the
other. Workbench is great tool to rapidly prototype, mesh, set
boundary conditions, and solve. It's where a ton of development has
gone there are many features that make it easy to run
analyses. However, it's limited by its IronPython scripting and you're
unable call multiple products at either a granular or high level or
use packages such as ``numpy``, ``scipy``, ``pytorch``,
``tensorflow``, etc.  PyMechanical ties this in with Mechanical, that allows you
to have a fully parametric workflow that leverages these machine
learning tools.



Script Restart
--------------
**Question**

Sometimes I have difficulty to terminate the simulation. I
have to close python and open it again.  I also need to clear all
previous data such as the mesh.  Is there a better way?

I am using:

.. code:: python

    import sys
    sys.modules[__name__].__dict__.clear()

Is there a better way?

**Solution**

Exiting Python should clear the solution within Python should do it
since if you kill the original process nothing should be in the new
python process. As for clearing out Mechanical, it's just
``mechanical.clear()`` or exiting and restarting Mechanical.
