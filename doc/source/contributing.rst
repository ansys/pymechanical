.. _ref_contributing:

==========
Contribute
==========
Overall guidance on contributing to a PyAnsys library appears in the
`Contribute <https://dev.docs.pyansys.com/overview/contributing.html>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with it, and all `Guidelines and Best Practices
<https://dev.docs.pyansys.com/guidelines/index.html>`_, before attempting to
contribute to PyMechanical.
 
The following contribution information is specific to PyMechanical.

Clone the repository
--------------------
Run this code to clone and install the latest version of PyMechanical in
development mode:

.. code::

    git clone https://github.com/pyansys/pymechanical
    cd pymechanical
    pip install pip -U
    pip install -e .


Post issues
-----------
Use the `PyMechanical Issues <https://github.com/pyansys/pymechanical/issues>`_
page to submit questions, report bugs, and request new features. When possible,
you should use these templates:

* Bug report template
* Feature request template

If your issue does not fit into one of these template categories, create your own issue.

To reach the PyAnsys support team, email `pyansys.support@ansys.com <pyansys.support@ansys.com>`_.

View documentation
------------------
Documentation for the latest stable release of PyMechanical is hosted at
`PyMechanical Documentation <https://mechanical.docs.pyansys.com>`_.

Documentation for the latest development version, which tracks the
``main`` branch, is hosted at `Development PyMechanical Documentation <https://dev.mechanical.docs.pyansys.com/>`_.
This version is automatically kept up to date via GitHub actions.

Test PyMechanical
-----------------
If you do not have a licensed copy of Mechanical installed locally but
still want to run PyMechanical unit tests, you must set up environment
variables.

**On Windows**

.. code::

    SET PYMECHANICAL_START_INSTANCE=False
    SET PYMECHANICAL_PORT=<MECHANICAL Port> (default 10000)
    SET PYMECHANICAL_IP=<MECHANICAL IP> (default 127.0.0.1)

**On Linux**

.. code::

    export PYMECHANICAL_START_INSTANCE=False
    export PYMECHANICAL_PORT=<MECHANICAL Port> (default 10000)
    export PYMECHANICAL_IP=<MECHANICAL IP> (default 127.0.0.1)


The environment variables for your operating system tell PyMechanical 
to attempt to connect to the existing Mechanical service by default
when you use the ``launch_mechanical`` method.


Code style
----------
PyMechanical follows the PEP8 standard as outlined in the `PyAnsys Development Guide
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

