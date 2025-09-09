Contributing as a documentarian
===============================

.. grid:: 1 1 3 3

    .. grid-item-card:: :fa:`pencil` Write documentation
        :padding: 2 2 2 2
        :link: write-documentation
        :link-type: ref

        Explain how to get started, use, and contribute to the project.

    .. grid-item-card:: :fa:`laptop-code` Add a new example
        :padding: 2 2 2 2
        :link: write-examples
        :link-type: ref

        Showcase the capabilities of PyMechanical by adding a new example.

    .. grid-item-card:: :fa:`file-code` Build the documentation
        :padding: 2 2 2 2
        :link: build-documentation
        :link-type: ref

        Render the documentation to see your changes reflected.

.. _write-documentation:

Write documentation
===================

The documentation generator used in PyMechanical is `Sphinx`_. Most of the documents
are written in `reStructuredText`_. Some parts of the documentation, like the
:ref:`Examples <ref_examples>`, use Python files. If
you are interested in writing examples, see the :ref:`writing examples <write-examples>`
section.

The documentation is located in the ``doc/source`` directory. The landing page
is declared in the ``doc/source/index.rst`` file. The rest of the files contain
the main pages of different sections of the documentation. Finally, the
``doc/source/_static/`` folder contains various assets like images, and CSS
files.

The layout of the ``doc/source`` directory is reflected in the slug of the
online documentation. For example, the
``doc/source/contribute.rst`` renders as
``https://mechanical.docs.pyansys.com/version/stable/contribute.html``.

Thus, if you create a new file, it important to follow these rules:

- Use lowercase letters for file and directory names
- Use short and descriptive names
- Use hyphens to separate words
- Play smart with the hierarchy of the files and directories

All files need to be included in a table of contents. No dangling files are
permitted. If a file is not included in the table of contents, Sphinx raises a
warning that makes the build to fail.

A table of contents can be declared using a directive like this:

.. code-block:: rst

    .. toctree::
        :hidden:
        :maxdepth: 3

        path-to-file-A
        path-to-file-B
        path-to-file-C
        ...

The path to the file is relative to the directory where the table of contents
is declared.

.. _write-examples:

Write a new example
===================

The :ref:`Examples <ref_examples>` section of the documentation showcases different
capabilities of PyMechanical. Each example is a standalone Python script. Despite
being ``*.py`` files, they are written in a mix of `reStructuredText`_ and Python.

Documentarians writing new examples are encouraged to open a new Jupyter Lab
session and write the example as a Jupyter Notebook. This way, the
documentation can test the code and see the output in real-time. The created
Jupyter Notebook gets stored as a Python file automatically.

Finally, here are some tips for writing examples:

- Begin your PyMechanical example by briefly describing the feature or workflow being demonstrated.
  For instance, clarify if the example covers geometry creation, simulation setup, or result extraction.

- Next, clearly state the objective of the example.
  Define the problem, list all required parameters (such as geometry details, material properties,
  boundary conditions), and specify what the example will accomplish
  (e.g., running a modal analysis, extracting displacement results).

- For each code cell, precede it with a concise explanation. In Jupyter notebooks,
  use a markdown cell before each code cell to describe its purpose—such as importing modules,
  configuring the simulation, or visualizing results. This helps readers understand the context
  and reasoning behind each step.


.. _build-documentation:

Build the documentation
=======================

To build the documentation,  you need several dependencies installed.
These dependencies are listed in the ``pyproject.toml`` file under the
``[project.optional-dependencies]`` section. To install them, run:

.. code-block:: bash

    pip install -e .[doc]

For building documentation, you can run the usual rules provided in the
`Sphinx`_ ``make`` file:

.. tab-set::

    .. tab-item:: Linux / macOS

        .. code-block:: bash

            make -C doc clean
            make -C doc html
            your_browser_name doc/html/index.html

    .. tab-item:: Windows

        .. code-block:: text

            doc\make clean
            doc\make html
            start .\doc\_build\html\index.html

However, the recommended way of checking documentation integrity is to use
``tox``:

.. code:: bash

    tox -e doc && your_browser_name .tox/doc_out/index.html

Documentation building process involves building cheatsheets, which are generated using
quarto. If have quarto installed locally and want to build cheatsheets, then set the
environment variable ``BUILD_CHEATSHEET`` to ``true``.

