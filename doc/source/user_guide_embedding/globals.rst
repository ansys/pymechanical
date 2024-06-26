.. _ref_embedding_user_guide_globals:

Globals
=======

When using Mechanical scripting APIs (in either Mechanical's graphical user interface or when
sending scripts to a remote session of Mechanical), there are many global variables that are
by default usable from Python. Some of these are API entry points, like those discussed in
:ref:`ref_user_guide_scripting`, while others are types and namespaces that are used by the
scripting APIs. Examples of those are

* ``DataModel``
* ``Model``
* ``Tree``
* ``Graphics``
* ``Quantity``
* ``System``
* ``Ansys``
* ``Transaction`` : The class `Transaction()
  <../api/ansys/mechanical/core/embedding/imports/Transaction.html#ansys.mechanical.core.embedding.imports.Transaction>`_
  can be used to speed up a
  block of code that modifies multiple objects. This ensures that
  the tree is not refreshed and that only the bare minimum graphics and validations
  occur while the transaction is in scope. The class Transaction()
  should only be used around code blocks that do not require state updates,
  such as solving or meshing.
* ``MechanicalEnums``
* ``DataModelObjectCategory``
* ``Point``
* ``SectionPlane``
* ``Point2D``
* ``Point3D``
* ``Vector3D``

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
