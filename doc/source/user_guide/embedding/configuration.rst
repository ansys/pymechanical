.. _ref_embedding_user_guide_addin_configuration:

Addin configuration
===================

There are some configuration options that are respected when loading an embedded instance
of Mechanical into Python.
The :class:`~ansys.mechanical.core.embedding.addins.AddinConfiguration` class can be
used to set up addin configuration. This configuration can be supplied to the constructor
of the :class:`~ansys.mechanical.core.embedding.app.App` class.

For example, to load an instance of Mechanical using the "Mechanical" configuration name and
without loading any ACT Addins:

.. code:: python

    from ansys.mechanical.core import App
    from ansys.mechanical.core.embedding import AddinConfiguration

    config = AddinConfiguration("Mechanical", no_act_addins=True)
    app = App(config=config)
