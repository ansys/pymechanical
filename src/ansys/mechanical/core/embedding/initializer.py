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

"""Initializer for Mechanical embedding. Sets up paths and resolvers."""
from importlib.metadata import distribution
import os
from pathlib import Path
import platform
import sys
import warnings

import ansys.tools.path as atp

from ansys.mechanical.core.embedding.loader import load_clr
from ansys.mechanical.core.embedding.resolver import resolve

INITIALIZED_VERSION = None
"""Constant for the initialized version."""

SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS_WINDOWS = {242: "2024R2", 241: "2024R1", 232: "2023R2"}
"""Supported Mechanical embedding versions on Windows."""


def __add_sys_path(version: int) -> str:
    install_path = Path(os.environ[f"AWP_ROOT{version}"])
    platform_string = "winx64" if os.name == "nt" else "linx64"
    bin_path = install_path / "aisol" / "bin" / platform_string
    sys.path.append(str(bin_path.resolve()))


def __workaround_material_server(version: int) -> None:
    """Workaround material server bug in 2024 R1.

    A REST server is used as a backend for the material model GUI.
    In 2024 R1, this GUI is used even in batch mode. The server
    starts by default on a background thread, which may lead to
    a race condition on shutdown.
    """
    if version in [241]:
        os.environ["ENGRDATA_SERVER_SERIAL"] = "1"


def _get_default_linux_version() -> int:
    """Try to get the active linux version from the environment.

    On linux, embedding is only possible by setting environment variables before starting python.
    The version will then be fixed  to a specific version, based on those env vars.
    The documented way to set those variables is to run python using the ``mechanical-env`` script,
    which can be used after installing the ``ansys-mechanical-env`` package with this command:
    ``pip install ansys-mechanical-env``. The script takes user input of a version. If the user
    does not provide a version, the ``find_mechanical()`` function from the ``ansys-tools-path``
    package is used to find a version of Mechanical.
    """
    supported_versions = [232, 241, 242]
    awp_roots = {ver: os.environ.get(f"AWP_ROOT{ver}", "") for ver in supported_versions}
    installed_versions = {
        ver: path for ver, path in awp_roots.items() if path and os.path.isdir(path)
    }
    assert len(installed_versions) == 1, "multiple AWP_ROOT environment variables found!"
    return next(iter(installed_versions))


def _get_default_version() -> int:
    if os.name == "posix":
        return _get_default_linux_version()

    if os.name != "nt":  # pragma: no cover
        raise Exception("Unexpected platform!")

    _, version = atp.find_mechanical(
        supported_versions=SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS_WINDOWS
    )

    # version is of the form 23.2
    int_version = int(str(version).replace(".", ""))
    return int_version


def __check_python_interpreter_architecture():
    """Embedding support only 64 bit architecture."""
    if platform.architecture()[0] != "64bit":
        raise Exception("Mechanical Embedding requires a 64-bit Python environment.")


def __check_for_mechanical_env():
    """Embedding in linux platform must use mechanical-env."""
    if platform.system() == "Linux" and os.environ.get("PYMECHANICAL_EMBEDDING") != "TRUE":
        raise Exception(
            "On linux, embedding an instance of the Mechanical process using"
            "the App class requires running python inside of a Mechanical environment."
            "Use the `mechanical-env` script to do this. For more information, refer to:"
            "https://mechanical.docs.pyansys.com/version/stable/"
            "getting_started/running_mechanical.html#embed-a-mechanical-instance"
        )


def initialize(version: int = None):
    """Initialize Mechanical embedding."""
    __check_python_interpreter_architecture()  # blocks 32 bit python
    __check_for_mechanical_env()  # checks for mechanical-env in linux embedding

    global INITIALIZED_VERSION
    if INITIALIZED_VERSION != None:
        assert INITIALIZED_VERSION == version
        return

    if version == None:
        version = _get_default_version()

    INITIALIZED_VERSION = version

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
    load_clr(os.environ[f"AWP_ROOT{version}"])

    # attach the resolver
    resolve(version)

    return version
