Create a pool of Mechanical instances
=====================================
PyMechanical contains the :class:`MechanicalLocalPool <ansys.mechanical.core.MechanicalLocalPool>`
class to simplify creating multiple local instances of the :class:`Mechanical <ansys.mechanical.core.mechanical.Mechanical>`
class for batch processing. This can be used for the batch processing of a
set of input files or other batch-related processes.

To create the pool:

.. code:: python

    >>> from ansys.mechanical.core import LocalMechanicalPool
    >>> pool = LocalMechanicalPool(10, version="231")
    'Mechanical Pool with 10 active instances'

You can also supply additional keyword arguments when creating the
pool. For instance, to restart failed instances.

.. code:: python

    >>> import os
    >>> my_path = os.getcmd()
    >>> pool = LocalMechanicalPool(10, version="231", restart_failed=True)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

Each individual instance of mechanical can be accessed with:

.. code:: python

    >>> pool[0]
    <ansys.mechanical.core.mechanical.Mechanical at 0x7fabf0230d90>

Note that this is a self healing pool. If an instance of Mechanical dies
during a batch process, this instance is automatically restarted.
When creating the pool, you can disable this behavior by setting ``restart_failed=False``.


Run a set of input files
~~~~~~~~~~~~~~~~~~~~~~~~
You can use the pool to run a set of pre-generated input files using
:func:`run_batch <ansys.mechanical.core.MechanicalLocalPool.run_batch>`.  For
example, you can run the first set of 20 verification files with:

.. code:: python

     >>>>>> from ansys.mechanical.core import examples
     >>> files = [f"test{index}.py" for index in range(1, 21)]
     >>> outputs = pool.run_batch(files)
     >>> len(outputs)
     20

Run a user-defined function
~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can also use the pool to run a custom user-defined function on each
instance of Mechanical over a set of inputs. This example again uses set
of verification files as in the :func:`run_batch
<ansys.mechanical.core.MechanicalLocalPool.run_batch>` example, but implements
it as a function and outputs the final routine instead of the text
output from Mechanical.

.. code:: python

    >>> completed_indices = []
    >>> def func(mechanical, input_file, index):
            # input_file, index = args
            mechanical.clear()
            output = mechanical.run_python_script_from_file(input_file)
            completed_indices.append(index)
            return output
    >>> inputs = [('test{index}.py', i) for i in range(1, 10)]
    >>> output = pool.map(func, inputs, progress_bar=True, wait=True)
    ['result1',
     'result2',
     'result3',
     'result4',
     'result5',
     'result6',
     'result7',
     'result8',
     'result9']


API reference
~~~~~~~~~~~~~
For more information, see :ref:`ref_pool_api`.
