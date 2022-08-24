.. _using_standard_install:

********************************************
Using PyMechanical from the Standard Install
********************************************

The pyansys ``ansys-mechanical-core`` package requires either a local or
remote instance of Mechanical to communicate with it.  This section covers
launching and interfacing with Mechanical from a local instance by
launching it from Python.

Installing Mechanical
---------------------

Mechanical is installed by default from the standard installer.  When
installing ANSYS, verify that the "Mechanical Products" option is
checked under the "Structural Mechanics" option.  The standard
installer options may change, but for reference see the following
figure.

.. figure:: ../images/unified_install_2023R1.jpg
    :width: 400pt


Launching Mechanical
--------------------

Launching Mechanical locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the ``launch_mechanical`` function to have Python startup Mechanical and
automatically connect to it:

.. code:: python

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mechanical = launch_mechanical()
    >>> print(mechanical)

    Ansys Mechanical [Ansys Mechanical Enterprise]
    Product Version:231
    Software build date:Wednesday, August 10, 2022 4:28:15 PM


This is the easiest and fastest way to get PyMechanical up and running. 
But you need to have an ANSYS license server installed locally. 

Launching a gRPC Mechanical session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can start Mechanical from the command line and then connect to it.
To launch Mechanical on Windows (assuming a ``C:/Program Files/ANSYS Inc/v231`` installation) use:

.. code::

    C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/.AnsysWBU.exe -DSApplet -AppModeMech -nosplash -notabctrl -grpc 10000

Or on Linux (assuming a ``/usr/ansys_inc`` installation):

.. code::

    /usr/ansys_inc/v231/aisol/.workbench -dsapplet -AppModeMech -nosplash -notabctrl -grpc 10000

This starts up Mechanical in gRPC mode, and Mechanical should output:

.. code::

    Starting the grpc server at port 10000
    Started the grpc server at port 10000

You can configure the port Mechanical starts on with the ``-grpc`` argument.  For
example, you can startup the server to listen for connections at 
port 10001 with:

.. code::

    /usr/ansys_inc/v211/ansys/bin/ansys211 -grpc 10001


Connecting to a gRPC Mechanical session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Mechanical gRPC server can be connected to either from the same host, or from an
external host.  For example, you can connect to a Mechanical service
running **locally** with:

.. code::

    >>> from ansys.mechanical.core import Mechanical
    >>> mechanical = Mechanical()


This assumes that your Mechanical service is running locally on the default ip 
(127.0.0.1) and on the default port (10000).

If you want to connect to a **remote** instance of Mechanical and you know the IP 
address of that instance, you can connect to it.
For example, if on your local network at IP ``192.168.0.1`` there is a
computer running Mechanical on the port 50052, you can connect to it with

.. code::

    >>> mechanical = Mechanical('192.168.0.1', port=10000)

Alternatively you can use a hostname:

.. code:: python

    >>> mechanical = Mechanical('myremotemachine', port=10000)

Please note that you must have started Mechanical in gRPC mode in the PC with
the mentioned IP/hostname for this to work.
If you have Mechanical installed on your local host, you
can use ``launch_mechanical`` to both start and connect to Mechanical.


Debugging Launching Mechanical
------------------------------
For any number of reasons, Python may fail to launch Mechanical.  Here's
some approaches to debug the start:


Manually Set the Executable Location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you have a non-standard install, ``pymechanical`` may be unable find
your installation.  If that's the case, provide the location of Mechanical
as the first parameter to ``launch_mechanical``.  For example, on Windows,
this will be:

.. code:: python

    >>> from ansys.mechanical.core import launch_mechanical
    >>> exec_loc = 'C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/AnsysWBU.exe'
    >>> mechanical = launch_mechanical(exec_loc)

For Linux:

.. code:: python

    >>> from ansys.mechanical.core import launch_mechanical
    >>> exec_loc = '/usr/ansys_inc/v231/aisol/.workbench'
    >>> mechanical = launch_mechanical(exec_loc)

