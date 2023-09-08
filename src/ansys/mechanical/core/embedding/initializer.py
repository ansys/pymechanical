# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
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
import sys
import warnings

import ansys.tools.path as atp

from ansys.mechanical.core.embedding.loader import load_clr
from ansys.mechanical.core.embedding.resolver import resolve

INITIALIZED_VERSION = None
SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS_WINDOWS = {241: "2024R1", 232: "2023R2", 231: "2023R1"}


def __add_sys_path(version) -> str:
    install_path = Path(os.environ[f"AWP_ROOT{version}"])
    platform_string = "winx64" if os.name == "nt" else "linx64"
    bin_path = install_path / "aisol" / "bin" / platform_string
    sys.path.append(str(bin_path.resolve()))


def __disable_sec() -> None:
    """SEC is part of RSM and is unstable with embedding.

    I'm not going to debug why that is since we are planning to support
    DCS/REP in the future instead of RSM.
    """
    os.environ["ANSYS_MECHANICAL_EMBEDDING_NO_SEC"] = "1"


def _get_default_linux_version() -> int:
    """Try to get the active linux version from the environment.

    On linux, embedding is only possible by setting environment variables before starting python.
    The version will then be fixed  to a specific version, based on those env vars.
    The documented way to set those variables is to run python using the .workbench_lite script,
    which is distributed with the unified installer.
    That script doesn't quite set an env var to the version number, like 232, however it does set
    the env var AWP_ROOT{version} to some path. So here, we can search for which of those env
    vars are set assuming that the user did not set any others.
    To overcome this, if multiple are set, the user should set the version number in the
    constructor of the app, like app(version=232)
    """
    supported_versions = [232, 241]
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


def initialize(version=None):
    """Initialize Mechanical embedding."""
    global INITIALIZED_VERSION
    if INITIALIZED_VERSION != None:
        assert INITIALIZED_VERSION == version
        return

    if version == None:
        version = _get_default_version()

    INITIALIZED_VERSION = version

    __disable_sec()

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
