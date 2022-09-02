.. _ref_user_guide:

==========
User guide
==========
This guide provides a general overview of how you use PyMechanical library.


..
   This toctreemust be a top level index to get it to show up in
   pydata_sphinx_theme

.. toctree::
   :maxdepth: 1
   :hidden:

   launcher
   mechanical
   pool
   


PyMechanical overview
======================
The :func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>` function
within the ``ansys-mechanical-core`` library creates an instance of of
:class:`Mechanical <ansys.mechanical.core.mechanical.Mechanical>` in the background and sends
commands to that service. Errors and warnings are processed
Pythonically, letting you develop a script in real time without
worrying about if it functions correctly when deployed in batch
mode.

Mechanical can be started from Python in gRPC mode using the
:func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>`
method.

.. code:: python

    import os
    from ansys.mechanical.core import launch_mechanical

    mechanical = launch_mechanical()

Mechanical is now active. You can send commands to Mechanical as a genuine
Python class. For example, if can send a Python script:

.. code:: python

    result = mechanical.run_python_script('2+3')
    result = mechanical.run_python_script('ExtAPI.DataModel.Project.ProjectDirectory')

Mechanical interactively returns the result of each command and it is
stored to the logging module. Errors are caught immediately. For
example, if you input an invalid command:

.. code:: python

    >>> mechanical.run_python_script('2****3')

   grpc.RpcError:
   "unexpected token '**'"

This ``grpc.RpcError`` was caught immediately, and this means that
you can write your Mechanical scripts in Python, run them interactively, and
then as a batch, without worrying if the script runs correctly if
you had instead outputted it to a script file.

The :class:`Mechanical <ansys.mechanical.core.mechanical.Mechanical>` class supports much more
than just sending text to Mechanical and includes higher level wrapping
allowing for better scripting and interaction with Mechanical. See the
:ref:`ref_examples` for an overview of the various advanced
methods to interact with Mechanical.

