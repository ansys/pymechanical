.. _ref_user_guide:

==========
User Guide
==========
This guide provides a general overview of the basics and usage of the
PyMechanical library.


..
   This toctreemust be a top level index to get it to show up in
   pydata_sphinx_theme

.. toctree::
   :maxdepth: 1
   :hidden:

   launcher
   mechanical
   pool
   


PyMechanical Basic Overview
===========================
The :func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>` function
within the ``ansys-mechanical-core`` library creates an instance of of
:class:`Mechanical <ansys.mechanical.core.mechanical.Mechanical>` in the background and sends
commands to that service.  Errors and warnings are processed
Pythonically letting the user develop a script real-time without
worrying about if it will function correctly when deployed in batch
mode.

Mechanical can be started from python in gRPC mode using
:func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>`.

.. code:: python

    import os
    from ansys.mechanical.core import launch_mechanical

    mechanical = launch_mechanical()

Mechanical is now active and you can send commands to it as a genuine a
Python class.  For example, if we wanted to send a python script

.. code:: python

    result = mechanical.run_python_script('2+3')
    result = mechanical.run_python_script('ExtAPI.DataModel.Project.ProjectDirectory')

Mechanical interactively returns the result of each command and it is
stored to the logging module.  Errors are caught immediately.  For
example, if you input an invalid command:

.. code:: python

    >>> mechanical.run_python_script('2****3')

   grpc.RpcError:
   "unexpected token '**'"

This grpc.RpcError was caught immediately, and this means that
you can write your Mechanical scripts in python, run them interactively and
then as a batch without worrying if the script will run correctly if
you had instead outputted it to a script file.

The :class:`Mechanical <ansys.mechanical.core.mechanical.Mechanical>` class supports much more
than just sending text to Mechanical and includes higher level wrapping
allowing for better scripting and interaction with Mechanical.  See the
:ref:`ref_examples` for an overview of the various advanced
methods to interact with Mechanical.

