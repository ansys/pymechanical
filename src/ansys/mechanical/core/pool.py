# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""This module is for threaded implementations of the Mechanical interface."""

import os
import time
import warnings

import ansys.platform.instancemanagement as pypim
from ansys.tools.path import version_from_path

from ansys.mechanical.core.errors import VersionError
from ansys.mechanical.core.mechanical import (
    _HAS_TQDM,
    LOG,
    MECHANICAL_DEFAULT_PORT,
    get_mechanical_path,
    launch_mechanical,
    port_in_use,
)
from ansys.mechanical.core.misc import threaded, threaded_daemon

if _HAS_TQDM:
    from tqdm import tqdm


def available_ports(n_ports, starting_port=MECHANICAL_DEFAULT_PORT):
    """Get a list of a given number of available ports starting from a specified port number.

    Parameters
    ----------
    n_ports : int
        Number of available ports to return.
    starting_port: int, option
        Number of the port to start the search from. The default is
        ``MECHANICAL_DEFAULT_PORT``.
    """
    port = starting_port
    ports = []
    while port < 65536 and len(ports) < n_ports:
        if not port_in_use(port):
            ports.append(port)
        port += 1

    if len(ports) < n_ports:
        raise RuntimeError(
            f"There are not {n_ports} available ports between {starting_port} and 65536."
        )

    return ports


