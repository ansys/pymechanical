.. _ref_user_guide_embedding:

=======================
Embedded instance guide
=======================
This section provides an overview of how you use PyMechanical to embed
an instance of Mechanical in Python.


..
   This toctreemust be a top-level index to get it to show up in
   pydata_sphinx_theme.

.. toctree::
   :maxdepth: 1
   :hidden:

   configuration
   globals


Overview
========
The :class:`Application <ansys.mechanical.core.embedding.Application>` class provides
a Mechanical instance.

.. code:: python

    from ansys.mechanical.core import Application
    app = Application()
    ns = app.DataModel.Project.Model.AddNamedSelection()

The `Application` class has access to the global scripting entry points that are available
from built-in Mechanical scripting. These are:

* ExtAPI: ``Application.ExtAPI``
* DataModel: ``Application.DataModel``
* Model: ``Application.DataModel.Project.Model``
* Tree: ``Application.DataModel.Tree``
* Graphics: ``Application.ExtAPI.Graphics``

Besides the scripting entry points, many other types and objects are available from
built-in Mechanical scripting. To learn how to import the scripting entry points,
namespaces, and types, see :ref:`ref_embedding_user_guide_globals`.

Additional configuration
------------------------
By default, an instance of :class:`Application <ansys.mechanical.core.embedding.Application>`
is configured in the same way as the Mechanical application. To customize this, see
:ref:`ref_embedding_user_guide_configuration`.
