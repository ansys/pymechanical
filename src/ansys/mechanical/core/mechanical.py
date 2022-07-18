"""Connect to Mechanical grpc server and issues commands."""
from contextlib import closing
import datetime
from functools import wraps
from glob import glob
import os
import re
import socket
import threading
import time
import warnings
import weakref

import ansys.platform.instancemanagement as pypim
import appdirs
import grpc

import ansys.mechanical.core
from ansys.mechanical.core import LOG
from ansys.mechanical.core.errors import MechanicalExitedError, MechanicalRuntimeError, VersionError
from ansys.mechanical.core.launcher import MechanicalLauncher
import ansys.mechanical.core.mechanical_pb2 as mechanical_pb2
import ansys.mechanical.core.mechanical_pb2_grpc as mechanical_pb2_grpc
from ansys.mechanical.core.misc import (
    check_valid_ip,
    check_valid_port,
    check_valid_start_instance,
    is_float,
    is_windows,
    threaded,
)

# Default 256 MB message length
MAX_MESSAGE_LENGTH = int(os.environ.get("PYMECHANICAL_MAX_MESSAGE_LENGTH", 256 * 1024**2))


def setup_logger(loglevel="INFO", log_file=True, mechanical_instance=None):
    """Initialize the logger for the given mechanical instance."""
    # return existing log if this function has already been called
    if hasattr(setup_logger, "log"):
        return setup_logger.log
    else:
        setup_logger.log = LOG.add_instance_logger("Mechanical", mechanical_instance)

    setup_logger.log.setLevel(loglevel)

    if log_file:
        if isinstance(log_file, str):
            setup_logger.log.log_to_file(filename=log_file, level=loglevel)

    return setup_logger.log


def suppress_logging(func):
    """Decorate a function to suppress the logging for a Mechanical instance."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        mechanical = args[0]
        prior_log_level = mechanical.log.level
        if prior_log_level != "CRITICAL":
            mechanical.set_log_level("CRITICAL")

        out = func(*args, **kwargs)

        if prior_log_level != "CRITICAL":
            mechanical.set_log_level(prior_log_level)

        return out

    return wrapper


SETTINGS_DIR = appdirs.user_data_dir("ansys_mechanical_core")
print(f"ansys_mechanical_core settings directory: {SETTINGS_DIR}")

if not os.path.isdir(SETTINGS_DIR):
    try:
        os.makedirs(SETTINGS_DIR)
    except OSError:
        warnings.warn(
            "Unable to create settings directory.\n"
            "Will be unable to cache Mechanical executable location"
        )

CONFIG_FILE = os.path.join(SETTINGS_DIR, "config.txt")
LOCALHOST = "127.0.0.1"
MECHANICAL_DEFAULT_PORT = 10000


def _version_from_path(path):
    """Extract ansys version from a path.

    Generally, the version of Mechanical is contained in the path:

    C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/AnsysWBU.exe

    /usr/ansys_inc/v231/aisol/.workbench

    Note that if the Mechanical executable, you have to rely on the version
    in the path.

    Parameters
    ----------
    path : str
        Path to the Mechanical executable

    Returns
    -------
    int
        Integer version number (e.g. 231).

    """
    # expect v<ver>/ansys
    # replace \\ with / to account for possible windows path
    matches = re.findall(r"v(\d\d\d)", path.replace("\\", "/"), re.IGNORECASE)
    if not matches:
        raise RuntimeError(f"Unable to extract Ansys version from {path}")
    return int(matches[-1])


def port_in_use(port, host=LOCALHOST):
    """Return True when a port is in use at the given host.

    Must actually "bind" the address.  Just checking if we can create
    a socket is insufficient as it's possible to run into permission
    errors like:

    - An attempt was made to access a socket in a way forbidden by its
      access permissions.
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False

    # below implementation doesn't work
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #     try:
    #         sock.bind((host, port))
    #         return False
    #     except socket.error:
    #         return True


def check_ports(port_range, ip="localhost"):
    """Check the state of ports in a port range."""
    ports = {}
    for port in port_range:
        ports[port] = port_in_use(port, ip)
    return ports


# def close_all_local_instances(port_range=None):
#     """Close all Mechanical instances within a port_range.
#
#     This function can be used when cleaning up from a failed pool or
#     batch run.
#
#     Parameters
#     ----------
#     port_range : list, optional
#         Defaults to ``range(10000, 10200)``.  Expand this range if
#         there are many potential instances of Mechanical in gRPC mode.
#
#     Examples
#     --------
#     Close all instances on in the range of 10000 and 10199.
#
#     >>> import ansys.mechanical.core as pymechanical
#     >>> pymechanical.close_all_local_instances()
#
#     """
#     if port_range is None:
#         port_range = range(10000, 10200)
#
#     @threaded
#     def close_mechanical(port, name="Closing mechanical thread."):
#         try:
#             LOG.debug(name)
#             mechanical = Mechanical(port=port)
#             mechanical.exit()
#         except OSError:
#             pass
#
#     ports = check_ports(port_range)
#     for port_temp, state in ports.items():
#         if state:
#             close_mechanical(port_temp)


def close_all_local_instances(port_range=None):
    """Close all Mechanical instances within a port_range.

    This function can be used when cleaning up from a failed pool or
    batch run.

    Parameters
    ----------
    port_range : list, optional
        Defaults to LOCAL_PORTS (managed by this package).
        Pass a range to cleanup Mechanical using those ports .

    Examples
    --------
    Close all instances stored in LOCAL_PORTS

    >>> import ansys.mechanical.core as pymechanical
    >>> pymechanical.close_all_local_instances()

    """
    if port_range is None:
        port_range = ansys.mechanical.core.LOCAL_PORTS

    @threaded
    def close_mechanical(port, name="Closing mechanical thread."):
        try:
            LOG.debug(name)
            mechanical = Mechanical(port=port)
            mechanical.exit(force=True)
        except OSError:
            pass

    ports = check_ports(port_range)
    for port_temp, state in ports.items():
        if state:
            close_mechanical(port_temp)


# the below implementation doesn't work quite right
# def close_all_local_instances(port_range=None):
#     """Close all Mechanical instances within a port_range.
#
#     This function can be used when cleaning up from a failed pool or
#     batch run.
#
#     Parameters
#     ----------
#     port_range : list, optional
#         Defaults to ``range(10000, 10200)``.  Expand this range if
#         there are many potential instances of Mechanical in gRPC mode.
#
#     Examples
#     --------
#     Close all instances on in the range of 10000 and 10199.
#
#     >>> import ansys.mechanical.core as pymechanical
#     >>> pymechanical.close_all_local_instances()
#
#     """
#     if port_range is None:
#         port_range = range(10000, 10200)
#
#     @threaded
#     def close_mechanical(port, name="Closing mechanical thread."):
#         try:
#             LOG.debug(name)
#             mechanical = Mechanical(port=port)
#             mechanical.exit()
#         except OSError:
#             pass
#
#     ports = check_ports(port_range)
#     for port_temp, state in ports.items():
#         if state:
#             close_mechanical(port_temp)


