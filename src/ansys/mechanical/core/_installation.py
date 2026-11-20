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

"""Resolve which Mechanical installation to use and where its files live."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
import os
from pathlib import Path

import ansys.tools.common.path as atp


@dataclass(frozen=True)
class Installation:
    """Provides the version and root folder of a Mechanical installation.

    Examples
    --------
    Describe the Mechanical 2026 R1 installation.

    >>> installation = Installation(261, Path("/ansys_inc/v261"))
    >>> installation.version
    261
    """

    version: int
    root: Path

    @property
    def aisol(self) -> Path:
        """Mechanical application folder.

        Examples
        --------
        >>> Installation(261, Path("/ansys_inc/v261")).aisol.as_posix()
        '/ansys_inc/v261/aisol'
        """
        return self.root / "aisol"

    @property
    def bin_dir(self) -> Path:
        """Platform-specific folder holding the Mechanical binaries.

        The folder is ``winx64`` on Windows and ``linx64`` on Linux.

        Examples
        --------
        >>> bin_dir = Installation(261, Path("/ansys_inc/v261")).bin_dir
        >>> bin_dir.parent.as_posix()
        '/ansys_inc/v261/aisol/bin'
        >>> bin_dir.name in ("winx64", "linx64")
        True
        """
        return self.aisol / "bin" / ("winx64" if os.name == "nt" else "linx64")

    @property
    def executable(self) -> Path:
        """Mechanical executable file.

        The file is ``aisol/bin/winx64/AnsysWBU.exe`` on Windows and
        ``aisol/.workbench`` on Linux.

        Examples
        --------
        >>> Installation(261, Path("/ansys_inc/v261")).executable.name in (
        ...     "AnsysWBU.exe",
        ...     ".workbench",
        ... )
        True
        """
        if os.name == "nt":
            return self.bin_dir / "AnsysWBU.exe"
        return self.aisol / ".workbench"


def for_version(version: int, environ: Mapping[str, str] | None = None) -> Installation:
    """Get the installation for a version.

    ``AWP_ROOT<version>`` is used if set. Otherwise, the installation that
    :func:`installed` discovers for that version under any ``AWP_ROOT*`` name is used.

    Parameters
    ----------
    version : int
        Mechanical version, such as ``261``.
    environ : Mapping[str, str], default: None
        Environment to read. ``None`` reads ``os.environ``.

    Returns
    -------
    Installation
        Installation for ``version``.

    Raises
    ------
    RuntimeError
        If no ``AWP_ROOT*`` variable points to that version.

    Examples
    --------
    >>> for_version(261, {"AWP_ROOT261": "/ansys_inc/v261"}).root.as_posix()
    '/ansys_inc/v261'
    """
    environ = os.environ if environ is None else environ
    root = environ.get(f"AWP_ROOT{version}")
    if root is not None:
        return Installation(version, Path(root))
    found = installed(environ).get(version)
    if found is None:
        raise RuntimeError(
            f"AWP_ROOT{version} environment variable not found. Set it to the Mechanical "
            f"{version} installation, such as /path/to/ansys_inc/v{version}."
        )
    return found


def installed(environ: Mapping[str, str] | None = None) -> dict[int, Installation]:
    """Get the installations declared by ``AWP_ROOT*`` variables, keyed by version.

    The version comes from the ``v<version>`` name of the resolved root folder.
    Roots whose folder doesn't follow that pattern are skipped.

    Parameters
    ----------
    environ : Mapping[str, str], default: None
        Environment to read. ``None`` reads ``os.environ``.

    Returns
    -------
    dict[int, Installation]
        Installations keyed by version.

    Examples
    --------
    >>> sorted(installed({"AWP_ROOT252": "/ansys_inc/v252", "AWP_ROOT261": "/ansys_inc/v261"}))
    [252, 261]
    """
    environ = os.environ if environ is None else environ
    found = {}
    for key, value in environ.items():
        if not key.startswith("AWP_ROOT"):
            continue
        name = Path(value).resolve().name
        if name.startswith("v") and name[1:].isdigit():
            found[int(name[1:])] = Installation(int(name[1:]), Path(value))
    return found


def find(
    version: int | None = None,
    environ: Mapping[str, str] | None = None,
    locator: Callable[..., str | None] | None = None,
) -> Installation | None:
    """Find a Mechanical installation, preferring ``AWP_ROOT*`` variables.

    The search order is ``AWP_ROOT<version>``, then the requested version from the
    environment, then the latest version from the environment, then ``locator``.
    The root of a located executable is the folder above its ``aisol`` folder.

    Parameters
    ----------
    version : int, default: None
        Preferred Mechanical version.
    environ : Mapping[str, str], default: None
        Environment to read. ``None`` reads ``os.environ``.
    locator : Callable, default: None
        Called as ``locator(allow_input=False, version=version)`` to get the
        executable path when no ``AWP_ROOT*`` variable is usable. ``None`` uses
        ``ansys.tools.common.path.get_mechanical_path``.

    Returns
    -------
    Installation or None
        Installation found, or ``None`` if there is none.

    Examples
    --------
    >>> find(242, {"AWP_ROOT261": "/ansys_inc/v261"}).version
    261
    """
    environ = os.environ if environ is None else environ
    if version is not None and f"AWP_ROOT{version}" in environ:
        return for_version(version, environ)
    found = installed(environ)
    if version in found:
        return found[version]
    if found:
        return found[max(found)]
    exe = (locator or atp.get_mechanical_path)(allow_input=False, version=version)
    if not exe:
        return None
    exe_path = Path(exe)
    root = next((p.parent for p in exe_path.parents if p.name.lower() == "aisol"), exe_path.parent)
    return Installation(atp.version_from_path("mechanical", exe), root)
