Initial setup and launching Mechanical locally
----------------------------------------------
To run, the ``ansys-mechanical-core`` package must know the location
of the Mechanical binary. Most of the time, this can be automatically
determined. However, for a non-standard installation, you must provide
the location of Mechanical.

When running for the first time, the ``ansys-mechanical-core`` package
requests the location of the Mechanical executable if it cannot find it
automatically. You can test your installation of PyMechanical and set it
up by running the :func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>`
method:

.. code:: python

    from ansys.mechanical.core import launch_mechanical
    mechanical = launch_mechanical()

Python automatically attempts to detect your Mechanical binary based on
environmental variables. If it is unable to find an installation of Mechanical,
you are prompted for the location of the Mechanical executable.

Here is a sample input for Linux:

.. code::

    Enter location of Mechanical executable: /usr/ansys_inc/v231/aisol/.workbench

Here is a sample input for Windows:

.. code::

    Enter location of Mechanical executable: C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/AnsysWBU.exe

The settings file is stored locally. You do not need to enter
the path again. If you must change the default Ansys path,
(for example, change the default version of Mechanical), run the following:

.. code:: python

    from ansys.mechanical import core as pymechanical
    new_path = 'C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/AnsysWBU.exe'
    pymechanical.change_default_mechanical_path(new_path)

Also see :func:`change_default_ansys_path() <ansys.mechanical.core.change_default_mechanical_path>` and
:func:`find_mechanical() <ansys.mechanical.core.find_mechanical>`.

Additionally, it is possible to specify the executable using the ``exec_file`` keyword argument. 


**On Linux*

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    mechanical = launch_mechanical(exec_file='/usr/ansys_inc/v231/aisol/.workbench')


**On Windows**

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    mechanical = launch_mechanical(exec_file='C:\\Program File\\ANSYS Inc\\v231\\aisol\\bin\\winx64\\AnsysWBU.exe')

You can also specify a custom executable by adding the correspondent flag (``-custom``) to the additional switches keyword argument.

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    custom_exec = '/usr/ansys_inc/v231/aisol/.workbench'
    add_switch = f"-featureflags "mechanical.material.import;""
    mechanical = launch_mechanical(additional_switches=add_switch)



API reference
~~~~~~~~~~~~~
For more information on controlling how Mechanical launches locally, see the description
of the :func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>` method.
