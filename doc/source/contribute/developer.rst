Contributing as a developer
===========================

.. grid:: 1 1 3 3

    .. grid-item-card:: :fa:`code-fork` Fork the repository
        :padding: 2 2 2 2
        :link: fork-the-repository
        :link-type: ref

        Learn how to fork the project and get your own copy.

    .. grid-item-card:: :fa:`download` Clone the repository
        :padding: 2 2 2 2
        :link: clone-the-repository
        :link-type: ref

        Download your own copy in your local machine.

    .. grid-item-card:: :fa:`download` Install for developers
        :padding: 2 2 2 2
        :link: install-for-developers
        :link-type: ref

        Install the project in editable mode.

    .. grid-item-card:: :fab:`docker` Adhere to coding style
        :padding: 2 2 2 2
        :link: coding-style
        :link-type: ref

        Adhere to the coding style guidelines using pre-commit hooks.

    .. grid-item-card:: :fa:`vial-circle-check` Run the tests
        :padding: 2 2 2 2
        :link: run-tests
        :link-type: ref

        Verify your changes by testing the project.



.. _fork-the-repository:

Fork the repository
===================

Forking the repository is the first step to contributing to the project. This
allows you to have your own copy of the project so you can make changes without
affection the main project. Once you have made your changes, you can submit a
pull-request to the main project to have your changes reviewed and merged.

.. button-link:: https://github.com/ansys/pymechanical/fork
    :color: primary
    :align: center

    :fa:`code-fork` Fork this project

.. note::

    If you are an Ansys employee, you can skip this step.

.. _clone-the-repository:

Clone the repository
====================

Make sure you `configure SSH`_ with your GitHub
account. This allows you to clone the repository without having to use tokens
or passwords. Also, make sure you have `git`_ installed in your machine.

To clone the repository using SSH, run:

.. code-block:: bash

    git clone git@github.com:ansys/pymechanical

.. note::

    If you are not an Ansys employee, you need to :ref:`fork the repository <fork-the-repository>` and
    replace ``ansys`` with your GitHub user name in the ``git clone``
    command.

.. _install-for-developers:

Install for developers
======================

Installing PyMechanical in development mode allows you to perform changes to the code
and see the changes reflected in your environment without having to reinstall
the library every time you make a change.

Virtual environment
-------------------

Start by navigating to the project's root directory by running:

.. code-block::

    cd pymechanical

Then, create a new virtual environment named ``.venv`` to isolate your system's
Python environment by running:

.. code-block:: text

    python -m venv .venv

Finally, activate this environment by running:

.. tab-set::

    .. tab-item:: Windows

        .. tab-set::

            .. tab-item:: CMD

                .. code-block:: text

                    .venv\Scripts\activate.bat

            .. tab-item:: PowerShell

                .. code-block:: text

                    .venv\Scripts\Activate.ps1

    .. tab-item:: macOS/Linux/UNIX

        .. code-block:: text

            source .venv/bin/activate

Development mode
----------------

Now, install PyMechanical in editable mode by running:

.. code-block:: text

    python -m pip install --editable .

Verify the installation by checking the version of the library:


.. code-block:: python

    from ansys.mechanical.core import __version__


    print(f"PyMechanical version is {__version__}")


.. _run-tests:

Run the tests
=============

PyMechanical uses `PyTest`_ and `tox`_ for unit testing. Prior to running the tests,
ensure Mechanical is installed on your system with a valid license and the test
dependencies are installed. Run this command to install the test dependencies::

  pip install -e .[tests]


Using ``pytest``
----------------

To run the tests, navigate to the root directory of the repository and run this command::

    pytest

The ``pytest`` command runs all of the tests in the ``tests`` folder. After ``pytest`` is
done running, it shows the test coverage of each of the files in the repository. To run
specific tests, run these commands::

    # Run tests for embedded instances
    pytest -m embedding

    # Run tests for embedded instances that use subprocess
    pytest -m embedding_scripts

    # Run tests that launch Mechanical and work with the gRPC server inside of it
    pytest -m remote_session_launch

    # Run tests that connect to Mechanical and work with the gRPC server inside of it
    pytest -m remote_session_connect

See the ``pyproject.toml`` file for a full list of markers (-m) and their descriptions.

To run specific tests based on a keyword, use the ``-k`` argument::

    # Run all tests containing the word ``appdata``
    # This would run ``test_private_appdata`` and ``test_normal_appdata`` only
    pytest -k appdata


Using ``tox``
-------------

This project takes advantage of `tox`_. This tool automates common development
tasks (similar to ``Makefile``), but it is oriented towards Python development.

While ``Makefile`` has rules, ``tox`` has environments. In fact, ``tox``
creates its own virtual environment so that anything being tested is isolated
from the project to guarantee the project's integrity.

The following environment commands are provided:

- ``tox -e style``: Checks for coding style quality.
- ``tox -e py``: Checks for unit tests.
- ``tox -e py-coverage``: Checks for unit testing and code coverage.
- ``tox -e doc``: Checks for documentation-building process.


Remote testing
--------------

If you do not have a licensed copy of Mechanical installed locally but want to
run PyMechanical unit tests on a remote instance, you must set up environment
variables.

**On Linux**

.. code::

    export PYMECHANICAL_START_INSTANCE=False
    export PYMECHANICAL_PORT=<MECHANICAL Port> (default 10000)
    export PYMECHANICAL_IP=<MECHANICAL IP> (default 127.0.0.1)

**On Windows**

.. code::

    SET PYMECHANICAL_START_INSTANCE=False
    SET PYMECHANICAL_PORT=<MECHANICAL Port> (default 10000)
    SET PYMECHANICAL_IP=<MECHANICAL IP> (default 127.0.0.1)

The environment variables for your operating system tell PyMechanical
to attempt to connect to the existing Mechanical service by default
when you use the :func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>`
method.


.. _coding-style:

Adhere to coding style
======================

As indicated in `Coding style <https://dev.docs.pyansys.com/coding-style/index.html>`_
in the *PyAnsys Developer's Guide*, PyMechanical follows PEP8 guidelines. PyMechanical
implements `pre-commit <https://pre-commit.com/>`_ for style checking.

To ensure your code meets minimum code styling standards, run these commands::

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook by running this command::

  pre-commit install

This way, it's not possible for you to push code that fails the style checks::

  $ pre-commit install
  $ git commit -am "added my cool feature"
  check pre-commit.ci config...............................................Passed
  black....................................................................Passed
  blacken-docs.............................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  codespell................................................................Passed
  Add License Headers......................................................Passed
  Ansys Technical Review...................................................Passed
  pydocstyle...............................................................Passed
  check for merge conflicts................................................Passed
  debug statements (python)................................................Passed
  check yaml...............................................................Passed
  trim trailing whitespace.................................................Passed
  check for added large files..............................................Passed
  Validate GitHub Workflows................................................Passed