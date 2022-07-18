"""Contain miscellaneous functions and methods at the module level."""

from functools import wraps
import os
import random
import socket
import string
from threading import Thread


def is_windows():
    """Find if the host machine is windows or not.

    Returns
    -------
    Returns True if the host machine is Windows otherwise False
    """
    if os.name == "nt":
        return True

    return False


def get_mechanical_bin(release_version):
    """Identify the Mechanical executable based on the release version (e.g. "231")."""
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


def no_return(func):
    """Decorate a function with this decorator to to return nothing from the wrapped function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

    return wrapper


def check_valid_ip(ip):
    """Check for valid IP address."""
    if ip.lower() != "localhost":
        ip = ip.replace('"', "").replace("'", "")
        socket.inet_aton(ip)


def check_valid_port(port, lower_bound=1000, high_bound=60000):
    """Check for valid port."""
    if not isinstance(port, int):
        raise ValueError("The 'port' parameter should be an integer.")

    if lower_bound < port < high_bound:
        return
    else:
        raise ValueError(f"'port' values should be between {lower_bound} and {high_bound}.")


def check_valid_start_instance(start_instance):
    """
    Check if the value obtained from the environmental variable is valid.

    Parameters
    ----------
    start_instance : str
        Value obtained from the corresponding environment variable.

    Returns
    -------
    bool
        Returns ``True`` if ``start_instance`` is ``True`` or ``"True"``,
        ``False`` if otherwise.

    """
    if not isinstance(start_instance, (str, bool)):
        raise ValueError("The value 'start_instance' should be an string or a boolean.")

    if isinstance(start_instance, bool):
        return start_instance

    if start_instance.lower() not in ["true", "false"]:
        raise ValueError(
            f"The value 'start_instance' should be equal to 'True' or 'False' (case insensitive)."
        )

    return start_instance.lower() == "true"


def is_float(input_string):
    """Return true when a string can be converted to a float."""
    try:
        float(input_string)
        return True
    except ValueError:
        return False


def random_string(string_length=10, letters=string.ascii_lowercase):
    """Generate a random string of fixed length."""
    return "".join(random.choice(letters) for _ in range(string_length))


def _check_has_ansys():
    """Safely wraps check_valid_ansys.

    Returns
    -------
    has_ansys : bool
        True when this local installation has ANSYS installed in a
        standard location.
    """
    from ansys.mechanical.core.mechanical import check_valid_mechanical

    try:
        return check_valid_mechanical()
    except:
        return False