def create_ip_file(ip, path):
    """Create 'mylocal.ip' file required for ansys to change the IP of the gRPC server."""
    file_name = os.path.join(path, "mylocal.ip")
    with open(file_name, "w") as f:
        f.write(ip)


def _get_available_base_mechanical():
    r"""Return a dictionary of available Mechanical versions with their base paths.

    Returns
    -------
    Return all installed Mechanical paths in Windows

    >>> _get_available_base_mechanical()
    {231: 'C:\\Program Files\\ANSYS Inc\\v231'}

    Within Linux

    >>> _get_available_base_mechanical()
    {231: '/usr/ansys_inc/v231'}
    """
    base_path = None
    if is_windows():
        supported_versions = [231]
        awp_roots = {ver: os.environ.get(f"AWP_ROOT{ver}", "") for ver in supported_versions}
        installed_versions = {
            ver: path for ver, path in awp_roots.items() if path and os.path.isdir(path)
        }
        if installed_versions:
            return installed_versions
        else:
            base_path = os.path.join(os.environ["PROGRAMFILES"], "ANSYS Inc")
    else:
        for path in ["/usr/ansys_inc", "/ansys_inc"]:
            if os.path.isdir(path):
                base_path = path

    if base_path is None:
        return {}

    paths = glob(os.path.join(base_path, "v*"))

    if not paths:
        return {}

    ansys_paths = {}
    for path in paths:
        ver_str = path[-3:]
        if is_float(ver_str):
            ansys_paths[int(ver_str)] = path

    return ansys_paths


def find_mechanical():
    """
    Search for ansys path within the standard install location.

    Returns the path of the latest version.

    Returns
    -------
    ansys_path : str
        Full path to ANSYS executable.

    version : float
        Version float.  For example, 23.1 corresponds to 2023R1.

    Examples
    --------
    Within Windows

    >>> from ansys.mechanical.core.mechanical import find_mechanical
    >>> find_mechanical()
    'C:/Program Files/ANSYS Inc/v231/aisol/bin/winx64/AnsysWBU.exe', 23.1

    Within Linux

    >>> find_mechanical()
    (/usr/ansys_inc/v211/aisol/.workbench, 23.1)
    """
    versions = _get_available_base_mechanical()
    if not versions:
        return "", ""
    version = max(versions.keys())
    ans_path = versions[version]
    if is_windows():
        mechanical_bin = os.path.join(ans_path, "aisol", "bin", "winx64", f"AnsysWBU.exe")
    else:
        mechanical_bin = os.path.join(ans_path, "aisol", ".workbench")
    return mechanical_bin, version / 10


def get_mechanical_path(allow_input=True):
    """Acquire Mechanical Path from a cached file or user input."""
    exe_loc = None
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            exe_loc = f.read()
        # verify
        if not os.path.isfile(exe_loc) and allow_input:
            exe_loc = save_mechanical_path()
    elif allow_input:  # create configuration file
        exe_loc = save_mechanical_path()
    if exe_loc is None:
        exe_loc = find_mechanical()[0]
        if not exe_loc:
            exe_loc = None

    return exe_loc


def check_valid_mechanical():
    """Check if a valid version of Mechanical is installed and preconfigured."""
    mechanical_bin = get_mechanical_path(allow_input=False)
    if mechanical_bin is not None:
        version = _version_from_path(mechanical_bin)
        return not (version < 231 and os.name != "posix")
    return False


def change_default_mechanical_path(exe_loc):
    """Change your default ansys path.

    Parameters
    ----------
    exe_loc : str
        Ansys executable path.  Must be a full path.

    Examples
    --------
    Change default Ansys location on Linux

    >>> from ansys.mechanical.core import mechanical
    >>> mechanical.change_default_mechanical_path('/ansys_inc/v231/aisol/.workbench')
    >>> mechanical.get_mechanical_path()
    '/ansys_inc/v201/ansys/bin/ansys201'

    Change default Ansys location on Windows

    >>> mechanical_pth = 'C:/Program Files/ANSYS Inc/v231/aisol/bin/win64/AnsysWBU.exe'
    >>> mechanical.change_default_mechanical_path(mechanical_pth)
    >>> mechanical.check_valid_mechanical()
    True

    """
    if os.path.isfile(exe_loc):
        with open(CONFIG_FILE, "w") as f:
            f.write(exe_loc)
    else:
        raise FileNotFoundError("File %s is invalid or does not exist" % exe_loc)


def save_mechanical_path(exe_loc=None):  # pragma: no cover
    """Find Mechanical path or query user.

    If no ``exe_loc`` argument is supplied, this function attempt
    to obtain the Mechanical executable from (and in order):
    - The default ansys paths (i.e. 'C:/Program Files/Ansys Inc/vXXX/aiso/bin/AnsysWBU.exe')
    - The configuration file
    - User input

    If ``exe_loc`` is supplied, this function does some checks.
    If successful, it will write that ``exe_loc`` into the config file.

    Parameters
    ----------
    exe_loc : str, optional
        Path of the Mechanical executable ('AnsysWBU.exe'), by default None

    Returns
    -------
    str
        Path of the Mechanical executable.

    Notes
    -----
    The configuration file location (``config.txt``) can be found in
    ``appdirs.user_data_dir("ansys_mechanical_core")``. For example:

    .. code:: python

        >>> import appdirs
        >>> import os
        >>> print(os.path.join(appdirs.user_data_dir("ansys_mechanical_core"), "config.txt"))
        C:/Users/[username]]/AppData/Local/ansys_mechanical_core/ansys_mechanical_core/config.txt

    You can change the default ``exe_loc`` either by modifying the mentioned
    ``config.txt`` file or by executing this function:

    .. code:: python

       >>> from ansys.mechanical.core.mechanical import save_mechanical_path
       >>> save_mechanical_path('/new/path/to/executable')

    """
    if exe_loc is None:
        exe_loc, _ = find_mechanical()

    if is_valid_executable_path(exe_loc):  # pragma: not cover
        if not is_common_executable_path(exe_loc):
            warn_uncommon_executable_path(exe_loc)

        change_default_mechanical_path(exe_loc)
        return exe_loc

    if exe_loc is not None:
        if is_valid_executable_path(exe_loc):
            return exe_loc  # pragma: no cover

    # otherwise, query user for the location
    print("Cached Mechanical executable not found")
    print(
        "You are about to enter manually the path of the ANSYS Mechanical executable "
        "(.workbench. This file is very likely to contained in path ending in "
        "'vXXX/aisol/.workbench', but it is not required.\n \nIf you experience problems "
        "with the input path you can overwrite the configuration file by typing:\n"
        ">>> from ansys.mechanical.core.launcher import save_mechanical_path\n"
        ">>> save_mechanical_path('/new/path/to/executable/')\n"
    )
    need_path = True
    while need_path:  # pragma: no cover
        exe_loc = input("Enter the location of an Mechanical executable (.workbench):")

        if is_valid_executable_path(exe_loc):
            if not is_common_executable_path(exe_loc):
                warn_uncommon_executable_path(exe_loc)
            with open(CONFIG_FILE, "w") as f:
                f.write(exe_loc)
            need_path = False
        else:
            print(
                "The supplied path is either: not a valid file path, or does not "
                "match '.workbench' name."
            )

    return exe_loc


