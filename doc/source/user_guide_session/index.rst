.. _ref_user_guide_session:

Remote sessions
===============

This section  provides an overview of how you use PyMechanical as a client
to a remote Mechanical session.

..
   This toctreemust be a top level index to get it to show up in
   pydata_sphinx_theme

.. toctree::
   :maxdepth: 1
   :hidden:

   server-launcher
   mechanical
   pool

Overview
--------

The `launch_mechanical() <../api/ansys/mechanical/core/mechanical/index.html#mechanical.launch_mechanical>`_ method
creates an instance of the `Mechanical <../api/ansys/mechanical/core/mechanical/Mechanical.html>`_
class in the background and sends commands to it as a service. Because errors and warnings
are processed Pythonically, you can develop a script in real time without worrying about
whether the script runs correctly when deployed in batch mode.

Here is how you use the `launch_mechanical()`_ method to launch Mechanical from Python in gRPC mode:

.. code:: python

    import os
    from ansys.mechanical.core import launch_mechanical

    mechanical = launch_mechanical()

When Mechanical is active, you can send commands to it as a genuine
Python class. For example, you can send a Python script:

.. code:: python

    result = mechanical.run_python_script("2+3")
    result = mechanical.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")

Mechanical interactively returns the result of each command that you send,
saving the result to the logging module.

Errors are caught immediately. In the following code, an invalid command is sent,
and an error is raised:

.. code:: pycon

    >>> mechanical.run_python_script("2****3")
    grpc.RpcError:
    "unexpected token '**'"

Because the error is caught immediately, you can write your Mechanical scripts in
Python, run them interactively, and then run them in batch without worrying if the
scripts run correctly. This would not be the case if you had instead outputted the
scripts that you wrote to script files.

The `Mechanical`_ class supports
much more than sending text to Mechanical. It includes higher-level wrapping
that provides for better scripting and interaction with Mechanical. For information
on advanced methods for interacting with Mechanical, see :ref:`ref_examples`.

