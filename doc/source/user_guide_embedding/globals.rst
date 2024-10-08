.. _ref_embedding_user_guide_globals:

Add global variables
====================

When using Mechanical scripting APIs (in either Mechanical's graphical user interface or when
sending scripts to a remote session of Mechanical), there are many global variables that are
by default usable from Python. Some of these are API entry points, like those discussed in
:ref:`ref_user_guide_scripting`, while others are types and namespaces that are used by the
scripting APIs. Examples of those are the ``Quantity``, ``Transaction`` class or the ``DataModel`` entry point.

Embedding Mechanical into Python is as simple as constructing an application object. This can
not automatically change the global variables available to the Python scope that constructed
it. As a utility, a function that adds the API entry points is available. To use it, run the
following code:

.. code:: python

   from ansys.mechanical.core import App

   app = App()
   # The following line extracts the global API entry points and merges them into your global
   # Python global variables.
   app.update_globals(globals())

Some enum types are available when scripting inside of mechanical, such as ``SelectionTypeEnum``
or ``LoadDefineBy``. Because these number in the thousands, by default, these enums are
included in these global variables. To avoid including them, set the second argument of
``update_globals`` to False.

.. code:: python

   app.update_globals(globals(), False)