def is_valid_executable_path(exe_loc):  # pragma: no cover
    """Check whether the given exe_loc is valid."""
    if is_windows():
        return (
            os.path.isfile(exe_loc)
            and re.search("AnsysWBU.exe", os.path.basename(os.path.normpath(exe_loc))) is not None
        )
    return (
        os.path.isfile(exe_loc)
        and re.search(".workbench", os.path.basename(os.path.normpath(exe_loc))) is not None
    )


def is_common_executable_path(exe_loc):  # pragma: no cover
    """Check whether the give exe_loc is valid."""
    path = os.path.normpath(exe_loc)
    path = path.split(os.sep)

    is_valid_path = is_valid_executable_path(exe_loc)

    if is_windows():
        return (
            is_valid_path
            and re.search(r"v\d\d\d", exe_loc)
            and "aisol" in path
            and "bin" in path
            and "winx64" in path
            and "AnsysWBU.exe" in path
        )

    return (
        is_valid_path
        and re.search(r"v\d\d\d", exe_loc)
        and "aisol" in path
        and ".workbench" in path
    )


def warn_uncommon_executable_path(exe_loc):  # pragma: no cover
    """Display warning for the wrong exe_loc."""
    if is_windows():
        warnings.warn(
            f"The supplied path ('{exe_loc}') does not match the usual Mechanical "
            f"executable path style ('directory/vXXX/aisol/bin/winx64/AnsysWBU.exe'). "
            "You might have problems at later use."
        )
    else:
        warnings.warn(
            f"The supplied path ('{exe_loc}') does not match the usual Mechanical "
            f"executable path style ('directory/vXXX/aisol/.workbench'). "
            "You might have problems at later use."
        )


