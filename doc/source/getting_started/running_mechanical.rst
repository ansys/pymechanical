.. _using_standard_install:

*************************************************
Using PyMechanical from the standard installation
*************************************************

The ``ansys-mechanical-core`` package requires either a local or
remote instance of Mechanical to communicate with it. This page covers
launching and interfacing with Mechanical from a local instance by
launching it from Python.

Install Mechanical
------------------

Mechanical is installed by default from the Ansys standard installer. 
When you run the standard installer, verify that the **Mechanical Products**
checkbox is selected under the **Structural Mechanics** heading. Although
options in the standard installer might change, this image provides a reference.

.. figure:: ../images/unified_install_2023R1.jpg
    :width: 400pt


Launch Mechanical
-----------------
You can lauch Mechanical in many different ways.

Launch Mechanical locally
~~~~~~~~~~~~~~~~~~~~~~~~~

Using the ``launch_mechanical()`` method is the easiest and fastest way
to launch PyMechanical and automatically connect to it. However, this
method requires that you have an Ansys license server installed locally. If
this requirement is met, you can launch PyMechanical with:

.. code:: python

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mechanical = launch_mechanical()
    >>> print(mechanical)

    Ansys Mechanical [Ansys Mechanical Enterprise]
    Product Version:231
    Software build date:Wednesday, August 10, 2022 4:28:15 PM


Launch a gRPC Mechanical session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can launch Mechanical in gRPC mode from the command line and then connect to it.

**On Windows**

Assume that Mechanical is installed at ``C:/Program Files/ANSYS Inc/vXXX``
, where ``XXX`` is the three-digit format for the release. For example, the
path for 2023 R1 is ``C:/Program Files/ANSYS Inc/v231``. You would launch
Mechanical with:

.. code::

    C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/.AnsysWBU.exe -DSApplet -AppModeMech -nosplash -notabctrl -grpc 10000

**On Linux**

Assume that Mechanical is installed at ``/usr/ansys_inc``. You would launch
Mechanical 2023 R1 with:

.. code::

    /usr/ansys_inc/v231/aisol/.workbench -dsapplet -AppModeMech -nosplash -notabctrl -grpc 10000

As Mechanical starts and after it has started, you can see status information:

.. code::

    Starting the grpc server at port 10000
    Started the grpc server at port 10000

If you want to configure the port that Mechanical is to start on, you use the ``-grpc`` argument.
For example, you would start Mechanical 2023 R1 on Linux to listen for connections on port 10001 with:

.. code::

    /usr/ansys_inc/v211/ansys/bin/ansys211 -grpc 10001


Connect to a gRPC Mechanical session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can connect to a Mechanical gRPC server either from the same host or from an
external host. For example, you can connect to a Mechanical service running *locally* with:

.. code::

    >>> from ansys.mechanical.core import Mechanical
    >>> mechanical = Mechanical()


This assumes that your Mechanical service is running locally at the default IP address 
(127.0.0.1) and on the default port (10000).

If you want to connect to a *remote* instance of Mechanical, you must know the IP 
address of this instance. For example, assume that a computer on your local network
is running Mechanical at IP address ``192.168.0.1`` on port 50052. You can connect
to this instance with:

.. code::

    >>> mechanical = Mechanical('192.168.0.1', port=10000)

Alternatively, you can connect to the remote Mechanical instance using a hostname:

.. code:: python

    >>> mechanical = Mechanical('myremotemachine', port=10000)


To be able to connect to a remote instance of Mechanical, Mechanical must have
been started in gRPC mode at the specified IP address or hostname.

As indicated in the previous section, if you have Mechanical installed locally,
you can use the ``launch_mechanical`` function to both start and connect to Mechanical.

Launching issues
----------------

For any number of reasons, Python might fail to launch Mechanical. Some approaches
follow for debugging a launch failure.

Provde the location of the executable file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have a non-standard install, PyMechanical might not be able to find
your Mechanical installation. If this is the case, provide the location of Mechanical
as the first parameter to the ``launch_mechanical()`` method.

**On Windows**

.. code:: python

    >>> from ansys.mechanical.core import launch_mechanical
    >>> exec_loc = 'C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/AnsysWBU.exe'
    >>> mechanical = launch_mechanical(exec_loc)


