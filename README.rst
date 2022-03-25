PyMechanical
=======

Overview
--------
The PyMechanical project supports Pythonic access to Mechanical to be able to
communicate with the Mechanical process directly from Python. The latest
ansys-mechanical-core package enables a more comprehensive interface with
Mechanical and supports:

- Remote connections to Mechanical from anywhere via gRPC.

PyMechanical works within Jupyter Notebooks, the standard Python console,
or in batch mode on Windows, Linux, and even Mac OS.

Installation
------------
The ``ansys-mechanical-core`` package currently supports Python 3.7.11 through
Python 3.9 on Windows, Mac OS, and Linux.

For a local "development" version, install with:

.. code::

   git clone https://tfs.ansys.com:8443/tfs/ANSYS_Development/Mechanical/_git/pymechanical
   cd pymechanical
   pip install -e .


Dependencies
------------
You will need a local licenced copy of Mechanical to run Mechanical 2022R2.


Getting Started
---------------

Launch Mechanical Locally
~~~~~~~~~~~~~~~~~~~~
You can launch Mechanical locally directly from Python using:

TODO:


Launching Manually or Connecting to a Remote Instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you wish to connect to a session of Mechanical on a remote computer
(either locally the LAN or through the internet), first ensure you
have Mechanical started in gRPC server mode.  This example assumes you will
be launching an instance locally from Windows, but can be easily
adapted to run from Linux, or the LAN provided the necessary ports are
open.  This example specifies the port with ``-grpc 10000``, but this
option can be left out if you plan on using the default port 10000.

TODO:


Should you wish to connect to this instance of Mechanical from a remote
computer, you substitute ``ip=`` with the LAN or WAN address of the
computer you wish to connect to.  Depending on your network settings,
you may have to open local ports or enable port redirection across the
WAN.


Basic Usage
~~~~~~~~~~~
You run Mechanical commands via:

TODO:


Run on Docker
~~~~~~~~~~~~~
Run Mechanical within a container on any OS with ``docker``!


License and Acknowledgments
---------------------------
``PyMechanical`` is licensed under the MIT license.

This module, ``ansys-mechanical-core`` makes no commercial claim over Ansys
whatsoever.  This tool extends the functionality of ``Mechanical`` by
adding a Python interface to the Mechanical service without changing the
core behavior or license of the original software.  The use of the
interactive Mechanical control of ``PyMechanical`` requires a legally licensed
local copy of Ansys.

To get a copy of Ansys, please visit `Ansys <https://www.ansys.com/>`_.