class Mechanical(object):
    """Connects to a GRPC Mechanical server and allows commands to be passed."""

    # Required by `_name` method to be defined before __init__ be
    _ip = None
    _port = None

    def __init__(
        self,
        ip=None,
        port=None,
        timeout=60.0,
        loglevel="WARNING",
        log_file=False,
        log_mechanical=None,
        cleanup_on_exit=False,
        channel=None,
        remote_instance=None,
        keep_connection_alive=True,
        **kwargs,
    ):
        """Initialize the member variable to based on the arguments.

        Parameters
        ----------
        ip : str, optional
            IP address to connect to the server.  Defaults to 'localhost'.

        port : int, optional
            Port to connect to the Mecahnical server.  Defaults to 10000.

        timeout : float
            Maximum allowable time to connect to the Mechanical server.

        loglevel : str, optional
            Sets which messages are printed to the console.  Default
            'INFO' prints out all ANSYS messages, 'WARNING` prints only
            messages containing ANSYS warnings, and 'ERROR' prints only
            error messages.

        log_file : bool, optional
            Copy the log to a file called `logs.log` located where the
            python script is executed. Default ``True``.

        log_mechanical : str, optional
            Enables logging every script command to the local disk.  This
            can be used to "record" all the commands that are sent to
            Mechanical via PyMechanical so a script can be run within Mechanical without
            PyMechanical. This string is the path of the output file (e.g.
            ``log_mechanical='pymechanical_log.txt'``). By default this is disabled.

        cleanup_on_exit : bool, optional
            Exit Mechanical when Python exits or when this instance is garbage
            collected.

        channel : grpc.Channel, optional
            gRPC channel to use for the connection. Can be used as an
            alternative to the ``ip`` and ``port`` parameters.

        remote_instance : ansys.platform.instancemanagement.Instance
            The corresponding remote instance when Mechanical is launched through
            PyPIM. This instance will be deleted when calling
            :func:`mecahnical.exit <ansys.mechanical.core.Mechanical.exit>`.

        keep_connection_alive : bool, optional
            Keeps the grpc connection alive by running a background thread and making dummy calls
            for remote connections.
            Default ``True``.

        Examples
        --------
        Connect to an instance of Mechanical already running on locally on the
        default port 10000.

        >>> from ansys.mechanical import core as pymechanical
        >>> mechanical = pymechanical.Mechanical()

        Connect to an instance of Mechanical running on the LAN on a default port.

        >>> mechanical = pymechanical.Mechanical('192.168.1.101')

        Connect to an instance of Mechanical running on the LAN on a non-default port.

        >>> mechanical = pymechanical.Mechanical('192.168.1.101', port=60001)

        If you wish to customize the channel, you can also directly connect
        directly to gRPC channels. For example, if you wanted to create an insecure
        channel with a maximum message length of 8 MB.

        >>> import grpc
        >>> channel_temp = grpc.insecure_channel(
        ...     '127.0.0.1:10000',
        ...     options=[
        ...         ("grpc.max_receive_message_length", 8*1024**2),
        ...     ],
        ... )
        >>> mechanical = pymechanical.Mechanical(channel=channel_temp)
        """
        self._remote_instance = remote_instance
        self._keep_connection_alive = keep_connection_alive

        # ip could be a machine name. Convert it to ip address
        ip_temp = ip
        if channel is not None:
            if ip is not None or port is not None:
                raise ValueError(
                    "If `channel` is specified, neither `port` nor `ip` can be specified."
                )
        elif ip is None:
            ip_temp = "127.0.0.1"
        else:
            ip_temp = socket.gethostbyname(ip)  # Converting ip or hostname to ip

        self._ip = ip_temp
        self._port = port

        self._start_parm = kwargs

        self._logLevel = loglevel
        self._log_file = log_file
        self._log_mechanical = log_mechanical

        self._log = LOG.add_instance_logger(self._name, self, level=loglevel)  # instance logger
        # adding a file handler to the logger
        if log_file:
            if not isinstance(log_file, str):
                log_file = "instance.log"
            self._log.log_to_file(filename=log_file, level=loglevel)

        self._log_file_mechanical = log_mechanical
        if log_mechanical:
            if not isinstance(log_mechanical, str):
                self._log_file_mechanical = "pymechanical_log.txt"
            else:
                self._log_file_mechanical = log_mechanical

        # temporarily disable logging
        # useful when we run some dummy calls
        self._disable_logging = False

        self._stub = None
        self._cleanup_on_exit = cleanup_on_exit
        self._busy = False  # used to check if running a command on the server

        self._local = ip_temp in ["127.0.0.1", "127.0.1.1", "localhost"]
        if "local" in kwargs:  # pragma: no cover  # allow this to be overridden
            self._local = kwargs["local"]

        self._health_response_queue = None
        self._exiting = False
        self._exited = None

        self.version = None

        if port is None:
            port = MECHANICAL_DEFAULT_PORT
            self._port = port

        self._stub = None
        self._timeout = timeout

        if channel is None:
            self._channel = self._create_channel(ip_temp, port)
        else:
            self._channel = channel

        # connect and validate to the channel
        self._multi_connect(timeout=timeout)

        self.log_info("mechanical is ready to accept grpc calls")

    def __del__(self):  # pragma: no cover
        """Clean up when complete."""
        if self._cleanup_on_exit:
            try:
                self.exit(force=True)
            except grpc.RpcError as e:
                self.log_error(f"exit: {e}")

    def _set_log_level(self, level):
        """Alias for set_log_level."""
        self.set_log_level(level)

    @property
    def log(self):
        """Return the log associated with the current Mechanical instance."""
        return self._log

    @property
    def _name(self):
        """Instance unique identifier."""
        if self._ip or self._port:
            return f"GRPC_{self._ip}:{self._port}"
        return f"GRPC_instance_{id(self)}"

    def get_name(self):
        """Return the instance unique identifier."""
        return self._name

    def _multi_connect(self, n_attempts=5, timeout=15):
        """Try to connect over a series of attempts to the channel.

        Parameters
        ----------
        n_attempts : int, optional
            Number of connection attempts.
        timeout : float, optional
            Total timeout.

        """
        # This prevents a single failed connection from blocking other attempts
        connected = False
        attempt_timeout = timeout / n_attempts

        max_time = time.time() + timeout
        i = 1
        while time.time() < max_time and i <= n_attempts:
            self.log_debug(f"Connection attempt {i}")
            connected = self._connect(timeout=attempt_timeout)
            i += 1
            if connected:
                self.log_debug("Connected")
                break
        else:
            self.log_debug(
                f"Reached either maximum amount of connection attempts "
                f"({n_attempts}) or timeout ({timeout} s)."
            )

        if not connected:
            raise IOError(f"Unable to connect to Mechanical gRPC instance at {self._channel_str}")

    @property
    def _channel_str(self):
        """Return the target string.

        Generally of the form of "ip:port", like "127.0.0.1:10000".

        """
        if self._channel is not None:
            return self._channel._channel.target().decode()
        return ""

    def _connect(self, timeout=5, enable_health_check=False):
        """Establish a gRPC channel to a remote or local Mechanical instance.

        Parameters
        ----------
        timeout : float
            Time in seconds to wait until the connection has been established
        """
        self._state = grpc.channel_ready_future(self._channel)
        self._stub = mechanical_pb2_grpc.MechanicalServiceStub(self._channel)

        # verify connection
        time_start = time.time()
        while ((time.time() - time_start) < timeout) and not self._state._matured:
            time.sleep(0.01)

        if not self._state._matured:  # pragma: no cover
            return False
        self.log_debug("Established connection to Mechanical gRPC")

        self.wait_till_mechanical_is_ready(timeout)

        # keeps Mechanical session alive
        self._timer = None
        if not self._local and self._keep_connection_alive:
            self._initialised = threading.Event()
            self._t_trigger = time.time()
            self._t_delay = 30
            self._timer = threading.Thread(
                target=Mechanical._threaded_heartbeat, args=(weakref.proxy(self),)
            )
            self._timer.daemon = True
            self._timer.start()

        # enable health check
        if enable_health_check:
            self._enable_health_check()

        self.__server_version = None

        return True

    def _enable_health_check(self):
        """Place the status of the health check in _health_response_queue."""
        # lazy imports here to speed up module load
        from grpc_health.v1 import health_pb2, health_pb2_grpc

        def _consume_responses(response_iterator, response_queue):
            try:
                for response in response_iterator:
                    response_queue.put(response)
                # NOTE: we're doing absolutely nothing with this as
                # this point since the server side health check
                # doesn't change state.
            except Exception:
                if self._exiting:
                    return
                self._exited = True
                raise MechanicalExitedError("Lost connection with Mechanical server") from None

        # enable health check
        from queue import Queue

        request = health_pb2.HealthCheckRequest()
        self._health_stub = health_pb2_grpc.HealthStub(self._channel)
        rendezvous = self._health_stub.Watch(request)

        # health check feature implemented after 2023 R1
        try:
            status = rendezvous.next()
        except Exception as err:
            if err.code().name != "UNIMPLEMENTED":
                raise err
            return

        if status.status != health_pb2.HealthCheckResponse.SERVING:
            raise MechanicalRuntimeError(
                "Unable to enable health check and/or connect to" " the Mechanical server"
            )

        self._health_response_queue = Queue()

        # allow main process to exit by setting daemon to true
        thread = threading.Thread(
            target=_consume_responses,
            args=(rendezvous, self._health_response_queue),
            daemon=True,
        )
        thread.start()

    def _threaded_heartbeat(self):
        """To be called from a thread to verify Mechanical instance is alive."""
        self._initialised.set()
        while True:
            if self._exited:
                break
            try:
                time.sleep(self._t_delay)
                if not self.is_alive:
                    break
            except ReferenceError:
                break
            # except Exception:
            #     continue

    def _create_channel(self, ip, port):
        """Create an unsecured grpc channel."""
        check_valid_ip(ip)

        # open the channel
        channel_str = f"{ip}:{port}"
        self.log_debug(f"Opening insecure channel at {channel_str}")
        return grpc.insecure_channel(
            channel_str,
            options=[
                ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
            ],
        )

    @property
    def is_alive(self) -> bool:
        """Return True when there is an active connect to the gRPC server."""
        if self._exited:
            return False

        if self._busy:
            return True

        try:
            self.__make_dummy_call()
            return True
        except grpc.RpcError:
            return False

    @staticmethod
    def set_log_level(loglevel):
        """Set log level.

        Parameters
        ----------
        loglevel : str, int
            Log level.  Must be one of: ``'DEBUG', 'INFO', 'WARNING', 'ERROR'``.

        Examples
        --------
        Set the log level to debug

        # >>> mechanical.set_log_level('DEBUG')
        #
        # Set the log level to info
        #
        # >>> mechanical.set_log_level('INFO')
        #
        # Set the log level to warning
        #
        # >>> mechanical.set_log_level('WARNING')
        #
        # Set the log level to error
        #
        # >>> mechanical.set_log_level('ERROR')
        """
        if isinstance(loglevel, str):
            loglevel = loglevel.upper()
        setup_logger(loglevel=loglevel)

    def get_product_info(self):
        """Get the product info by running the script in the grpc server."""
        try:
            self._disable_logging = True
            return self.run_jscript("scriptcode.getProductInfo()")
        except grpc.RpcError:
            raise
        finally:
            self._disable_logging = False

    @suppress_logging
    def __str__(self):
        """Return the user-readable string form of the Mechanical instance."""
        try:
            if self._exited:
                return "Mechanical exited"
            return self.get_product_info()
        except grpc.RpcError:
            return "Mechanical exited"

    def launch(self, cleanup_on_exit=True):
        """Launch the Mechanical in batch or UI mode.

        Parameters
        ----------
        cleanup_on_exit : bool, optional
            Exit Mechanical when Python exits or when this instance is garbage
            collected. Default
        """
        if not self._local:
            raise RuntimeError("Can only launch with a local instance of Mechanical")

        # let us respect the current cleanup behavior
        if self._cleanup_on_exit:
            self.exit()

        exec_file = self._start_parm.get("exec_file", get_mechanical_path(allow_input=False))
        batch = self._start_parm.get("batch", True)
        additional_switches = self._start_parm.get("additional_switches", None)
        additional_envs = self._start_parm.get("additional_envs", None)
        port = launch_grpc(
            exec_file=exec_file,
            batch=batch,
            additional_switches=additional_switches,
            additional_envs=additional_envs,
            verbose=True,
        )
        # update the new cleanup behavior
        self._cleanup_on_exit = cleanup_on_exit
        self._port = port
        self._channel = self._create_channel(self._ip, port)
        self._connect(port)

        self.log_info("mechanical is ready to accept grpc calls")

    def wait_till_mechanical_is_ready(self, wait_time=-1):
        """Wait till mechanical is ready.

        Parameters
        ----------
        wait_time : float, optional
            Maximum allowable time to connect to the Mechanical grpc server
        """
        time_1 = datetime.datetime.now()

        sleep_time = 0.5
        if wait_time == -1:
            self.log_info("going to try until the mechanical grpc server is ready")
        else:
            self.log_info(
                f"going to try for {wait_time} seconds to connect to " f"mechanical grpc server"
            )

        while not self.__isMechanicalReady():
            time_2 = datetime.datetime.now()
            time_interval = time_2 - time_1
            time_interval_seconds = int(time_interval.total_seconds())

            self.log_debug(f"mechanical is not ready. waiting so far {time_interval_seconds}")
            if self._timeout != -1:
                if time_interval_seconds > wait_time:
                    self.log_debug(
                        f"allowed wait time {wait_time} seconds. "
                        f"waited for {time_interval_seconds} seconds,"
                        f" before throwing error"
                    )
                    raise RuntimeError(
                        f"Couldn't connect to mechanical. "
                        f"waited for {time_interval_seconds} seconds"
                    )

            time.sleep(sleep_time)

        time_2 = datetime.datetime.now()
        time_interval = time_2 - time_1
        time_interval_seconds = int(time_interval.total_seconds())

        self.log_info(f"mechanical is ready. took {time_interval_seconds} seconds to verify")

    def __isMechanicalReady(self):
        """Return whether the Mechanical grpc server is ready or not.

        Returns
        -------
            Return True if Mechanical is ready otherwise False
        """
        try:
            jscript_block = "DS.Script.isDistributed()"
            self.run_jscript(jscript_block)
        except grpc.RpcError as error:
            self.log_debug(f"mechanical is not ready. error:{error.details()}")
            return False

        return True

    def run_jscript(
        self, script_block: str, enable_logging=False, log_level="WARNING", timeout=2000
    ):
        """Run jscript block inside Mechanical.

        Parameters
        ----------
        script_block :
            script block (one or more lines) to run.

        enable_logging: bool, default is False
            Enable or Disable logging

        log_level: str
            Log level.  Must be one of: ``'DEBUG', 'INFO', 'WARNING', 'ERROR'``.

        timeout: int
            Frequency at which to get the log messages from the server in ms. Default is 2000 ms

        Returns
        -------
        str
            Return value in the string form.
        """
        self.verify_valid_connection()
        response = self.__call_run_jscript(script_block, enable_logging, log_level, timeout)
        return response.script_result

    @staticmethod
    def convert_to_server_log_level(log_level):
        """Convert the log_level to server_log_level.

        Parameters
        ----------
        log_level : str
            Log level.  Must be one of: ``'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'``.

        Returns
        -------
            Return the converted log level for the server
        """
        if log_level == "DEBUG":
            return 1
        elif log_level == "INFO":
            return 2
        elif log_level == "WARNING":
            return 3
        elif log_level == "ERROR":
            return 4
        elif log_level == "CRITICAL":
            return 5

        raise ValueError(
            f"not a valid log_level: {log_level}. Possible values are "
            f"'DEBUG','INFO', 'WARNING', 'ERROR', 'CRITICAL'"
        )

    def run_python_script(
        self, script_block: str, enable_logging=False, log_level="WARNING", timeout=2000
    ):
        """Run python script block inside Mechanical.

        Parameters
        ----------
        script_block :
            script block (one or more lines) to run.

        enable_logging: bool, default is False
            Enable or Disable logging

        log_level: str
            Log level.  Must be one of: ``'DEBUG', 'INFO', 'WARNING', 'ERROR'``.

        timeout: int
            Frequency at which to get the log messages from the server in ms. Default is 2000 ms

        Returns
        -------
        str
            Return value in the string form.
        """
        self.verify_valid_connection()
        response = self.__call_run_python_script(script_block, enable_logging, log_level, timeout)
        return response.script_result

    def run_jscript_from_file(
        self, file_path, enable_logging=False, log_level="WARNING", progress_interval=2000
    ):
        """Run the jscript file inside Mechanical.

        Parameters
        ----------
        file_path :
            This file contains jscript

        enable_logging: bool, default is False
            Enable or Disable logging

        log_level: str
            Log level.  Must be one of: ``'DEBUG', 'INFO', 'WARNING', 'ERROR'``.

        progress_interval: int
            Frequency at which to get the log messages from the server in ms. Default is 2000 ms

        Returns
        -------
        str
            Return value in the string form.
        """
        self.verify_valid_connection()
        self.log_debug(f"run_jscript_from_file started")
        script_code = Mechanical.__readfile(file_path)
        self.log_debug(f"run_jscript_from_file done")
        return self.run_jscript(script_code, enable_logging, log_level, progress_interval)

    def run_python_script_from_file(
        self, file_path, enable_logging=False, log_level="WARNING", progress_interval=2000
    ):
        """Run the python file inside Mechanical.

        Parameters
        ----------
        file_path :
            This file contains python script

        enable_logging: bool, default is False
            Enable or Disable logging

        log_level: str
            Log level.  Must be one of: ``'DEBUG', 'INFO', 'WARNING', 'ERROR'``.

        progress_interval: int
            Frequency at which to get the log messages from the server in ms. Default is 2000 ms

        Returns
        -------
        str
            Return value in the string form.
        """
        self.verify_valid_connection()
        self.log_debug(f"run_python_script_from_file started")
        script_code = Mechanical.__readfile(file_path)
        self.log_debug(f"run_python_script_from_file started")
        return self.run_python_script(script_code, enable_logging, log_level, progress_interval)

    def exit(self, force=False):
        """Exit Mechanical.

        Parameters
        ----------
        force : bool, optional
            Control the exit_behavior. False - asks for confirmation (only in UI mode).
            Override any environment variables that may inhibit exiting Mechanical.
        """
        if not force:
            if get_start_instance():
                self.log_info("Ignoring exit due to PYMECHANICAL_START_INSTANCE=False")
                return

        if self._exited:
            return

        self.verify_valid_connection()

        self._exiting = True

        self.log_debug("In shutdown")
        request = mechanical_pb2.ShutdownRequest(force_exit=force)
        self.log_debug("shutdown running")

        self._busy = True
        try:
            self._stub.Shutdown(request)
        finally:
            self._busy = False

        self._exited = True

        if self._remote_instance is not None:
            self.log_debug("pypim delete started")
            self._remote_instance.delete()
            self.log_debug("pypim delete done")

            self._remote_instance = None
        else:
            self.log_debug("No pypim cleanup needed")

        local_ports = ansys.mechanical.core.LOCAL_PORTS
        if self._local and self._port in local_ports:
            local_ports.remove(self._port)

        self.log_info("shutdown done")

    def upload_file(self, file_path, file_location_destination="", chunk_size=1048576):
        """Upload given file to the server.

        Parameters
        ----------
        file_path  :
            Path of the local file to be uploaded
        file_location_destination
            Destination path on the server where file needs to be copied
        chunk_size
            Sends chunk_size bytes at a time to the server
        """
        self.verify_valid_connection()

        self._busy = True
        try:
            chunks = Mechanical.get_file_chunks(file_location_destination, file_path, chunk_size)
            response = self._stub.UploadFile(chunks)
            self.log_debug(f"upload_file response is {response.is_ok}")
        finally:
            self._busy = False

    def download_file(self, file_path, file_location_destination="", chunk_size=1048576):
        """Download a given file from the server.

        Parameters
        ----------
        file_path  :
            Path of the server file to be downloaded
        file_location_destination
            Destination path on the local machine where file needs to be copied
        chunk_size
            Receives chunk_size bytes at a time from the server
        """
        self.verify_valid_connection()

        if len(file_location_destination) == 0:
            directory = os.getcwd()
        else:
            directory = file_location_destination

        base_name = os.path.basename(file_path)
        output_path = os.path.join(directory, base_name)

        request = mechanical_pb2.FileDownloadRequest(file_path=file_path, chunk_size=chunk_size)

        self._busy = True
        try:
            with open(output_path, "wb") as f:
                for file_download_response in self._stub.DownloadFile(request):
                    f.write(file_download_response.chunk.payload)
        finally:
            self._busy = False

    def clear(self):
        """Clear the database."""
        self.run_python_script("ExtAPI.DataModel.Project.New()")

    def __make_dummy_call(self):
        try:
            self._disable_logging = True
            self.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")
        except grpc.RpcError:
            raise
        finally:
            self._disable_logging = False

    @staticmethod
    def get_file_chunks(file_location, file_path, chunk_size):
        """Construct the file upload request for the server."""
        with open(file_path, "rb") as f:
            while True:
                piece = f.read(chunk_size)
                length = len(piece)
                if length == 0:
                    return
                chunk = mechanical_pb2.Chunk(payload=piece, size=length)
                yield mechanical_pb2.FileUploadRequest(
                    file_name=os.path.basename(file_path), file_location=file_location, chunk=chunk
                )

    @staticmethod
    def __readfile(file_path):
        """Return the contents of the file as a string."""
        # open text file in read mode
        text_file = open(file_path, "r")
        # read whole file to a string
        data = text_file.read()
        # close file
        text_file.close()

        return data

    def __call_run_jscript(self, script_code: str, enable_logging, log_level, progress_interval):
        """Run the jscript block on the server."""
        log_level_server = self.convert_to_server_log_level(log_level)
        request = mechanical_pb2.RunScriptRequest()
        request.script_code = script_code
        request.enable_logging = enable_logging
        request.logger_severity = log_level_server
        request.progress_interval = progress_interval

        response = None
        self._busy = True

        try:
            for runscript_response in self._stub.RunJScript(request):
                if runscript_response.log_info == "__done__":
                    response = runscript_response
                    break
                else:
                    if enable_logging:
                        self.log_message(log_level, runscript_response.log_info)
        finally:
            self._busy = False

        return response

    def __call_run_python_script(
        self, script_code: str, enable_logging, log_level, progress_interval
    ):
        """Run the python script block on the server."""
        log_level_server = self.convert_to_server_log_level(log_level)
        request = mechanical_pb2.RunScriptRequest()
        request.script_code = script_code
        request.enable_logging = enable_logging
        request.logger_severity = log_level_server
        request.progress_interval = progress_interval

        response = None
        self._busy = True

        try:
            for runscript_response in self._stub.RunPythonScript(request):
                if runscript_response.log_info == "__done__":
                    response = runscript_response
                    break
                else:
                    if enable_logging:
                        self.log_message(log_level, runscript_response.log_info)
        finally:
            self._busy = False

        self._log_mechanical_script(script_code)

        return response

    def log_message(self, log_level, message):
        """Log the message using the given log_level.

         Parameters
        ----------
        log_level: str
            Log level.  Must be one of: ``'DEBUG', 'INFO', 'WARNING', 'ERROR'``.
        message : str
            Message to be logged
        """
        if log_level == "DEBUG":
            self.log_debug(message)
        elif log_level == "INFO":
            self.log_info(message)
        elif log_level == "WARNING":
            self.log_warning(message)
        elif log_level == "ERROR":
            self.log_error(message)

    def log_debug(self, message):
        """Log the debug message."""
        if self._disable_logging:
            return
        self._log.debug(message)

    def log_info(self, message):
        """Log the info message."""
        if self._disable_logging:
            return
        self._log.info(message)

    def log_warning(self, message):
        """Log the warning message."""
        if self._disable_logging:
            return
        self._log.warning(message)

    def log_error(self, message):
        """Log the error message."""
        if self._disable_logging:
            return
        self._log.error(message)

    def verify_valid_connection(self):
        """Verify whether we have any valid connection to Mechanical."""
        if self._exited:
            raise MechanicalExitedError

        if self._stub is None:
            raise ValueError(
                "Don't have a valid connection to mechanical. Use either launch or connect first."
            )

    @property
    def exited(self):
        """Verify whether Mechanical already exited or not."""
        return self._exited

    def _log_mechanical_script(self, script_code):
        if self._disable_logging:
            return

        if self._log_file_mechanical:
            try:
                with open(self._log_file_mechanical, "a") as file:
                    file.write(script_code)
                    file.write("\n")
            except IOError as e:
                self.log_warning(f"I/O error({e.errno}): {e.strerror}")
            except Exception as e:  # handle other exceptions such as attribute errors
                self.log_warning("Unexpected error:" + str(e))


