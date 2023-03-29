"""Contain miscellaneous functions and methods at the module level."""

from functools import wraps
import os
import socket
from threading import Thread


def is_windows():
    """Check if the host machine is on Windows.

    Returns
    -------
    ``True`` if the host machine is on Windows, ``False`` otherwise.
    """
    if os.name == "nt":  # pragma: no cover
        return True

    return False


def get_mechanical_bin(release_version):
    """Get the path for the Mechanical executable file based on the release version.

    Parameters
    ----------
    release_version: str
        Mechanical version using the three-digit format. For example, ``"231"`` for
        2023 R1.
    """
    if is_windows():  # pragma: no cover
        program_files = os.getenv("PROGRAMFILES", os.path.join("c:\\", "Program Files"))
        ans_root = os.getenv(
            f"AWP_ROOT{release_version}",
            os.path.join(program_files, "ANSYS Inc", f"v{release_version}"),
        )
        mechanical_bin = os.path.join(ans_root, "aisol", "bin", "winx64", f"AnsysWBU.exe")
    else:
        ans_root = os.getenv(f"AWP_ROOT{release_version}", os.path.join("/", "usr", "ansys_inc"))
        mechanical_bin = os.path.join(*ans_root, f"v{release_version}", "aisol", f".workbench")

    return mechanical_bin


def threaded(func):
    """Decorate a function with this decorator to call it using a thread."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        name = kwargs.get("name", f"Threaded `{func.__name__}` function")
        thread = Thread(target=func, name=name, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


def threaded_daemon(func):
    """Decorate a function with this decorator to call it using a daemon thread."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        name = kwargs.get("name", f"Threaded (with Daemon) `{func.__name__}` function")
        thread = Thread(target=func, name=name, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread

    return wrapper


def check_valid_ip(ip):
    """Check if the IP address is valid.

    Parameters
    ----------
    ip : str
        IP address to check.

    """
    if ip.lower() != "localhost":
        ip = ip.replace('"', "").replace("'", "")
        socket.inet_aton(ip)


def check_valid_port(port, lower_bound=1000, high_bound=60000):
    """Check if the port is valid.

    Parameters
    ---------
    port : int
        Port to check.
    lower_bound : int, optional
       Lowest possible value for the port. The default is ``1000``.
    high_bound : int, optional
       Highest possible value for the port. The default is ``60000``.
    """
    if not isinstance(port, int):
        raise ValueError("The 'port' parameter must be an integer.")

    if lower_bound < port < high_bound:
        return
    else:
        raise ValueError(f"'port' values must be between {lower_bound} and {high_bound}.")


def check_valid_start_instance(start_instance):
    """
    Check if the value obtained from the environmental variable is valid.

    Parameters
    ----------
    start_instance : str, bool
        Value obtained from the corresponding environment variable.

    Returns
    -------
    bool
        ``True`` if ``start_instance`` is ``True`` or ``"True"``,
        ``False`` otherwise.

    """
    if not isinstance(start_instance, (str, bool)):
        raise ValueError("The value for 'start_instance' should be a string or a boolean.")

    if isinstance(start_instance, bool):
        return start_instance

    if start_instance.lower() not in ["true", "false"]:
        raise ValueError(
            f"The value for 'start_instance' should be 'True' or 'False' (case insensitive)."
        )

    return start_instance.lower() == "true"


def is_float(input_string):
    """Check if a string can be converted to a float.

    Parameters
    ----------
    input_string : str
        String to check.

    Returns
    -------
    bool
        ``True`` when conversion is possible, ``False`` otherwise.
    """
    try:
        float(input_string)
        return True
    except ValueError:
        return False