Should this fail to launch or hang while launching, pass
``verbose_mechanical=True`` when using ``launch_mechanical``.  This will print
the output of Mechanical within Python and can be used to debug why Mechanical
isn't launching.  Output will be limited on Windows due to the way
Mechanical launches on Windows.


Debug Launch Issues
~~~~~~~~~~~~~~~~~~~
In some cases, it may be necessary to debug why Mechanical isn't launching
by running the launch command manually from the command line.  In
Windows, open up a command prompt and run the following (version
dependent) command:

.. code::

    "C:/Program Files/ANSYS Inc/v231/aiso/bin/winx64/AnsysWBU.exe -DSApplet -AppModeMech -nosplash -notabctrl -grpc 10000"

.. note::
   Powershell users can run the above without quotes.


For Linux:

.. code::

    /usr/ansys_inc/v231/aisol/.workbench -DSApplet -AppModeMech -nosplash -notabctrl -grpc 10000

If this command doesn't launch, you could have a variety of issues, including:

  - License server setup
  - Running behind a VPN
  - Missing dependencies


Licensing Issues
----------------

PADT generally has a great blog regarding ANSYS issues, and licensing is always a common issue (for example `Changes to Licensing at ANSYS 2023R1 <https://www.padtinc.com/blog/15271-2/>`_).  Should you be responsible for maintaining Ansys licensing or have a personal install of Ansys, please check the online Ansys licensing documentation at `Installation and Licensing <https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/prod_page.html?pn=Installation%20and%20Licensing&pid=InstallationAndLicensing&lang=en>`_.

For an in-depth explanation, please see the :download:`ANSYS Licensing Guide <ANSYS_Inc._Licensing_Guide.pdf>`.


VPN Issues
----------
Sometimes, Mechanical has issues starting when VPN software is running. Refer the Mechanical documentation for mere help.


Missing Dependencies on Linux
-----------------------------
Some Linux installations may be missing required dependencies.  Should
you get errors like ``libXp.so.6: cannot open shared object file: No
such file or directory``, you may be missing some necessary
dependencies.

CentOS
~~~~~~
On CentOS 7, you can install these with:

.. code::

    yum install openssl openssh-clients mesa-libGL mesa-libGLU motif libgfortran


Ubuntu
~~~~~~
Since Mechanical isn't officially supported on Ubuntu, it's a bit more
difficult to setup, but it's still possible.  On Ubuntu 20.04 with
Ansys 2023R1, install the following:

.. code::

    sudo apt-get install libx11-6 libgl1 libxm4 libxt6 libxext6 libxi6 libx11-6 libsm6 libice6 libxxf86vm1 libglu1

This takes care of everything except for ``libxp6``.  Should you be
using Ubuntu 16.04, you can install that simply with ``sudo apt
install libxp6``.  However, on Ubuntu 18.04+, you must manually
download and install the package.

Since ``libxpl6`` also pre-depends on ``multiarch-support``, which is
also outdated, it must be removed, otherwise you'll have a broken
package configuration.  The following step downloads and modifies the
``libxp6`` package to remove the ``multiarch-support`` dependency, and
then installs it via ``dpkg``.

.. code::

    cd /tmp
    wget http://ftp.br.debian.org/debian/pool/main/libx/libxp/libxp6_1.0.2-2_amd64.deb
    ar x libxp6_1.0.2-2_amd64.deb
    sudo tar xzf control.tar.gz
    sudo sed '/Pre-Depends/d' control -i
    sudo bash -c "tar c postinst postrm md5sums control | gzip -c > control.tar.gz"
    sudo ar rcs libxp6_1.0.2-2_amd64_mod.deb debian-binary control.tar.gz data.tar.xz
    sudo dpkg -i ./libxp6_1.0.2-2_amd64_mod.deb
