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

.. note::
   The provided Docker configuration is **experimental** and is intended to produce a
   minimal image for running PyMechanical tests. The
   `.dockerignore <https://github.com/ansys/pymechanical/blob/main/docker/252/.dockerignore>`_
   file deliberately excludes a large number of Mechanical installation files to reduce
   image size. If you encounter issues with missing capabilities or components in your
   container, review and modify the ``.dockerignore`` file to include the additional
   files required for your use case.

The Mechanical Docker image provided in the PyMechanical repository is for internal use. Users must
build it from a local Mechanical installation. Instructions are provided in the PyMechanical
repository under `Make container <https://github.com/ansys/pymechanical/blob/main/docker/make_container.rst>`_,
which uses the `Dockerfile <https://github.com/ansys/pymechanical/blob/main/docker/252/Dockerfile>`_ and
`.dockerignore <https://github.com/ansys/pymechanical/blob/main/docker/252/.dockerignore>`_.

**Step 1: Download Mechanical**

Download the latest Mechanical installer from the
`Ansys Customer Portal <https://download.ansys.com/Current%20Release>`_.

**Step 2: Create Mechanical Docker image**

Install Mechanical on a Linux-based machine that supports the Mechanical product.
Follow `Make container <https://github.com/ansys/pymechanical/blob/main/docker/make_container.rst>`_
to create the Docker image.

**Step 3: Launch the container**

Once the image is built, launch Mechanical by providing the address of your license
server in the ``LICENSE_SERVER`` environment variable:

Note that port ``10000``, which is local to the container, is mapped to port ``10000``
on the host. You can use different port mappings to run multiple instances simultaneously.

By default, the Mechanical container starts a secure gRPC server (mTLS on Linux) when the
Mechanical version supports secure connections (for example, 2025 R2 / 252 with SP03 or later,
and any version released after 261). For a full breakdown of which versions and service packs
enable secure connections by default, see
:ref:`Version and service pack requirements <grpc_security_version_requirements>`.

The following demonstrates how to launch the container in **insecure mode** if you prefer to
connect without encryption. This is not recommended for production environments. To do so,
override the entrypoint and pass
``--transport-mode insecure`` explicitly:

.. code::

    LICENSE_SERVER=1055@XXX.XXX.XXX.XXX
    VERSION=252

    docker run -d \
      -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER \
      -p 10000:10000 \
      --entrypoint=tini \
      mechanical:25.2 \
      -- xvfb-run /install/ansys_inc/v${VERSION}/aisol/.workbench \
      -dsapplet -b -grpc 10000 --grpc-host 0.0.0.0 --transport-mode insecure

As Mechanical starts, you can see status information:

.. code:: console

    Info: Starting the grpc server at port : 10000 (Insecure:0.0.0.0:certs)
    Info: Started the grpc server at port : 10000 (Insecure:0.0.0.0:certs)

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

    docker run -d \
      -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER \
      -p 10000:10000 \
      --entrypoint=tini \
      mechanical:25.2 \
      -- xvfb-run /install/ansys_inc/v${VERSION}/aisol/.workbench \
      -dsapplet -b -grpc 10000 --grpc-host 0.0.0.0 --transport-mode insecure \
      -featureflags mechanical.material.import

For additional command line arguments, see the `Scripting in Mechanical Guide`_ in the
Ansys Help.


For PyMechanical embedding, you can directly enter the container using ``--entrypoint=/bin/bash``
and then install Python packages as needed.

.. code:: bash

    docker run -it -e ANSYSLMD_LICENSE_FILE=$LICENSE_SERVER --entrypoint=/bin/bash mechanical:25.2

    # Once inside the container, you can install Python and packages as needed, then create an embedded app.


.. note::
    Ansys employees can access the Mechanical Docker image provided in the PyMechanical repository by following
    the `running container <https://github.com/ansys/pymechanical/blob/main/docker/run_container.rst>`_ instructions.