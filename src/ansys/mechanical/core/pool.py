"""This module is for threaded implementations of the mechanical interface."""

import os
import time
import warnings

import ansys.platform.instancemanagement as pypim

from ansys.mechanical.core.errors import VersionError
from ansys.mechanical.core.mechanical import (
    _HAS_TQDM,
    LOG,
    MECHANICAL_DEFAULT_PORT,
    _version_from_path,
    get_mechanical_path,
    launch_mechanical,
    port_in_use,
)
from ansys.mechanical.core.misc import threaded, threaded_daemon

if _HAS_TQDM:
    from tqdm import tqdm


def available_ports(n_ports, starting_port=MECHANICAL_DEFAULT_PORT):
    """Return a list the first ``n_ports`` ports starting from ``starting_port``."""
    port = MECHANICAL_DEFAULT_PORT
    ports = []
    while port < 65536 and len(ports) < n_ports:
        if not port_in_use(port):
            ports.append(port)
        port += 1

    if len(ports) < n_ports:
        raise RuntimeError(
            f"There are not {n_ports} available ports between {starting_port} and 65536"
        )

    return ports


class LocalMechanicalPool:
    """Create a pool of Mechanical instances.

    .. note::
       Requires Mechanical 2023 R1 or later.

    Parameters
    ----------
    n_instance : int
        Number of instances to create.

    wait : bool, optional
        Wait for pool to be initialized.  Otherwise, pool will start
        in the background and all resources may not be available instantly.

    starting_port : int, optional
        Starting port for the Mechanical instances.  Defaults to 10000.

    progress_bar : bool, optional
        Show a progress bar when starting the pool.  Defaults to
        ``True``.  Will not be shown when ``wait=False``.

    restart_failed : bool, optional
        Restarts any failed instances in the pool.

    **kwargs : dict, optional
        See :func:`ansys.mechanical.core.launch_mechanical` for a complete
        listing of all additional keyword arguments. If exec_file is found, it will be used to
        start instances. If PyPIM is configured, version is specified and
        exec_file is not specified, instances are created using PyPIM.

    Examples
    --------
    Simply create a pool of 10 instances to run

    >>> from ansys.mechanical.core import LocalMechanicalPool
    >>> pool = LocalMechanicalPool(10)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    Create a pool while specifying the Mechanical executable in Windows.

    >>> exec_file = 'C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/AnsysWBU.exe'
    >>> pool = LocalMechanicalPool(10, exec_file=exec_file)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    Create a pool while specifying the Mechanical executable in Linux.

    >>> exec_file = '/ansys_inc/v231/aisol/.workbench'
    >>> pool = LocalMechanicalPool(10, exec_file=exec_file)
    Creating Pool: 100%|########| 10/10 [00:01<00:00,  1.43it/s]

    Create a pool in the PyPIM environment

    >>> pool = LocalMechanicalPool(10, version="231")
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
        """Initialize several instances of mechanical."""
        self._instances = []
        self._spawn_kwargs = kwargs
        self._remote = False

        # verify that mechanical is 2023R1 or newer
        exec_file = None
        if "exec_file" in kwargs:
            exec_file = kwargs["exec_file"]
        else:  # get default executable
            if pypim.is_configured():
                if "version" in kwargs:
                    version = kwargs["version"]
                    self._remote = True
                else:
                    raise "Pypim is configured. But version is not passed."
            else:
                exec_file = get_mechanical_path()
                if exec_file is None:
                    raise FileNotFoundError(
                        "Invalid exec_file path or cannot load cached "
                        "Mechanical path.  Enter one manually using "
                        "exec_file=<path to executable>"
                    )

        if not self._remote:
            if _version_from_path(exec_file) < 231:
                raise VersionError("LocalMechanicalPool requires Mechanical 2023R1 or later.")

        ports = None

        if not self._remote:
            # grab available ports
            ports = available_ports(n_instances, port)

        self._instances = []
        self._active = True  # used by pool monitor

        n_instances = int(n_instances)
        if n_instances < 2:
            raise ValueError("Must request at least 2 instances to create a pool.")

        pbar = None
        if wait and progress_bar:
            if not _HAS_TQDM:  # pragma: no cover
                raise ModuleNotFoundError(
                    f"To use the keyword argument 'progress_bar', you need to have installed "
                    f"the 'tqdm' package. To avoid this message you can set 'progress_bar=False'."
                )

            pbar = tqdm(total=n_instances, desc="Creating Pool")

        # initialize a list of dummy instances
        self._instances = [None for _ in range(n_instances)]

        if self._remote:
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
            if len(self) != n_instances:
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
        if self._remote:
            raise RuntimeError("PyPim is used. Ports information is not available.")

        if len(self._ports) != len(self):
            raise RuntimeError("MechanicalPool has overlapping ports")

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
        """Run a function for each instance of mechanical within the pool.

        Parameters
        ----------
        func : function
            User function with an instance of ``mechanical`` as the first
            argument.  The remaining arguments should match the number
            of items in each iterable (if any).

        iterable : list, tuple, optional
            An iterable containing a set of arguments for ``func``.
            If None, will run ``func`` once for each instance of
            mechanical.

        clear_at_start : bool, optional
            Clear Mechanical at the start of execution.  By default this is
            ``True``, and setting this to ``False`` may lead to
            instability.

        progress_bar : bool, optional
            Show a progress bar when running the batch.  Defaults to
            ``True``.

        close_when_finished : bool, optional
            Exit the Mechanical instances when the pool is finished.
            Default ``False``.

        timeout : float, optional
            Maximum runtime in seconds for each iteration.  If
            ``None``, no timeout.  If specified, each iteration will
            be only allowed to run ``timeout`` seconds, and then
            killed and treated as a failure.

        wait : bool, optional
            Block execution until the batch is complete.  Default
            ``True``.

        Returns
        -------
        list
            A list containing the return values for ``func``.  Failed
            runs will not return an output.  Since the returns are not
            necessarily in the same order as ``iterable``, you may
            want to add some sort of tracker to the return of your
            user function``func``.

        Examples
        --------
        Run several input files while storing the final routine.  Note
        how the user function to be mapped must use ``mechanical`` as the
        first argument.  The function can have any number of
        additional arguments.

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
        if not len(self):
            # instances could still be spawning...
            if not all(v is None for v in self._instances):
                raise RuntimeError("No Mechanical instances available.")

        results = []

        if iterable is not None:
            n = len(iterable)
        else:
            n = len(self)

        pbar = None
        if progress_bar:
            if not _HAS_TQDM:  # pragma: no cover
                raise ModuleNotFoundError(
                    f"To use the keyword argument 'progress_bar', you need to have installed "
                    f"the 'tqdm' package. To avoid this message you can set 'progress_bar=False'."
                )

            pbar = tqdm(total=n, desc="Mechanical Running")

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

            if timeout:
                time_start = time.time()
                while not complete[0]:
                    time.sleep(0.01)
                    if (time.time() - time_start) > timeout:
                        break

                if not complete[0]:
                    LOG.error(f"Killed instance due to timeout of {timeout} seconds")
                    obj.exit()
            else:
                run_thread.join()
                if not complete[0]:
                    LOG.error(f"Killed instance due to run failed.")
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

        if close_when_finished:
            # start closing any instances that are not in execution
            while not all(v is None for v in self._instances):
                # grab the next available instance of mechanical and close it
                instance, i = self.next_available(return_index=True)
                self._instances[i] = None

                try:
                    instance.exit()
                except Exception as error:
                    LOG.error(f"Failed to close instance : str{error}")
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
        """Run a batch of input files on the pool.

        Parameters
        ----------
        files : list
            List of input files to run.

        clear_at_start : bool, optional
            Clear Mechanical at the start of execution.  By default this is
            ``True``, and setting this to ``False`` may lead to
            instability.

        progress_bar : bool, optional
            Show a progress bar when starting the pool.  Defaults to
            ``True``.  Will not be shown when ``wait=False``

        progress_bar : bool, optional
            Show a progress bar when running the batch.  Defaults to
            ``True``.

        close_when_finished : bool, optional
            Exit the Mechanical instances when the pool is finished.
            Default ``False``.

        timeout : float, optional
            Maximum runtime in seconds for each iteration.  If
            ``None``, no timeout.  If specified, each iteration will
            be only allowed to run ``timeout`` seconds, and then
            killed and treated as a failure.

        wait : bool, optional
            Block execution until the batch is complete.  Default
            ``True``.

        Returns
        -------
        list
            List of text outputs from Mechanical for each batch run.  Not
            necessarily in the order of the inputs. Failed runs will
            not return an output.  Since the returns are not
            necessarily in the same order as ``iterable``, you may
            want to add some sort of tracker or note within the input files.

        Examples
        --------
        Run 20 verification files on the pool

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
        """Wait until an instance of mechanical is available and return that instance.

        Parameters
        ----------
        return_index : bool, optional
            Return the index along with the instance.  Default ``False``.

        Returns
        -------
        pymechanical.Mechanical
            Instance of Mechanical.

        int
            Index within the pool of the instance of Mechanical.  By
            default this is not returned.

        Examples
        --------
        >>> mechanical = pool.next_available()
        >>> print(mechanical)
        Ansys Mechanical [Ansys Mechanical Enterprise]
        Product Version:231
        Software build date:Wed Jul 13 14:29:54 2022
        """
        # loop until the next instance is available
        while True:
            for i, instance in enumerate(self._instances):
                if not instance:  # if encounter placeholder
                    continue

                if not instance.locked and not instance._exited:
                    # any instance that is not running or exited
                    # should be available
                    if not instance.busy:
                        # double check that this instance is alive:
                        try:
                            instance._make_dummy_call()
                        except:
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
        self.exit()

    def exit(self, block=False):
        """Close out all instances in the pool.

        Parameters
        ----------
        block : bool, optional
            When ``True``, wait until all processes are closed.

        Examples
        --------
        >>> pool.exit()
        """
        self._active = False  # kills any active instance restart

        @threaded
        def threaded_exit(index, instance_local):
            if instance_local:
                try:
                    instance_local.exit()
                except:
                    pass
                self._instances[index] = None
                LOG.debug(f"Exited instance: {str(instance_local)}")

        threads = []
        for i, instance in enumerate(self):
            threads.append(threaded_exit(i, instance))

        if block:
            [thread.join() for thread in threads]

    def __len__(self):
        """Return the number of instances inc the pool."""
        count = 0
        for instance in self._instances:
            if instance:
                if not instance._exited:
                    count += 1
        return count

    def __getitem__(self, key):
        """Return an instance by an index."""
        return self._instances[key]

    def __iter__(self):
        """Iterate through active instances."""
        for instance in self._instances:
            if instance:
                yield instance

    @threaded_daemon
    def _spawn_mechanical(self, index, port=None, pbar=None, name=""):
        """Spawn a mechanical instance at an index."""
        LOG.debug(name)
        self._instances[index] = launch_mechanical(port=port, **self._spawn_kwargs)
        # LOG.debug("Spawned instance %d. Name '%s'", index, name)
        if pbar is not None:
            pbar.update(1)

    @threaded_daemon
    def _spawn_mechanical_remote(self, index, pbar=None, name=""):
        """Spawn a mechanical instance at an index."""
        LOG.debug(name)
        self._instances[index] = launch_mechanical(**self._spawn_kwargs)
        # LOG.debug("Spawned instance %d. Name '%s'", index, name)
        if pbar is not None:
            pbar.update(1)

    @threaded_daemon
    def _monitor_pool(self, refresh=1.0, name=""):
        """Check if instances within a pool have exited (failed) and restarts them."""
        LOG.debug(name)
        while self._active:
            for index, instance in enumerate(self._instances):
                if not instance:  # encountered placeholder
                    continue
                if instance._exited:
                    try:
                        if self._remote:
                            LOG.debug(
                                f"restarting a mechanical remote instance for the index : {index}"
                            )
                            self._spawn_mechanical_remote(index, name=f"Instance {index}").join()
                        else:
                            # use the next port after the current available port
                            port = max(self._ports) + 1
                            LOG.debug(
                                f"restarting a mechanical instance for the index : "
                                f"{index} port: {port}"
                            )
                            self._spawn_mechanical(
                                index, port=port, name=f"Instance {index}"
                            ).join()
                    except Exception as e:
                        LOG.error(e, exc_info=True)
            time.sleep(refresh)

    @property
    def _ports(self):
        """Return the list of ports used."""
        return [inst._port for inst in self if inst is not None]

    def __str__(self):
        """Return string representation of this object."""
        return "Mechanical Pool with %d active instances" % len(self)
