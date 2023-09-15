.. _ref_embedding_user_guide_libraries:

*********
Libraries
*********


.. note::

    This is an experimental feature. Some of these libraries will not work.

Most of Mechanical's scripting APIs are implemented in C#. However, there are a small number
of Python modules that are distributed with the installation of Mechanical that can be used
from within the Mechanical Scripting View. These modules are not available for use from an
embedded instance of Mechanical in python because Python does not know where to find those.

The function ``add_mechanical_python_libraries`` allows Python to find these libraries, and
some of them can be imported into Python. Note that this is only recommended after the embedded
instance of Mechanical is initialized, since some of these libraries expect the .NET Common
Language Runtime to have been initialized and for the appropriate C# libraries to have already
been loaded.

To use this function, run the following code:

.. code:: python


   from ansys.mechanical.core import App, global_variables
   from ansys.mechanical.core.embedding import add_mechanical_python_libraries

   app = App(version=232)

   add_mechanical_python_libraries(232)
   import materials  # This is materials.py that's shipped with Mechanical v232
