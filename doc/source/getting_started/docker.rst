.. _docker:

********************************
Using Mechanical Through Docker
********************************
You can run Mechanical within a container on any OS using `docker` and
connect to it via PyMechanical.

There are several situations in which it is advantageous to run Mechanical
in a containerized environment (e.g. Docker or singularity):

- Run in a consistent environment regardless of the host OS.
- Portability and ease of install.
- Large scale cluster deployment using Kubernetes
- Genuine application isolation through containerization.


Installing the Mechanical Image
-------------------------------
There is a docker image hosted on the `PyMechanical GitHub
<https://https://github.com/pyansys/pymechanical>`_ repository that you
can download using your GitHub credentials.

Assuming you have docker installed, you can get started by
authorizing docker to access this repository using a personal access
token.  Create a GH personal access token with ``packages read`` permissions
according to `Creating a personal access token <https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token>`_

Save that token to a file with:

.. code::

   echo XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX > GH_TOKEN.txt


This lets you send the token to docker without leaving the token value
in your history.  Next, authorize docker to access this repository
with:

.. code::

    GH_USERNAME=<my-github-username>
    cat GH_TOKEN.txt | docker login ghcr.io -u $GH_USERNAME --password-stdin


You can now launch Mechanical directly from docker with a short script or
directly from the command line.  Since this image contains no license
server, you will need to enter in your license server IP address the
``LICENSE_SERVER`` environment variable.  With that, you can launch
Mechanical with:

.. code::

    LICENSE_SERVER=1055@XXX.XXX.XXX.XXX
    VERSION=v23.1.0

    IMAGE=ghcr.io/pyansys/pymechanical/mechanical:$VERSION
    docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p ip:10000:10000 $IMAGE


Note that port `10000` (local to the container) is being mapped to
10000 on the host.  This makes it possible to launch several Mechanical
instances with different port mappings to allow for multiple instances
of Mechanical.

Once you've launched Mechanical you should see:

.. code::

    Starting the grpc server at port 10000
    Started the grpc server at port 10000


Connecting to the Mechanical Container from Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can now connect to the instance with:

.. code:: python

    >>> from ansys.mechanical.core import Mechanical
    >>> mechanical = Mechanical()

If you mapped to any other port other than 50052, you should specify
that port when connecting to Mechanical with:

.. code:: python

    >>> mechanical = Mechanical(port=<my-port>)

Verify your connection with:

.. code:: python

    >>> print(mechanical)

    Ansys Mechanical [Ansys Mechanical Enterprise]
    Product Version:231
    Software build date:Wednesday, August 10, 2022 4:28:15 PM

Additional Considerations
-------------------------
In the command:

.. code::

    IMAGE=ghcr.io/pyansys/pymechanical/mechanical:$VERSION
    docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p 50052:50052 $IMAGE -featureflags "mechanical.material.import;"

You can provide additional command line parameters to Mechanical by simply
appending to the docker command.  For example, you can pass feature flags

For additional command line arguments please see the ansys
documentation at `ANSYS help <https://ansyshelp.ansys.com>`_.
