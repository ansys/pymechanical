Initial Setup and Launching Mechanical Locally
----------------------------------------------
To run, ``ansys.mechanical.core`` needs to know the location of the Mechanical
binary.  Most of the time this can be automatically determined, but
non-standard installs will need to provide the location of Mechanical.
When running for the first time, ``ansys-mechanical-core`` will request the
location of the Mechanical executable if it cannot automatically find it.
You can test your installation of PyMechanical and set it up by running
the :func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>`:

.. code:: python

    from ansys.mechanical.core import launch_mechanical
    mechanical = launch_mechanical()

Python will automatically attempt to detect your Mechanical binary based on
environmental variables.  If it is unable to find a copy of Mechanical, you
will be prompted for the location of the Mechanical executable.  Here is a
sample input for Linux:

.. code::

    Enter location of Mechanical executable: /usr/ansys_inc/v231/aisol/.workbench

and for Windows:

.. code::

    Enter location of Mechanical executable: C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/AnsysWBU.exe

The settings file is stored locally and you will not not need to enter
the path again.  If you need to change the default ansys path
(i.e. changing the default version of Mechanical), run the following:

.. code:: python

    from ansys.mechanical import core as pymechanical
    new_path = 'C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/AnsysWBU.exe'
    pymechanical.change_default_mechanical_path(new_path)

Also see :func:`change_default_ansys_path() <ansys.mechanical.core.change_default_mechanical_path>` and
:func:`find_mechanical() <ansys.mechanical.core.find_mechanical>`.

Additionally, it is possible to specify the executable using the keyword argument ``exec_file``. 
In Linux:

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    mechanical = launch_mechanical(exec_file='/usr/ansys_inc/v231/aisol/.workbench')


And in Windows:

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    mechanical = launch_mechanical(exec_file='C:\\Program File\\ANSYS Inc\\v231\\aisol\\bin\\winx64\\AnsysWBU.exe')

You could also specify a custom executable by adding the correspondent flag (``-custom``) to the additional switches keyword argument.

.. code:: python

    from ansys.mechanical.core import launch_mechanical

    custom_exec = '/usr/ansys_inc/v231/aisol/.workbench'
    add_switch = f"-featureflags "mechanical.material.import;""
    mechanical = launch_mechanical(additional_switches=add_switch)



API Reference
~~~~~~~~~~~~~
For more details for controlling how Mechanical launches locally, see the
function description of :func:`launch_mechanical() <ansys.mechanical.core.launch_mechanical>`.
