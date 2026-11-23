# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Initializer for Mechanical embedding. Sets up paths and resolvers."""

from importlib.metadata import distribution
import os
import platform
import sys
import warnings

from ansys.mechanical.core import _installation
from ansys.mechanical.core._capabilities import Capabilities
from ansys.mechanical.core._limitations import Limitations
from ansys.mechanical.core.embedding.loader import load_clr
from ansys.mechanical.core.embedding.resolver import resolve
from ansys.mechanical.core.mechanical import LOG

INITIALIZED_VERSION = None
"""The currently initialized Mechanical version, or None."""

SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS = {
    261: "2026R1",
    252: "2025R2",
    251: "2025R1",
    242: "2024R2",
}
"""Supported Mechanical embedding versions on Windows."""


def __add_sys_path(version: int) -> None:
    sys.path.append(str(_installation.for_version(version).bin_dir.resolve()))


def __workaround_material_server(version: int) -> None:
    """Workaround material server bug in 2024 R1.

    A REST server is used as a backend for the material model GUI.
    In 2024 R1, this GUI is used even in batch mode. The server
    starts by default on a background thread, which may lead to
    a race condition on shutdown.
    """
    if Limitations(version).material_server_race:
        os.environ["ENGRDATA_SERVER_SERIAL"] = "1"


def __check_for_supported_version(version: int) -> int:
    """Check if Mechanical version is supported with current version of PyMechanical.

    If specific environment variable is enabled, then users can overwrite the supported versions.
    However, using unsupported versions may cause issues.
    """
    allow_old_version = os.getenv("ANSYS_MECHANICAL_EMBEDDING_SUPPORT_OLD_VERSIONS") == "1"

    # Check if the version is supported
    if not allow_old_version and version < min(SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS):
        raise ValueError(f"Mechanical version {version} is not supported.")

    return version


def _get_latest_default_version() -> int:
    """Try to get the latest Mechanical version from the environment.

    Check if multiple versions of Mechanical are found in the system.
    For Linux, only one is expected since ``mechanical-env`` takes care of that.
    If multiple versions are detected, the latest one is selected.
    """
    versions_found = sorted(_installation.installed())
    if not versions_found:
        raise RuntimeError(
            "No AWP_ROOT### environment variables pointing to a v<version> folder found.\n"
            "Ensure Mechanical is installed.\n"
            "To set the environment variable manually, use:\n"
            "  AWP_ROOT<version>=/path/to/ansys_inc/v<version>\n"
            "  Example: AWP_ROOT261=/path/to/ansys_inc/v261"
        )

    LOG.info(f"Available versions of Mechanical: {versions_found}")

    latest_version = versions_found[-1]

    if len(versions_found) > 1:
        LOG.warning(
            f"Multiple versions of Mechanical found! Using latest version {latest_version} ..."
        )
    return latest_version


def __check_python_interpreter_architecture() -> None:
    """Embedding support only 64 bit architecture."""
    if platform.architecture()[0] != "64bit":
        raise RuntimeError("Mechanical Embedding requires a 64-bit Python environment.")


def __windows_store_workaround(version: int) -> None:
    """Workaround for Windows store.

    See https://github.com/ansys/pymechanical/issues/1136

    Windows Store Python uses the Win32 API ``SetDefaultDllDirectories`` so
    that the PATH environment variable isn't scanned for any DLL dependency.

    PyMechanical loads the embedding library which automatically sets
    these Paths, but this uses the PATH environment variable which doesn't
    work for Windows store Python.

    We provide a workaround for versions 2024R2 and later that sets
    these paths using `os.add_dll_directory`.

    Note:   This workaround does not include DLL paths used in FSI
            mapping workflows.

    Parameters
    ----------
    version : int
        The version of Mechanical to set the DLL paths for.
    """
    # Nothing to do on Linux
    if sys.platform != "win32":
        return

    # Nothing to do if it isn't a Windows Store Python distribution.
    if r"WindowsApps\PythonSoftwareFoundation" not in sys.base_prefix:
        return

    paths = _installation.for_version(version).windows_store_dll_dirs
    if paths is None:
        LOG.warning(
            f"Mechanical version {version} is not recognized. DLL search paths have not been "
            "configured for the Windows Store Python workaround. You may encounter dependency "
            "issues when loading Mechanical."
        )
        return

    # Add each path to the DLL search path
    for path in paths:
        os.add_dll_directory(str(path))  # type: ignore


