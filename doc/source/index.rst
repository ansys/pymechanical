PyMechanical Documentation |version|
====================================

.. toctree::
   :hidden:
   :maxdepth: 3


   getting_started/index
   user_guide/index
   api/index
   examples/index
   contributing



Introduction and Purpose
------------------------
PyMechanical is part of the larger `PyAnsys <https://docs.pyansys.com>`_
effort to facilitate the use of Ansys technologies directly from
Python. Its primary package, ``ansys-mechanical-core``, provides:

- Scripting of Mechanical through Python

With PyMechanical it is easier than ever to integrate the simulation capabilities
of the Ansys Mechanical multi-physics solver directly into novel applications.
The package presents a Python-friendly interface to drive the software
that manages the submission of low-level Mechanical Scripting commands, while exchanging
data through high-performance gRPC interfaces.

Accelerate the preparation of your simulations using PyMechanical. Combine the
expressiveness of general-purpose Python code to control the flow in your
input decks with methods that drive the solver. Explore proof of concept
studies or capture knowledge using interactive Jupyter notebooks.  Tap
the solver as the physics engine in your next Artificial Intelligence
application. It is now open source: Enjoy it! Contributions are welcome.


Background
----------
PyMechanical, based on `gRPC <https://grpc.io/>`_. These technologies
allow the Mechanical application to function as a server, ready to respond to
connecting clients.

Google remote procedure calls, or gRPC, are used to establish secure
connections so that a client application can directly call methods on
a potentially remote Mechanical instance as if it were a local object. The
use of HTTP/2 makes it friendly to modern internet infrastructures.
This, along with the use of binary transmission formats, favors higher
performance. Using gRPC, PyMechanical can  send Mechanical scripting API commands
transmitted to an Mechanical instance running anywhere,
while producing network footprints that are compact and efficient.


Quick Code
----------
Here's a brief example of how PyMechanical works:

.. code:: python

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mechanical = launch_mechanical()
    >>> print(mechanical)

    Ansys Mechanical [Ansys Mechanical Enterprise]
    Product Version:231
    Software build date:Wednesday, August 10, 2022 4:28:15 PM

Mechanical is now active and you can send commands to it as a genuine a
Python class.  For example, if we wanted send some scripts:

.. code:: python

    result = mechanical.run_python_script('2+3')
    result = mechanical.run_python_script('10*5')

Mechanical interactively returns the result of each command and it is
stored to the logging module or can be immediately printed out with
``print(mechanical.run_python_script('2+3')``.  Errors are caught immediately and pythonically.

For a full listing of the additional PyMechanical features, please see the
:ref:`ref_user_guide`.


Project Index
*************

* :ref:`genindex`