def get_start_instance(start_instance_default=True):
    """Check if the environment variable ``PYMECHANICAL_START_INSTANCE`` exists and is valid.

    Parameters
    ----------
    start_instance_default : bool
        Value to return when ``PYMECHANICAL_START_INSTANCE`` is unset.

    Returns
    -------
    bool
        ``True`` when the ``PYMECHANICAL_START_INSTANCE`` environment variable is
        true, ``False`` when PYMECHANICAL_START_INSTANCE is false. If unset,
        returns ``start_instance_default``.

    Raises
    ------
    OSError
        Raised when ``PYMECHANICAL_START_INSTANCE`` is not either true or false
        (case independent).

    """
    if "PYMECHANICAL_START_INSTANCE" in os.environ:
        if os.environ["PYMECHANICAL_START_INSTANCE"].lower() not in ["true", "false"]:
            val = os.environ["PYMECHANICAL_START_INSTANCE"]
            raise OSError(
                f'Invalid value "{val}" for PYMECHANICAL_START_INSTANCE\n'
                'PYMECHANICAL_START_INSTANCE should be either "TRUE" or "FALSE"'
            )
        return os.environ["PYMECHANICAL_START_INSTANCE"].lower() == "true"
    return start_instance_default


def launch_grpc(
    exec_file="",
    batch=True,
    port=MECHANICAL_DEFAULT_PORT,
    ip=LOCALHOST,
    additional_switches=None,
    additional_envs=None,
    verbose=False,
) -> int:
    """Start Mechanical locally in gRPC mode.

    Parameters
    ----------
    exec_file : str, optional
        The location of the Mechanical executable.  Will use the cached
        location when left at the default ``None``.

    batch : bool, optional
        Launches mechanical in batch or UI mode. Default is True

    port : int
        Port to launch Mechanical gRPC on.  Final port will be the first
        port available after (or including) this port.

    ip : str, optional
        IP to use to connect to the launched instance. Default is 127.0.0.1

    additional_switches : list, optional
        List of additional arguments to pass. Default - None

    additional_envs : dictionary, optional
        dictionary of additional environment variables to pass. Default - None

    verbose : bool, optional
        Print all output when launching and running Mechanical.  Not
        recommended unless debugging the Mechanical start.  Default
        ``False``.

    Returns
    -------
    int
        Returns the port number that the gRPC instance started on.

    Notes
    -----
    If ``PYMECHANICAL_START_INSTANCE`` is set to FALSE, this ``launch_mechanical`` will
    look for an existing instance of Mechanical at ``PYMECHANICAL_IP`` on port
    ``PYMECHANICAL_PORT``, with defaults 127.0.0.1 and 10000 if unset. This is
    typically used for automated documentation and testing.

    Examples
    --------
    Launch Mechanical using the default configuration.

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mechanical = launch_mechanical()

    Run Mechanical with specified the location of the Mechanical binary.

    >>> exec_file_path = 'C:/Program Files/ANSYS Inc/v231/aisol/bin/win64/AnsysWBU.exe'
    >>> mechanical = launch_mechanical(exec_file_path)

    """
    # verify version
    if _version_from_path(exec_file) < 231:
        raise VersionError("The Mechanical gRPC interface requires Mechanical 231 or later")

    # get the next available port
    local_ports = ansys.mechanical.core.LOCAL_PORTS
    if port is None:
        if not local_ports:
            port = MECHANICAL_DEFAULT_PORT
        else:
            port = max(local_ports) + 1

    while port_in_use(port) or port in local_ports:
        port += 1
    local_ports.append(port)

    # setting ip for the grpc server
    if ip != LOCALHOST:  # Default local ip is 127.0.0.1
        create_ip_file(ip, os.getcwd())

    # exec_file = "",
    # port = MECHANICAL_DEFAULT_PORT,
    # ip = LOCALHOST,
    # additional_switches = "",
    # verbose = False,

    mechanical_launcher = MechanicalLauncher(
        batch, port, exec_file, additional_switches, additional_envs, verbose
    )
    mechanical_launcher.launch()

    return port


