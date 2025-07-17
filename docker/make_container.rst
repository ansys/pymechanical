
Create your own Mechanical Docker container
===========================================

.. warning:: You need a valid Ansys license and an Ansys account to
   complete the steps in this section.

You can create your own Mechanical Docker container following
the steps on this page.
These steps use a local Ubuntu machine to generate the needed
files for the Mechanical container by installing Ansys products first
and then copying the generated files to the container.


Requirements
============

* A Linux machine, preferable with Ubuntu 20.04 or later.
  CentOS Linux distribution is no longer supported.
  This machine needs to have `Docker <https://www.docker.com>`_ installed.

* A valid Ansys account. Your Ansys reseller should have
  provided you with an account.

* These files are provided:

  * `Dockerfile <https://github.com/ansys/pymechanical/tree/main/docker/252/Dockerfile>`_

  * `.dockerignore <https://github.com/ansys/pymechanical/tree/main/docker/252/.dockerignore>`_


Procedure
=========

Download Mechanical installation files
--------------------------------------------

Download the latest Mechanical version from the Ansys Customer Portal
(`Current Release <https://download.ansys.com/Current%20Release>`_).
You need to have a valid Ansys account with access to
the products to download.

If you do not Ansys account information, contact your
IT manager.


Install Mechanical product
--------------------------------

To install Mechanical product on an Ubuntu machine you can follow
`Install Mechanical <https://mechanical.docs.pyansys.com/version/stable/getting_started/running_mechanical.html#install-mechanical>`_
if you are using the graphical user interface
or `Install Ansys products in WSL <https://mechanical.docs.pyansys.com/version/stable/getting_started/wsl.html#install-ansys-products>`_
for the command line interface. The later approach can be reused with small changes in a
continuous integration workflow.

To reduce the size of the final image, you might want to
install the minimal files by using:

.. code:: bash

    sh /path-to-mechanical-installer \
        -silent -overwrite_preview -mechapdl -lsdyna \
        -install_dir /path-to-install-mechanical/

    # example
    # sh /home/username/download/linx/INSTALL \
    #    -silent -overwrite_preview -mechapdl -lsdyna \
    #    -install_dir /install/ansys_inc/


Use ``sudo`` if you do not have write permissions in the installation directory.
The ``-mechapdl`` command installs Mechanical.

Take note of where you are installing Ansys because the
directory path is need in the following section.

Build Docker image
------------------

To build the Docker image, you must create a directory and copy
all the files you need in the image into this directory.

The steps to copy these files and build the image are provided in the following script,
which you should modify to adapt it to your needs.

.. code:: bash

    # Create env vars for the Dockerfile
    export ANS_MAJOR_VERSION=25
    export ANS_MINOR_VERSION=2
    export ANS_VERSION=${ANS_MAJOR_VERSION}${ANS_MINOR_VERSION}

    export TAG=mechanical:${ANS_MAJOR_VERSION}.${ANS_MINOR_VERSION}

    # example: if Mechanical v252 is installed under usr/install/ansys_inc/v252
    # use export MECHANICAL_INSTALL_LOCATION=/usr/install/
    export MECHANICAL_INSTALL_LOCATION=/path_to_mechanical_installation/

    # example: if pymechanical is cloned under /some_location/pymechanical
    # use /some_location for path-to-pymechanical
    export PYMECHANICAL_LOCATION=/path-to-pymechanical

    # Create working directory
    cd ${MECHANICAL_INSTALL_LOCATION}

    # Copy the Docker files
    cp ${PYMECHANICAL_LOCATION}/pymechanical/docker/${ANS_VERSION}/Dockerfile .
    cp ${PYMECHANICAL_LOCATION}/pymechanical/docker/${ANS_VERSION}/.dockerignore .

    # Build Docker image
    sudo docker build  -t $TAG --build-arg VERSION=$ANS_VERSION .

Take note of the these paths:

* ``path-to-pymechanical`` is the path where PyMechanical repository is located.
* ``path_to_mechanical_installation`` is the path to where you have locally installed Mechanical.

Not all installation files are copied. In fact, the files ignored during the copying
are described in the `.dockerignore file <https://github.com/ansys/pymechanical/tree/main/docker/252/.dockerignore>`_.

The Docker container configuration needed to build the container is described in the
`Dockerfile <https://github.com/ansys/pymechanical/tree/main/docker/252/Dockerfile>`_.


Summary
=======


* **Step 1:** Download the latest Mechanical version from the Ansys Customer Portal
  (`Current Release <https://download.ansys.com/Current%20Release>`_).

* **Step 2:** Install Mechanical in a known folder. You can reuse your local
  installation if it is updated and the machine is running the same Ubuntu
  version as the target Ubuntu Docker version.

* **Step 3:** Build the Docker image with the provided Docker configuration files
  and script.