**On Linux**

.. code:: python

    >>> from ansys.mechanical.core import launch_mechanical
    >>> exec_loc = '/usr/ansys_inc/v231/aisol/.workbench'
    >>> mechanical = launch_mechanical(exec_loc)


If Mechanical fails to launch or hangs while launching when
you use the ``launch_mechanical()`` method, pass the ``verbose_mechanical=True``
parameter. This prints the output of Mechanical within Python. You 
can then use this output to debug why Mechanical isn't launching.

.. Note::
    On Windows, output is limited because of the way Mechanical launches.

Debug from the command line
~~~~~~~~~~~~~~~~~~~~~~~~~~~
In some cases, debugging why Mechanical isn't launching might require
running the launch command manually from the command line. The following
Windows and Linux code examples assume that you are launching Mechanical
2023 R1.

**On Windows**

Open up a command prompt and run this command:

.. code::

    "C:/Program Files/ANSYS Inc/v231/aiso/bin/winx64/AnsysWBU.exe -DSApplet -AppModeMech -nosplash -notabctrl -grpc 10000"

.. note::
   PowerShell users can run the above command without the opening and closing quotation
   marks.


**On Linux**

.. code::

    /usr/ansys_inc/v231/aisol/.workbench -DSApplet -AppModeMech -nosplash -notabctrl -grpc 10000


If the preceding command for your operating system doesn't launch Mechanical, you could have
a variety of issues, including:

  - License server setup
  - Running behind a VPN
  - Missing dependencies


Licensing issues
----------------

`PADT <https://www.padtinc.com/>`_ has an `Ansys <https://www.padtinc.com/simulation/ansys-simulation-products/>`_
product section, and posts about licensing are common. For example, see
`Changes to Licensing at ANSYS 2023R1 <https://www.padtinc.com/blog/15271-2/>`_.

If you are responsible for maintaining an Ansys license or have a personal installation
of Ansys, you likely can access the **Installation and Licensing** section of the
Ansys Help, where you can download the :download:`Ansys, Inc. Licensing Guide <ANSYS_Inc._Licensing_Guide.pdf>`.


VPN issues
----------
Sometimes, Mechanical has issues starting when VPN software is running. For more information,
see the *Mechanical User's Guide* in the **Mechanical Applicaiton** section of the Ansys Help.


Missing dependencies on Linux
-----------------------------
Some Linux installations might be missing required dependencies. For example, this error
might be raised::

    libXp.so.6: cannot open shared object file: No such file or directory

CentOS
~~~~~~
On CentOS 7, you can install required dependencies with:

.. code::

    yum install openssl openssh-clients mesa-libGL mesa-libGLU motif libgfortran


Ubuntu
~~~~~~
Because Mechanical isn't officially supported on Ubuntu, it's a bit more
difficult to install required dependencies. However, it's still possible.

On Ubuntu 20.04 with Ansys 2023 R1, you can install all required dependencies
except for the outdated ``libxp6`` package with:

.. code::

    sudo apt-get install libx11-6 libgl1 libxm4 libxt6 libxext6 libxi6 libx11-6 libsm6 libice6 libxxf86vm1 libglu1

If you are using Ubuntu 16.04, you can install the ``libxp6`` package with:


.. code::

    sudo apt install libxp6

However, on Ubuntu 18.04 and later, you must manually download and install the ``libxp6``
package. Because this package is dependent on another outdated package, ``multiarch-support``,
you must remove it. Otherwise, you'll have a broken package configuration.

This code downloads and modifies the ``libxp6`` package to remove the ``multiarch-support``
package dependency and then installs it with ``dpkg``:

.. code::

    cd /tmp
    wget http://ftp.br.debian.org/debian/pool/main/libx/libxp/libxp6_1.0.2-2_amd64.deb
    ar x libxp6_1.0.2-2_amd64.deb
    sudo tar xzf control.tar.gz
    sudo sed '/Pre-Depends/d' control -i
    sudo bash -c "tar c postinst postrm md5sums control | gzip -c > control.tar.gz"
    sudo ar rcs libxp6_1.0.2-2_amd64_mod.deb debian-binary control.tar.gz data.tar.xz
    sudo dpkg -i ./libxp6_1.0.2-2_amd64_mod.deb

