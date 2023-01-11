"""Initializer for Mechanical embedding. Sets up paths and resolvers."""
import os
from pathlib import Path
import sys

from ansys.mechanical.core.embedding.loader import load_clr
from ansys.mechanical.core.embedding.resolver import resolve

INITIALIZED_VERSION = None


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


def initialize(version):
    """Initialize Mechanical embedding."""
    global INITIALIZED_VERSION
    if INITIALIZED_VERSION != None:
        assert INITIALIZED_VERSION == version
        return
    INITIALIZED_VERSION = version

    __disable_sec()

    # need to add system path in order to import the assembly with the resolver
    __add_sys_path(version)

    # load the CLR with mono that is shipped with the unified ansys installer
    load_clr(os.environ[f"AWP_ROOT{version}"])

    # attach the resolver
    resolve(version)
