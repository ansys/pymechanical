Pull and Run the Mechanical Docker Image
----------------------------------------

.. warning::

   This section is intended for **Ansys internal use only**.

There is a Docker image hosted in the `PyMechanical GitHub
<https://github.com/ansys/pymechanical/pkgs/container/mechanical>`_ repository that you
can download using your GitHub credentials.

Assuming that you have Docker installed, you can authorize Docker to access
this repository using a GitHub personal access token with ``packages read``
permission. For more information, see GitHub's `Creating a personal access token
<https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens>`_.

Save this token to a file with a command like this:

.. code::

   echo XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX > GH_TOKEN.txt

This command lets you send the token to Docker without leaving the token value
in your history.

Next, authorize Docker to access the repository with this code:

.. code::

    GH_USERNAME=<my-github-username>
    cat GH_TOKEN.txt | docker login ghcr.io -u $GH_USERNAME --password-stdin

Pull the docker image

.. code::

    docker pull ghcr.io/ansys/mechanical:latest

For particular version use version tag.

.. code::

    docker pull ghcr.io/ansys/mechanical:25.2.0

You can now launch Mechanical directly from Docker with a short script or directly from the command line.
Refer to the `PyAnsys Mechanical Docker documentation
<https://mechanical.docs.pyansys.com/version/dev/getting_started/docker.html#build-your-own-mechanical-docker-image>`_ for the command line.
This section also describes how to build your own Mechanical Docker image.
