PyMechanical documentation |version|
====================================

.. toctree::
   :hidden:
   :maxdepth: 3


   getting_started/index
   user_guide_scripting/index
   user_guide_session/index
   user_guide_embedding/index
   api/index
   examples/index
   contributing



Introduction
------------
PyMechanical is part of the larger `PyAnsys <https://docs.pyansys.com>`_
effort to facilitate the use of Ansys technologies directly from
Python. Its primary package, ``ansys-mechanical-core``, provides
scripting of Ansys Mechanical through Python.

With PyMechanical, you can integrate the simulation capabilities
of the Mechanical multiphysics solver directly into novel apps.
The package presents a Python-friendly interface to drive the software
that facilitates use of Mechanical scripting commands.

Accelerate the preparation of your simulations using PyMechanical. Combine the
expressiveness of general-purpose Python code to control the flow in your
input decks with methods that drive the solver. Explore proof of concept
studies or capture knowledge using interactive Jupyter notebooks. Tap
the solver as the physics engine in your next Artificial Intelligence
application. Contributions to this open source library are welcome.


Mechanical scripting
--------------------
You could already perform scripting of Mechanical with Python from inside
Mechanical. PyMechanical leverages the same APIs but allow you to run your
automation from outside Mechanical. More information about using these APIs
is available in :ref:`ref_user_guide_scripting`.

Background
----------
PyMechanical contains two interfaces, a remote session and an embedded instance.

Remote session
^^^^^^^^^^^^^^
PyMechanical's  remote session is based on `gRPC <https://grpc.io/>`_.
Mechanical runs as a server, ready to respond to any clients.

PyMechanical provides a client to connect to a Mechanical server and make API
calls to that server.

For comprehensive information on this feature, see the
:ref:`ref_user_guide_session`.

Embedded instance
^^^^^^^^^^^^^^^^^
PyMechanical's embedded instance is based on `pythonnet <http://pythonnet.github.io/>_`.
Rather than starting a new process for Mechanical, a Mechanical object (which is
implemented in .NET) is directly loaded into Python memory using ``pythonnet``. From
there, Mechanical's entire data model is available for use from Python code.

For comprehensive information on this feature, see
:ref:`ref_user_guide_embedding`.


Project index
*************

* :ref:`genindex`