def launch_remote_mechanical(
    version=None,
    cleanup_on_exit=True,
) -> Mechanical:
    """Start Mechanical remotely using the product instance management API.

    When calling this method, you need to ensure that you are in an environment
    where PyPIM is configured.This can be verified with
    :func:`pypim.is_configured <ansys.platform.instancemanagement.is_configured>`.

    Parameters
    ----------
    version : str, optional
        The Mechanical version to run, in the 3 digits format, such as "231".

        If unspecified, the version will be chosen by the server.

    cleanup_on_exit : bool, optional
        Exit Mechanical when python exits or the Mechanical Python instance is
        garbage collected.

        If unspecified, it will be cleaned up.

    Returns
    -------
    ansys.mechanical.mechanical.core.Mechanical
    """
    pim = pypim.connect()
    instance = pim.create_instance(product_name="mechanical", product_version=version)

    print("pypim wait for ready started")
    instance.wait_for_ready()
    print("pypim wait for ready done")

    channel = instance.build_grpc_channel(
        options=[
            ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
        ]
    )
    return Mechanical(channel=channel, cleanup_on_exit=cleanup_on_exit, remote_instance=instance)


def launch_mechanical(
    exec_file=None,
    batch=True,
    loglevel="ERROR",
    log_file=False,
    log_mechanical=None,
    additional_switches="",
    additional_envs=None,
    start_timeout=120,
    port=None,
    ip=None,
    start_instance=None,
    verbose_mechanical=False,
    clear_on_connect=False,
    cleanup_on_exit=True,
    version=None,
    keep_connection_alive=True,
) -> Mechanical:
    """Start Mechanical locally.

    Parameters
    ----------
    exec_file : str, optional
        The location of the Mechanical executable.  Will use the cached
        location when left at the default ``None``. If pypim is configured
        and exce_file is None, it will launch using pypim using the ``version``.

    batch : bool, optional
        Launches mechanical in batch or UI mode. Default is True

    loglevel : str, optional
        Sets which messages are printed to the console.  ``'INFO'``
        prints out all ANSYS messages, ``'WARNING``` prints only
        messages containing ANSYS warnings, and ``'ERROR'`` logs only
        error messages.

    log_file : bool, optional
        Copy the log to a file called `logs.log` located where the
        python script is executed. Default ``False``.

    log_mechanical : str, optional
        Enables logging every script command to the local disk.  This
        can be used to "record" all the commands that are sent to
        Mechanical via PyMechanical so a script can be run within Mechanical without
        PyMechanical. This string is the path of the output file (e.g.
        ``log_mechanical='pymechanical_log.txt'``). By default this is disabled.

    additional_switches : str, optional
        Additional switches for Mechanical

    additional_envs : dictionary, optional
        dictionary of additional environment variables to pass. Default - None

    start_timeout : float, optional
        Maximum allowable time to connect to the Mechanical server.

    port : int
        Port to launch Mechanical gRPC on.  Final port will be the first
        port available after (or including) this port.  Defaults to
        10000.  You can also override the default behavior of this
        keyword argument with the environment variable
        ``PYMECHANICAL_PORT=<VALID PORT>``

    ip : str, optional
        Used only when ``start_instance`` is ``False``. If provided,
        it will force ``start_instance`` to be ``False``.
        You can also provide a hostname as an alternative to an IP address.
        Defaults to ``'127.0.0.1'``.

    start_instance : bool, optional
        When False, connect to an existing Mechanical instance at ``ip``
        and ``port``, which default to ``'127.0.0.1'`` at 10000.
        Otherwise, launch a local instance of Mechanical.  You can also
        override the default behavior of this keyword argument with
        the environment variable ``PYMECHANICAL_START_INSTANCE=FALSE``.
        Default ``None``

    verbose_mechanical : bool, optional
        Enable printing of all output when launching and running
        Mechanical.  This should be used for debugging only as output can
        be tracked within pymechanical.  Default ``False``.

    clear_on_connect : bool, optional
        Used only when ``start_instance`` is ``False``.  Defaults to
        ``False``, Pass True to give you a fresh environment when connecting to
        Mechanical.

    cleanup_on_exit : bool, optional
        Exit Mechanical when python exits or the Mechanical Python instance is
        garbage collected. Default ``True``

    version : str, optional
        The Mechanical version to run, in the 3 digits format, such as "231".
        If unspecified, the version will be chosen by the server.
        If pypim is configured and exce_file is None, it will launch using
        pypim using the ``version``

    keep_connection_alive : bool, optional
        Keeps the grpc connection alive by running a background thread and making dummy calls
        for remote connections.
        Default ``True``.

    Returns
    -------
    ansys.mechanical.core.mechanical.Mechanical
        An instance of Mechanical.

    Notes
    -----
    If the environment is configured to use `PyPIM <https://pypim.docs.pyansys.com>`_
    and ``start_instance`` is ``True``, then starting the instance will be delegated to PyPIM.
    In this event, most of the options will be ignored and the server side configuration will
    be used.

    Examples
    --------
    Launch Mechanical

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mech = launch_mechanical()

    Run Mechanical with specified the location of the binary.

    >>> exec_file_path = 'C:/Program Files/ANSYS Inc/v231/aisol/bin/win64/AnsysWBU.exe'
    >>> mech = launch_mechanical(exec_file_path)

    Connect to an existing instance of Mechanical at IP 192.168.1.30 and
    port 50001.  This is only available using the latest ``'grpc'``
    mode.

    >>> mech = launch_mechanical(start_instance=False, ip='192.168.1.30', port=50001)

    """
    # Start Mechanical with PyPIM if the environment is configured for it
    # and the user did not pass a directive on how to launch it.
    if pypim.is_configured() and exec_file is None:
        LOG.info("Starting Mechanical remotely. The startup configuration will be ignored.")
        return launch_remote_mechanical(version=version, cleanup_on_exit=cleanup_on_exit)

    if ip is None:
        ip = os.environ.get("PYMECHANICAL_IP", LOCALHOST)
    else:  # pragma: no cover
        start_instance = False
        ip = socket.gethostbyname(ip)  # Converting ip or hostname to ip

    check_valid_ip(ip)  # double check

    if port is None:
        port = int(os.environ.get("PYMECHANICAL_PORT", MECHANICAL_DEFAULT_PORT))
        check_valid_port(port)

    # connect to an existing instance if enabled
    if start_instance is None:
        start_instance = check_valid_start_instance(
            os.environ.get("PYMECHANICAL_START_INSTANCE", True)
        )

    if not start_instance:
        mechanical = Mechanical(
            ip=ip,
            port=port,
            loglevel=loglevel,
            log_file=log_file,
            log_mechanical=log_mechanical,
            timeout=start_timeout,
            cleanup_on_exit=cleanup_on_exit,
            keep_connection_alive=keep_connection_alive,
        )
        if clear_on_connect:
            mechanical.clear()

        return mechanical

    # verify executable
    if exec_file is None:
        exec_file = get_mechanical_path()
        if exec_file is None:
            raise FileNotFoundError(
                "Invalid exec_file path or cannot load cached "
                "mechanical path.  Enter one manually by specifying "
                "exec_file="
            )
    else:  # verify ansys exists at this location
        if not os.path.isfile(exec_file):
            raise FileNotFoundError(
                f'Invalid Mechanical executable at "{exec_file}"\n'
                "Enter one manually using exec_file="
            )

    start_parm = {
        "exec_file": exec_file,
        "batch": batch,
        "additional_switches": additional_switches,
        "additional_envs": additional_envs,
    }

    try:
        port = launch_grpc(port=port, verbose=verbose_mechanical, ip=ip, **start_parm)
        mechanical = Mechanical(
            ip=ip,
            port=port,
            loglevel=loglevel,
            log_file=log_file,
            log_mechanical=log_mechanical,
            timeout=start_timeout,
            cleanup_on_exit=cleanup_on_exit,
            keep_connection_alive=keep_connection_alive,
            **start_parm,
        )
    except Exception as exception:
        # pass
        raise exception

    return mechanical
