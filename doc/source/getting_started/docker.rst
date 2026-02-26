.. _ref_docker:

Using Mechanical through Docker
===============================

You can run Mechanical within a container on any operating system
using `Docker <https://www.docker.com/>`_ and connect to it with
PyMechanical.

Running Mechanical in a containerized environment like Docker or `Apptainer <https://apptainer.org/>`_
(formerly Singularity) is advantageous for several reasons, including:

- Ability to run in a consistent environment regardless of the host operating system
- Portability and ease of installation
- Large-scale cluster deployment using `Kubernetes <https://kubernetes.io/>`_
- Genuine application isolation through containerization

Build your own Mechanical Docker image
--------------------------------------

.. warning:: You need a valid Ansys license and an Ansys account to complete these steps.

.. note::
   The provided Docker configuration is **experimental** and is intended to produce a
   minimal image for running PyMechanical tests. The
   `.dockerignore <https://github.com/ansys/pymechanical/tree/main/docker/252/.dockerignore>`_
   file deliberately excludes a large number of Mechanical installation files to reduce
   image size. If you encounter issues with missing capabilities or components in your
   container, review and modify the ``.dockerignore`` file to include the additional
   files required for your use case.

Because the Mechanical Docker image is for internal use, you must build your own image
from a local Mechanical installation. The following steps summarize the process.
For full details, see the
`Dockerfile <https://github.com/ansys/pymechanical/blob/main/docker/252/Dockerfile>`_ and
`.dockerignore <https://github.com/ansys/pymechanical/blob/main/docker/252/dockerignore>`_
files in the PyMechanical repository.

**Step 1: Download Mechanical**

Download the latest Mechanical installer from the
`Ansys Customer Portal <https://download.ansys.com/Current%20Release>`_.

**Step 2: Install Mechanical on a Linux machine**

Install Mechanical on a Linux-based machine that supports the Mechanical product. To minimize the image size,
use the silent installer with only the required components:

.. code:: bash

    sh /path-to-mechanical-installer \
        -silent -overwrite_preview -mechapdl -lsdyna \
        -install_dir /path-to-install-mechanical/

**Step 3: Build the Docker image**

Use the provided Docker configuration files and the script below, adapting the paths
to your environment:

.. code:: bash

    export ANS_MAJOR_VERSION=25
    export ANS_MINOR_VERSION=2
    export ANS_VERSION=${ANS_MAJOR_VERSION}${ANS_MINOR_VERSION}
    export TAG=mechanical:${ANS_MAJOR_VERSION}.${ANS_MINOR_VERSION}

    # Path where Mechanical is installed (e.g. /usr/install/ if installed under /usr/install/ansys_inc/v252)
    export MECHANICAL_INSTALL_LOCATION=/path_to_mechanical_installation/

    # Path where the PyMechanical repository is cloned
    export PYMECHANICAL_LOCATION=/path-to-pymechanical

    cd ${MECHANICAL_INSTALL_LOCATION}

    cp ${PYMECHANICAL_LOCATION}/pymechanical/docker/${ANS_VERSION}/Dockerfile .
    cp ${PYMECHANICAL_LOCATION}/pymechanical/docker/${ANS_VERSION}/.dockerignore .

    sudo docker build -t $TAG --build-arg VERSION=$ANS_VERSION .

**Step 4: Launch the container**

Once the image is built, launch Mechanical by providing the address of your license
server in the ``LICENSE_SERVER`` environment variable:

.. code::

    LICENSE_SERVER=1055@XXX.XXX.XXX.XXX

    docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p 10000:10000 mechanical:25.2

Note that port ``10000``, which is local to the container, is mapped to port ``10000``
on the host. You can use different port mappings to run multiple instances simultaneously.

As Mechanical starts, you can see status information:

.. code::

    Starting the grpc server at port 10000
    Started the grpc server at port 10000

Launch in insecure mode
~~~~~~~~~~~~~~~~~~~~~~~

Mechanical versions that have the required service pack installed (for example, 2025 R2 / 252
with SP03 or later) and any version released after 252 default to secure gRPC transport (mTLS
on Linux). If you do not want to use mTLS and prefer to connect without encryption, you must
launch the container explicitly in insecure mode. For a full breakdown of which versions and
service packs enable secure connections by default, see
:ref:`Version and service pack requirements <grpc_security_version_requirements>`.

To launch in **insecure mode** (no encryption), override the entrypoint and pass
``--transport-mode insecure`` explicitly:

.. code::

    LICENSE_SERVER=1055@XXX.XXX.XXX.XXX
    VERSION=252

    docker run -d \
      -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER \
      -p 10000:10000 \
      --entrypoint="" \
      mechanical:25.2 \
      tini -- xvfb-run /install/ansys_inc/v${VERSION}/aisol/.workbench \
      -dsapplet -b -grpc 10000 --grpc-host 0.0.0.0 --transport-mode insecure

.. note::
   ``--entrypoint=""`` clears the default entrypoint so that the full command can be
   supplied directly.

Connect to the Mechanical container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can now connect to the Mechanical container with this code:

.. code:: python

    from ansys.mechanical.core import Mechanical

    mechanical = Mechanical()

If you launched the container in insecure mode, pass ``transport_mode="insecure"``
when connecting:

.. code:: python

    from ansys.mechanical.core import Mechanical

    mechanical = Mechanical(port=10000, transport_mode="insecure")

If you mapped to any port other than ``10000``, specify it when connecting:

.. code:: python

    mechanical = Mechanical(port=f"{my_port}")

Verify your connection with this code:

.. code:: pycon

    >>> mechanical
    Ansys Mechanical [Ansys Mechanical Enterprise]
    Product Version:252
    Software build date: 06/13/2025 15:54:58

Additional considerations
-------------------------

You can provide additional command line parameters to Mechanical by appending them
to the Docker command. For example, this code shows how you pass feature flags:

.. code::

    docker run -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER -p 10000:10000 mechanical:25.2 -featureflags mechanical.material.import;

For additional command line arguments, see the `Scripting in Mechanical Guide`_ in the
Ansys Help.