class LocalMechanicalPool:
    """Create a pool of Mechanical instances.

    Parameters
    ----------
    n_instance : int
        Number of Mechanical instances to create in the pool.
    wait : bool, optional
        Whether to wait for the pool to be initialized. The default is
        ``True``. When ``False``, the pool starts in the background, in
        which case all resources might not be immediately available.
    starting_port : int, optional
        Starting port for the instances. The default is ``10000``.
    progress_bar : bool, optional
        Whether to show a progress bar when starting the pool. The default
        is ``True``, but the progress bar is not shown when ``wait=False``.
    restart_failed : bool, optional
        Whether to restart any failed instances in the pool. The default is
        ``True``.
    **kwargs : dict, optional
        Additional keyword arguments. For a list of all keyword
        arguments, use the :func:`ansys.mechanical.core.launch_mechanical`
        function. If the ``exec_file`` keyword argument is found, it is used to
        start instances. PyPIM is used to create instances if the following
        conditions are met:

        - PyPIM is configured.
        - ``version`` is specified.
        - ``exec_file`` is not specified.


    Examples
    --------
    Create a pool of 10 Mechanical instances.

    >>> from ansys.mechanical.core import LocalMechanicalPool
    >>> pool = LocalMechanicalPool(10)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    On Windows, create a pool while specifying the Mechanical executable file.

    >>> exec_file = 'C:/Program Files/ANSYS Inc/v242/aisol/bin/winx64/AnsysWBU.exe'
    >>> pool = LocalMechanicalPool(10, exec_file=exec_file)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    On Linux, create a pool while specifying the Mechanical executable file.

    >>> exec_file = '/ansys_inc/v242/aisol/.workbench'
    >>> pool = LocalMechanicalPool(10, exec_file=exec_file)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    In the PyPIM environment, create a pool.

    >>> pool = LocalMechanicalPool(10, version="242")
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    """

    def __init__(
        self,
        n_instances,
        wait=True,
        port=MECHANICAL_DEFAULT_PORT,
        progress_bar=True,
        restart_failed=True,
        **kwargs,
    ):
        """Initialize several Mechanical instances.

        Parameters
        ----------
        n_instance : int
            Number of Mechanical instances to initialize.
        wait : bool, optional
            Whether to wait for the instances to be initialized. The default is
            ``True``. When ``False``, the instances start in the background, in
            which case all resources might not be immediately available.
        port : int, optional
            Port for the first Mechanical instance. The default is
            ``MECHANICAL_DEFAULT_PORT``.
        progress_bar : bool, optional
            Whether to display a progress bar when starting the instances. The default
            is ``True``, but the progress bar is not shown when ``wait=False``.
        restart_failed : bool, optional
            Whether to restart any failed instances. The default is ``True``.
        **kwargs : dict, optional
            Additional keyword arguments. For a list of all additional keyword
            arguments, see the :func:`ansys.mechanical.core.launch_mechanical`
            function. If the ``exec_file`` keyword argument is found, it is used to
            start instances. Instances are created using PyPIM if the following
            conditions are met:

            - PyPIM is configured.
            - Version is specified/
            - ``exec_file`` is not specified.
        """
        self._instances = []
        self._spawn_kwargs = kwargs
        self._remote = False

        # verify that mechanical is 2023R2 or newer
        exec_file = None
        if "exec_file" in kwargs:
            exec_file = kwargs["exec_file"]
        else:
            if pypim.is_configured():  # pragma: no cover
                if "version" in kwargs:
                    version = kwargs["version"]
                    self._remote = True
                else:
                    raise "Pypim is configured. But version is not passed."
            else:  # get default executable
                exec_file = get_mechanical_path()
                if exec_file is None:  # pragma: no cover
                    raise FileNotFoundError(
                        "Path to Mechanical executable file is invalid or cache cannot be loaded. "
                        "Enter a path manually by specifying a value for the "
                        "'exec_file' parameter."
                    )

        if not self._remote:  # pragma: no cover
            if version_from_path("mechanical", exec_file) < 232:
                raise VersionError("A local Mechanical pool requires Mechanical 2023 R2 or later.")

        ports = None

        if not self._remote:
            # grab available ports
            ports = available_ports(n_instances, port)

        self._instances = []
        self._active = True  # used by pool monitor

        n_instances = int(n_instances)
        if n_instances < 2:
            raise ValueError("You must request at least two instances to create a pool.")

        pbar = None
        if wait and progress_bar:
            if not _HAS_TQDM:  # pragma: no cover
                raise ModuleNotFoundError(
                    f"To use the keyword argument 'progress_bar', you must have installed "
                    f"the 'tqdm' package. To avoid this message, you can set 'progress_bar=False'."
                )

            pbar = tqdm(total=n_instances, desc="Creating Pool")

        # initialize a list of dummy instances
        self._instances = [None for _ in range(n_instances)]

        if self._remote:  # pragma: no cover
            threads = [
                self._spawn_mechanical_remote(i, pbar, name=f"Instance {i}")
                for i in range(n_instances)
            ]
        else:
            # threaded spawn
            threads = [
                self._spawn_mechanical(i, ports[i], pbar, name=f"Instance {i}")
                for i in range(n_instances)
            ]
        if wait:
            [thread.join() for thread in threads]

            # check if all clients connected have connected
            if len(self) != n_instances:  # pragma: no cover
                n_connected = len(self)
                warnings.warn(
                    f"Only {n_connected} clients connected out of {n_instances} requested"
                )
            if pbar is not None:
                pbar.close()

        # monitor pool if requested
        if restart_failed:
            self._pool_monitor_thread = self._monitor_pool(name="Monitoring_Thread started")

        if not self._remote:
            self._verify_unique_ports()

    def _verify_unique_ports(self):
        if self._remote:  # pragma: no cover
            raise RuntimeError("PyPIM is used. Port information is not available.")

        if len(self.ports) != len(self):  # pragma: no cover
            raise RuntimeError("Mechanical pool has overlapping ports.")

    def map(
        self,
        func,
        iterable=None,
        clear_at_start=True,
        progress_bar=True,
        close_when_finished=False,
        timeout=None,
        wait=True,
    ):
        """Run a user-defined function on each Mechanical instance in the pool.

        Parameters
        ----------
        func : function
            Function with ``mechanical`` as the first argument. The subsequent
            arguments should match the number of items in each iterable (if any).
        iterable : list, tuple, optional
            An iterable containing a set of arguments for the function.
            The default is ``None``, in which case the function runs
            once on each instance of Mechanical.
        clear_at_start : bool, optional
            Clear Mechanical at the start of execution. The default is
            ``True``. Setting this to ``False`` might lead to instability.
        progress_bar : bool, optional
            Whether to show a progress bar when running the batch of input
            files. The default is ``True``, but the progress bar is not shown
            when ``wait=False``.
        close_when_finished : bool, optional
            Whether to close the instances when the function finishes running
            on all instances in the pool. The default is ``False``.
        timeout : float, optional
            Maximum runtime in seconds for each iteration. The default is
            ``None``, in which case there is no timeout. If you specify a
            value, each iteration is allowed to run only this number of
            seconds. Once this value is exceeded, the batch process is
            stopped and treated as a failure.
        wait : bool, optional
            Whether block execution must wait until the batch process is
            complete. The default is ``True``.

        Returns
        -------
        list
            A list containing the return values for the function.
            Failed runs do not return an output. Because return values
            are not necessarily in the same order as the iterable,
            you might want to add some sort of tracker to the return
            of your function.

        Examples
        --------
        Run several input files while storing the final routine.  Note
        how the function to map must use ``mechanical`` as the first argument.
        The function can have any number of additional arguments.

        >>> from ansys.mechanical.core import LocalMechanicalPool
        >>> pool = LocalMechanicalPool(10)
        >>> completed_indices = []
        >>> def function(mechanical, name, script):
                # name, script = args
                mechanical.clear()
                output = mechanical.run_python_script(script)
                return name, output
        >>> inputs = [("first","2+3"), ("second", "3+4")]
        >>> output = pool.map(function, inputs, progress_bar=False, wait=True)
        [('first', '5'), ('second', '7')]
        """
        # check if any instances are available
        if not len(self):  # pragma: no cover
            # instances could still be spawning...
            if not all(v is None for v in self._instances):
                raise RuntimeError("No Mechanical instances available.")

        results = []

        if iterable is not None:
            jobs_count = len(iterable)
        else:
            jobs_count = len(self)

        pbar = None
        if progress_bar:
            if not _HAS_TQDM:  # pragma: no cover
                raise ModuleNotFoundError(
                    f"To use the keyword argument 'progress_bar', you must have installed "
                    f"the 'tqdm' package. To avoid this message, you can set 'progress_bar=False'."
                )

            pbar = tqdm(total=jobs_count, desc="Mechanical Running")

        @threaded_daemon
        def func_wrapper(obj, func, clear_at_start, timeout, args=None, name=""):
            """Expect obj to be an instance of Mechanical."""
            LOG.debug(name)
            complete = [False]

            @threaded_daemon
            def run(name_local=""):
                LOG.debug(name_local)

                if clear_at_start:
                    obj.clear()

                if args is not None:
                    if isinstance(args, (tuple, list)):
                        results.append(func(obj, *args))
                    else:
                        results.append(func(obj, args))
                else:
                    results.append(func(obj))

                complete[0] = True

            run_thread = run(name_local=name)

            if timeout:  # pragma: no cover
                time_start = time.time()
                while not complete[0]:
                    time.sleep(0.01)
                    if (time.time() - time_start) > timeout:
                        break

                if not complete[0]:
                    LOG.error(f"Stopped instance due to a timeout of {timeout} seconds.")
                    obj.exit()
            else:
                run_thread.join()
                if not complete[0]:  # pragma: no cover
                    LOG.error(f"Stopped instance because running failed.")
                    try:
                        obj.exit()
                    except:
                        pass

            obj.locked = False
            if pbar:
                pbar.update(1)

        threads = []
        if iterable is not None:
            for args in iterable:
                # grab the next available instance of mechanical
                instance, i = self.next_available(return_index=True)
                instance.locked = True

                threads.append(
                    func_wrapper(
                        instance, func, clear_at_start, timeout, args, name=f"Map_Thread{i}"
                    )
                )
        else:  # simply apply to all
            for instance in self._instances:
                if instance:
                    threads.append(
                        func_wrapper(instance, func, clear_at_start, timeout, name=f"Map_Thread")
                    )

        if close_when_finished:  # pragma: no cover
            # start closing any instances that are not in execution
            while not all(v is None for v in self._instances):
                # grab the next available instance of mechanical and close it
                instance, i = self.next_available(return_index=True)
                self._instances[i] = None

                try:
                    instance.exit()
                except Exception as error:  # pragma: no cover
                    LOG.error(f"Failed to close instance : str{error}.")
        else:
            # wait for all threads to complete
            if wait:
                [thread.join() for thread in threads]

        return results

    def run_batch(
        self,
        files,
        clear_at_start=True,
        progress_bar=True,
        close_when_finished=False,
        timeout=None,
        wait=True,
    ):
        """Run a batch of input files on the Mechanical instances in the pool.

        Parameters
        ----------
        files : list
            List of input files.
        clear_at_start : bool, optional
            Whether to clear Mechanical when execution starts. The default is
            ``True``. Setting this parameter to ``False`` might lead to
            instability.
        progress_bar : bool, optional
            Whether to show a progress bar when running the batch of input
            files. The default is ``True``, but the progress bar is not shown
            when ``wait=False``.
        close_when_finished : bool, optional
            Whether to close the instances when running the batch
            of input files is finished. The default is ``False``.
        timeout : float, optional
            Maximum runtime in seconds for each iteration. The default is
            ``None``, in which case there is no timeout. If you specify a
            value, each iteration is allowed to run only this number of
            seconds. Once this value is exceeded, the batch process is stopped
            and treated as a failure.
        wait : bool, optional
            Whether block execution must wait until the batch process is complete.
            The default is ``True``.

        Returns
        -------
        list
            List of text outputs from Mechanical for each batch run. The outputs
            are not necessarily listed in the order of the inputs. Failed runs do
            not return an output. Because the return outputs are not
            necessarily in the same order as ``iterable``, you might
            want to add some sort of tracker or note within the input files.

        Examples
        --------
        Run 20 verification files on the pool.

        >>> files = [f"test{index}.py" for index in range(1, 21)]
        >>> outputs = pool.run_batch(files)
        >>> len(outputs)
        20
        """
        # check all files exist before running
        for filename in files:
            if not os.path.isfile(filename):
                raise FileNotFoundError("Unable to locate file %s" % filename)

        def run_file(mechanical, input_file):
            if clear_at_start:
                mechanical.clear()
            return mechanical.run_python_script_from_file(input_file)

        return self.map(
            run_file,
            files,
            progress_bar=progress_bar,
            close_when_finished=close_when_finished,
            timeout=timeout,
            wait=wait,
        )

    def next_available(self, return_index=False):
        """Wait until a Mechanical instance is available and return this instance.

        Parameters
        ----------
        return_index : bool, optional
            Whether to return the index along with the instance. The default
            is ``False``.

        Returns
        -------
        pymechanical.Mechanical
            Instance of Mechanical.

        int
            Index within the pool of Mechanical instances. This index
            is not returned by default.

        Examples
        --------
        >>> mechanical = pool.next_available()
        >>> mechanical
        Ansys Mechanical [Ansys Mechanical Enterprise]
        Product Version:242
        Software build date: 06/03/2024 14:47:58
        """
        # loop until the next instance is available
        while True:
            for i, instance in enumerate(self._instances):
                # if encounter placeholder
                if not instance:  # pragma: no cover
                    continue

                if not instance.locked and not instance._exited:
                    # any instance that is not running or exited
                    # should be available
                    if not instance.busy:
                        # double check that this instance is alive:
                        try:
                            instance._make_dummy_call()
                        except:  # pragma: no cover
                            instance.exit()
                            continue

                        if return_index:
                            return instance, i
                        else:
                            return instance
                    # review - not needed
                    # else:
                    #     instance._exited = True

    def __del__(self):
        """Clean up when complete."""
        print("pool:Automatic clean up.")
        self.exit()

    def exit(self, block=False):
        """Exit all Mechanical instances in the pool.

        Parameters
        ----------
        block : bool, optional
            Whether to wait until all processes close before exiting
            all instances in the pool. The default is ``False``.

        Examples
        --------
        >>> pool.exit()
        """
        self._active = False  # Stops any active instance restart

        @threaded
        def threaded_exit(index, instance_local):
            if instance_local:
                try:
                    instance_local.exit()
                except:  # pragma: no cover
                    pass
                self._instances[index] = None
                LOG.debug(f"Exited instance: {str(instance_local)}")

        threads = []
        for i, instance in enumerate(self):
            threads.append(threaded_exit(i, instance))

        if block:
            [thread.join() for thread in threads]

    def __len__(self):
        """Get the number of instances in the pool."""
        count = 0
        for instance in self._instances:
            if instance:
                if not instance._exited:
                    count += 1
        return count

    def __getitem__(self, key):
        """Get an instance by an index."""
        return self._instances[key]

    def __iter__(self):
        """Iterate through active instances."""
        for instance in self._instances:
            if instance:
                yield instance

    @threaded_daemon
    def _spawn_mechanical(self, index, port=None, pbar=None, name=""):
        """Spawn a Mechanical instance at an index.

        Parameters
        ----------
        index : int
            Index to spawn the instance on.
        port : int, optional
            Port for the instance. The default is ``None``.
        pbar :
            The default is ``None``.
        name : str, optional
            Name for the instance. The default is ``""``.
        """
        LOG.debug(name)
        self._instances[index] = launch_mechanical(port=port, **self._spawn_kwargs)
        # LOG.debug("Spawned instance %d. Name '%s'", index, name)
        if pbar is not None:
            pbar.update(1)

    @threaded_daemon
    def _spawn_mechanical_remote(self, index, pbar=None, name=""):  # pragma: no cover
        """Spawn a Mechanical instance at an index.

        Parameters
        ----------
        index : int
            Index to spawn the instance on.
        pbar :
            The default is ``None``.
        name : str, optional
            Name for the instance. The default is ``""``.

        """
        LOG.debug(name)
        self._instances[index] = launch_mechanical(**self._spawn_kwargs)
        # LOG.debug("Spawned instance %d. Name '%s'", index, name)
        if pbar is not None:
            pbar.update(1)

    @threaded_daemon
    def _monitor_pool(self, refresh=1.0, name=""):
        """Check for instances within a pool that have exited (failed) and restart them.

        Parameters
        ----------
        refresh : float, optional
            The default is ``1.0``.
        name : str, optional
            Name for the instance. The default is ``""``.
        """
        LOG.debug(name)
        while self._active:
            for index, instance in enumerate(self._instances):
                # encountered placeholder
                if not instance:  # pragma: no cover
                    continue
                if instance._exited:  # pragma: no cover
                    try:
                        if self._remote:
                            LOG.debug(
                                f"Restarting a Mechanical remote instance for index : {index}."
                            )
                            self._spawn_mechanical_remote(index, name=f"Instance {index}").join()
                        else:
                            # use the next port after the current available port
                            port = max(self.ports) + 1
                            LOG.debug(
                                f"Restarting a Mechanical instance for index : "
                                f"{index} on port: {port}."
                            )
                            self._spawn_mechanical(
                                index, port=port, name=f"Instance {index}"
                            ).join()
                    except Exception as e:
                        LOG.error(e, exc_info=True)
            time.sleep(refresh)

    @property
    def ports(self):
        """Get a list of the ports that are used.

        Examples
        --------
        Get the list of ports used by the pool of Mechanical instances.

        >>> pool.ports
        [10001, 10002]

        """
        return [inst._port for inst in self if inst is not None]

    def __str__(self):
        """Get the string representation of this object."""
        return "Mechanical pool with %d active instances" % len(self)
