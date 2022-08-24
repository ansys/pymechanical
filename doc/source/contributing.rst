.. _ref_contributing:

============
Contributing
============
Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <https://dev.docs.pyansys.com/overview/contributing.html>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with it and all `Guidelines and Best Practices
<https://dev.docs.pyansys.com/guidelines/index.html>`_ before attempting to
contribute to PyMechanical.
 
The following contribution information is specific to PyMechanical.

Cloning the PyMechanical Repository
-----------------------------------
Run this code to clone and install the latest version of PyMechanical in development mode:

.. code::

    git clone https://github.com/pyansys/pymechanical
    cd pymechanical
    pip install pip -U
    pip install -e .


Posting Issues
--------------
Use the `PyMechanical Issues <https://github.com/pyansys/pymechanical/issues>`_
page to submit questions, report bugs, and request new features. When possible, we
recommend that you use these issue templates:

* Bug report template
* Feature request template

If your issue does not fit into one of these categories, create your own issue.

To reach the project support team, email `pyansys.support@ansys.com <pyansys.support@ansys.com>`_.

Viewing PyMechanical Documentation
----------------------------------
Documentation for the latest stable release of PyMechanical is hosted at
`PyMechanical Documentation <https://mechanical.docs.pyansys.com>`_.

Documentation for the latest development version, which tracks the
``main`` branch, is hosted at  `Development PyMechanical Documentation <https://dev.mechanical.docs.pyansys.com/>`_.
This version is automatically kept up to date via GitHub actions.

Testing Mechanical
------------------
If you do not have Mechanical installed locally but still want to run the
unit testing, you must set up the following environment variables.

In Windows, use:

.. code::

    SET PYMECHANICAL_START_INSTANCE=False
    SET PYMECHANICAL_PORT=<MECHANICAL Port> (default 10000)
    SET PYMECHANICAL_IP=<MECHANICAL IP> (default 127.0.0.1)

In Linux, use:

.. code::

    export PYMECHANICAL_START_INSTANCE=False
    export PYMECHANICAL_PORT=<MECHANICAL Port> (default 10000)
    export PYMECHANICAL_IP=<MECHANICAL IP> (default 127.0.0.1)

This tells ``ansys.mechanical.core`` to attempt to connect to the existing
Mechanical service by default when the ``launch_mechanical`` function is used.


Code Style
----------
PyMechanical follows PEP8 standard as outlined in the `PyAnsys Development Guide
<https://dev.docs.pyansys.com>`_ and implements style checking using
`pre-commit <https://pre-commit.com/>`_.

To ensure your code meets minimum code styling standards, run::

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook by running::

  pre-commit install

This way, it's not possible for you to push code that fails the style checks. For example::

  $ pre-commit install
  $ git commit -am "added my cool feature"
  black....................................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  codespell................................................................Passed

