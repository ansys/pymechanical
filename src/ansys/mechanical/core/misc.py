# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Contain miscellaneous functions and methods at the module level."""

from functools import wraps
import os
from pathlib import Path
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
        Mechanical version using the three-digit format. For example, ``"252"`` for
        2025 R2.
    """
    if is_windows():  # pragma: no cover
        program_files = os.getenv("PROGRAMFILES", str(Path("c:") / "Program Files"))
        ans_root = os.getenv(
            f"AWP_ROOT{release_version}",
            str(Path(program_files) / "ANSYS Inc" / f"v{release_version}"),
        )
        mechanical_bin = Path(ans_root) / "aisol" / "bin" / "winx64" / "AnsysWBU.exe"
    else:
        ans_root = os.getenv(f"AWP_ROOT{release_version}", str(Path("/") / "usr" / "ansys_inc"))
        mechanical_bin = Path(ans_root) / f"v{release_version}" / "aisol" / ".workbench"

    return str(mechanical_bin)


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
    ----------
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
            "The value for 'start_instance' should be 'True' or 'False' (case insensitive)."
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


def has_grpc_service_pack(version):
    """Check if the Mechanical version supports advanced gRPC options.

    Mechanical versions 241 and later support gRPC, but advanced options like
    transport modes and host binding require Service Pack 04 or later.

    For version 241, this always returns True (assumes SP04+).
    For version 261, this always returns True (forced override).
    For other versions, it checks the builddate.txt file.

    Parameters
    ----------
    version : int
        Mechanical version number (e.g., 241, 251, 261).

    Returns
    -------
    bool
        True if version has SP04+ support, False otherwise.
    """
    if version == 241:
        return True

    if version == 261:
        # FORCED OVERRIDE: Assuming v261 has SP04 support
        # WARNING: This may not be correct for all v261 installations
        return True

    # For other versions, check builddate
    from ansys.tools.common.path import get_mechanical_path

    exe_path = get_mechanical_path(allow_input=False, version=version)

    # If the mechanical path cannot be found, assume no SP04
    if exe_path is None:
        return False

    exe_path = Path(exe_path)

    # Navigate to version root directory (v251) where builddate.txt is located
    # Path structure: .../v251/aisol/bin/winx64/AnsysWBU.exe -> .../v251
    if is_windows():
        # Windows: go up from bin/winx64/AnsysWBU.exe to aisol, then to v251
        version_root = exe_path.parent.parent.parent.parent
    else:
        # Linux: path is typically .../v251/aisol/.workbench -> .../v251
        version_root = exe_path.parent.parent

    builddate_file = version_root / "builddate.txt"

    if not builddate_file.exists():
        # If builddate.txt doesn't exist, assume no SP04
        return False

    # Read first two lines and check for SP04 or higher
    try:
        with builddate_file.open("r", encoding="utf-8", errors="ignore") as f:
            line1 = f.readline().strip()
            line2 = f.readline().strip()
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        with builddate_file.open("r", encoding="latin1", errors="ignore") as f:
            line1 = f.readline().strip()
            line2 = f.readline().strip()

    # Check if either line contains SP04 or higher service pack
    combined_text = f"{line1} {line2}".upper()

    # Look for SP04, SP05, SP06, etc. (SP04 through SP19 should be sufficient)
    for sp_num in range(4, 20):
        sp_tag = f"SP{sp_num:02d}"
        if sp_tag in combined_text:
            return True

    return False


def is_linux() -> bool:
    """Check if the host machine is Linux.

    Returns
    -------
    ``True`` if the host machine is Linux, ``False`` otherwise.
    """
    return os.name == "posix"