def __set_environment(version: int) -> None:
    """Set environment variables to configure embedding."""
    limitations = Limitations(version)
    if os.name == "nt":  # pragma: no cover
        if limitations.unoptimized_startup:
            os.environ["MECHANICAL_STARTUP_UNOPTIMIZED"] = "1"

    # Set an environment variable to use the custom CLR host
    # for embedding.
    if limitations.clr_host_lite_opt_in:
        if "PYMECHANICAL_NO_CLR_HOST_LITE" not in os.environ:
            os.environ["ANSYS_MECHANICAL_EMBEDDING_CLR_HOST"] = "1"
    if Capabilities(version).clr_host_lite_default:
        if "PYMECHANICAL_NO_CLR_HOST_LITE" in os.environ:
            os.environ["ANSYS_MECHANICAL_EMBEDDING_CLR_HOST"] = "0"


def __check_for_mechanical_env():
    """Embedding in linux platform must use mechanical-env."""
    if platform.system() == "Linux" and os.environ.get("PYMECHANICAL_EMBEDDING") != "TRUE":
        raise RuntimeError(
            "On linux, embedding an instance of the Mechanical process using "
            "the App class requires running python inside of a Mechanical environment. "
            "Use the `mechanical-env` script to do this. For more information, refer to:"
            "https://mechanical.docs.pyansys.com/version/stable/"
            "getting_started/running_mechanical.html#embed-a-mechanical-instance"
        )


def __is_lib_loaded(libname: str):  # pragma: no cover
    """Return whether a library is loaded."""
    import ctypes

    rtld_noload = 4
    try:
        ctypes.CDLL(libname, rtld_noload)
    except OSError:
        return False
    return True


def __check_loaded_libs(version: int | None = None):  # pragma: no cover
    """Ensure that incompatible libraries aren't loaded prior to PyMechanical load."""
    if platform.system() != "Linux":
        return

    if version is None or not Limitations(version).libx11_shutdown_crash:
        return

    # For 2025 R1, PyMechanical will crash on shutdown if libX11.so is already loaded
    # before starting Mechanical
    if __is_lib_loaded("libX11.so"):
        LOG.warning(
            "libX11.so is loaded prior to initializing the Embedded Instance of Mechanical.\
                      Python will crash on shutdown..."
        )


def initialize(version: int | None = None):
    """Initialize Mechanical embedding."""
    global INITIALIZED_VERSION
    if version is None:
        version = _get_latest_default_version()

    version = __check_for_supported_version(version=version)

    if INITIALIZED_VERSION is not None:
        if INITIALIZED_VERSION != version:
            raise ValueError(
                f"Initialized version {INITIALIZED_VERSION} "
                f"does not match the expected version {version}."
            )
        return INITIALIZED_VERSION

    __check_python_interpreter_architecture()  # blocks 32 bit python
    __check_for_mechanical_env()  # checks for mechanical-env in linux embedding

    __set_environment(version)

    __windows_store_workaround(version)

    __check_loaded_libs(version)

    __workaround_material_server(version)

    # need to add system path in order to import the assembly with the resolver
    __add_sys_path(version)

    # Check if 'pythonnet' is installed... and if so, throw warning
    try:
        distribution("pythonnet")
        warnings.warn(
            "The pythonnet package was found in your environment "
            "which interferes with the ansys-pythonnet package. "
            "Some APIs may not work due to pythonnet being installed.\n\n"
            "For using PyMechanical, we recommend you do the following:\n"
            "1. Uninstall your existing pythonnet package: pip uninstall pythonnet\n"
            "2. Install the ansys-pythonnet package: pip install --upgrade "
            "--force-reinstall ansys-pythonnet\n",
            stacklevel=2,
        )
    except ModuleNotFoundError:
        pass

    # load the CLR with mono that is shipped with the unified ansys installer
    load_clr(str(_installation.for_version(version).root))

    # attach the resolver
    resolve(version)

    INITIALIZED_VERSION = version
    return version
