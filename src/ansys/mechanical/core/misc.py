# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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
    """Check if the Mechanical version supports advanced gRPC security options.

    Advanced gRPC options (transport modes and host binding) require specific service packs:
    - 2024 R2 (242): requires SP05+
    - 2025 R1 (251): requires SP04+
    - 2025 R2 (252): requires SP03+
    - 2026 R1 (261)+: all versions supported

    Parameters
    ----------
    version : int
        Mechanical version number (e.g., 242, 251, 252, 261).

    Returns
    -------
    bool
        True if version has required service pack for gRPC security, False otherwise.
    """
    # Handle None version
    if version is None:
        return False

    # Convert string to int if needed
    if isinstance(version, str):
        try:
            version = int(version)
        except (ValueError, TypeError):
            return False

    # Version 261+ has built-in support
    if version >= 261:
        return True

    # Versions before 242 don't support secure gRPC
    if version < 242:
        return False

    # Define minimum required service pack for each version
    min_service_pack = {
        242: 5,  # 2024 R2 requires SP05
        251: 4,  # 2025 R1 requires SP04
        252: 3,  # 2025 R2 requires SP03
    }

    # If version not in our supported list, assume no support
    if version not in min_service_pack:
        return False

    required_sp = min_service_pack[version]

    # Get the executable path to find builddate.txt
    from ansys.tools.common.path import get_mechanical_path

    exe_path = get_mechanical_path(allow_input=False, version=version)

    if exe_path is None:
        return False

    exe_path = Path(exe_path)

    # Navigate to version root directory where builddate.txt is located
    if is_windows():
        version_root = exe_path.parent.parent.parent.parent
    else:
        version_root = exe_path.parent.parent

    builddate_file = version_root / "builddate.txt"

    if not builddate_file.exists():
        return False

    # Read builddate.txt and check for service pack
    try:
        with builddate_file.open("r", encoding="utf-8", errors="ignore") as f:
            line1 = f.readline().strip()
            line2 = f.readline().strip()
    except UnicodeDecodeError:
        with builddate_file.open("r", encoding="latin1", errors="ignore") as f:
            line1 = f.readline().strip()
            line2 = f.readline().strip()

    combined_text = f"{line1} {line2}".upper()

    # Check if the installed service pack meets the requirement
    for sp_num in range(required_sp, 20):
        sp_tag = f"SP{sp_num:02d}"
        if sp_tag in combined_text:
            return True

    return False


def get_service_pack_message(version):
    """Get the required service pack message for a given version.

    Parameters
    ----------
    version : int
        Mechanical version number (e.g., 241, 242, 251, 252).

    Returns
    -------
    str
        Message indicating required service pack, or empty string if not applicable.
    """
    service_pack_requirements = {
        242: "SP05",  # 2024 R2
        251: "SP04",  # 2025 R1
        252: "SP03",  # 2025 R2
    }

    if version == 241:
        # 2024 R1 does not support secure gRPC at all
        return (
            "Update to Ansys 2024 R2 or later with required service pack for secure gRPC support."
        )
    elif version in service_pack_requirements:
        sp_required = service_pack_requirements[version]
        return f"Update to Service Pack {sp_required} or later for secure gRPC support."
    elif version >= 261:
        return ""  # Version 261+ has built-in support
    else:
        return "Update to Ansys 2024 R2 or later for secure gRPC support."


def is_linux() -> bool:
    """Check if the host machine is Linux.

    Returns
    -------
    ``True`` if the host machine is Linux, ``False`` otherwise.
    """
    return os.name == "posix"


def resolve_certs_dir(transport_mode, certs_dir=None):
    """Resolve the certificate directory for mTLS connections.

    Checks the ANSYS_GRPC_CERTIFICATES environment variable if:
    - transport_mode is "mtls"
    - certs_dir is None (not explicitly provided by user)
    - On Windows: only if the variable is set at user level
    - On Linux: at any level

    Parameters
    ----------
    transport_mode : str
        Transport mode being used (insecure, mtls, wnua).
    certs_dir : str, optional
        Certificate directory path. Default is None, which triggers environment
        variable lookup for mTLS, then defaults to "certs".

    Returns
    -------
    str
        Resolved certificate directory path.
    """
    if transport_mode and transport_mode.lower() == "mtls" and certs_dir is None:
        if is_windows():
            # On Windows, only read user-level environment variable
            try:
                import winreg

                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ
                ) as key:
                    try:
                        value, _ = winreg.QueryValueEx(key, "ANSYS_GRPC_CERTIFICATES")
                        return value
                    except FileNotFoundError:
                        return "certs"
            except ImportError:  # pragma: no cover
                return "certs"
        else:
            # On Linux, read at any level
            return os.environ.get("ANSYS_GRPC_CERTIFICATES", "certs")
    return certs_dir if certs_dir is not None else "certs"
