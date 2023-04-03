
Create your own Mechanical docker container
===========================================

.. warning:: You need a valid Ansys license and an Ansys account to
   follow the steps detailed in this section.

You can create your own Mechanical docker container following
the steps given in this page.
This guide will use a local Ubuntu machine to generate the needed
files for the Mechanical container by installing Ansys products first
and then copy the generated files to the container.


Requirements
============

* A linux machine, preferable with Ubuntu 18.04 or later.
  CentOS Linux distribution is not supported anymore.
  This machine needs to have `Docker <https://www.docker.com>`_ installed.

* A valid Ansys account. Your Ansys reseller should have
  provide you with one.

* The following provided files:
  
  * `Dockerfile <https://github.com/pyansys/pymechanical/tree/main/docker/231/Dockerfile>`_
  * `.dockerignore <https://github.com/pyansys/pymechanical/tree/main/docker/231/.dockerignore>`_


Procedure
=========

Download Ansys Mechanical installation files
--------------------------------------------

Download latest Ansys Mechanical version from the customer portal 
(`Current Release <ansys_current_release_>`_).
You need to have a valid Ansys account with access to
products downloads.

If you lack of an Ansys account, please contact your
IT manager.


Install Ansys Mechanical product
--------------------------------

To install Ansys Mechanical product on an Ubuntu machine you can follow 
:ref:`install_mechanical` if you are using the graphical user interface
or :ref:`installing_ansys_in_wsl` for the command line interface.
The later approach can be reused with small changes in a
continuous integration workflow.

To reduce the size of the final image, you might want to
install the minimal files by using:

.. code:: bash

    sh /path-to-mechanical-installer \
        -install_dir /path-to-install-mechanical/ \
        -nochecks -mechapdl -silent

This command install Mechanical (``-mechapdl``).

Please take note of where you are installing ANSYS because the
directory path is need in the following section.

Build Docker image
------------------

To build the Docker image, you need to create a directory and copy
all the files you need in the image.

The steps to copy those files and build the image are detailed in the following script,
which you should modify to adapt it to your needs.

.. code:: bash

    # Creating env vars for the Dockerfile
    export ANS_MAJOR_VERSION=23
    export ANS_MINOR_VERSION=1
    export ANS_VERSION=${ANS_MAJOR_VERSION}${ANS_MINOR_VERSION}

    export TAG=mechanical:${ANS_MAJOR_VERSION}.${ANS_MINOR_VERSION}
    # example: if Mechanical v231 is install under
    # /install/ansys_inc/v231
    # use /install for path_to_mechanical_installation
    export MECHANICAL_INSTALL_LOCATION=/path_to_mechanical_installation/

    # example: if pymechanical is cloned under
    # /some_location/pymechanical
    # use /some_location for path-to-pymechanical
    export PYMECHANICAL_LOCATION=/path-to-pymechanical

    # Creating working directory
    cd ${MECHANICAL_INSTALL_LOCATION}

    # Copying the docker files
    # 
    cp ${PYMECHANICAL_LOCATION}/pymechanical/docker/{ANS_VERSION}/Dockerfile .
    cp ${PYMECHANICAL_LOCATION}/pymechanical/docker/{ANS_VERSION}/.dockerignore .

    # Build Docker image
    sudo docker build  -t $TAG --build-arg VERSION=$ANS_VERSION .

Please notice that:

* ``path-to-pymechanical`` is the path where PyMechanical repository is located.
* ``path_to_mechanical_installation`` is the path to where you have locally installed ANSYS Mechanical.

Not all the installation files are copied, in fact, the files ignored during the copying
are detailed in the file `.dockerignore <https://github.com/pyansys/pymechanical/tree/main/docker/231/.dockerignore>`_.

The Docker container configuration needed to build the container is detailed in the
`Dockerfile <https://github.com/pyansys/pymechanical/tree/main/docker/231/Dockerfile>`_.


Summary
=======


* **Step 1:** Download latest Ansys Mechanical version from the customer portal 
  (`Current Release <ansys_current_release_>`_).

* **Step 2:** Install Ansys Mechanical in a known folder. You can reuse your local
  installation if it is updated and the machine is running the same Ubuntu
  version as the targe Ubuntu docker version.

* **Step 3:** Build the docker image with the provided Docker configuration files
  and script.
