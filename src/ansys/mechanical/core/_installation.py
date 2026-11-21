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

from ansys.mechanical.core._capabilities import Capabilities

_WINDOWS_STORE_TP_DIRS = {
    242: (
        "IntelCompiler/2023.1.0/winx64",
        "IntelMKL/2023.1.0/winx64",
        "hdf5/1.12.2/winx64",
        "qt/5.15.16/winx64/bin",
    ),
    251: (
        "IntelCompiler/2023.1.0/winx64",
        "IntelMKL/2023.1.0/winx64",
        "hdf5/1.12.2/winx64",
        "qt/5.15.17/winx64/bin",
    ),
    252: (
        "IntelCompiler/2023.1.0/winx64",
        "IntelMKL/2024.2.3/winx64",
        "hdf5/winx64",
        "qt/5.15.18/winx64/bin",
    ),
    261: (
        "IntelCompiler/2023.1.0/winx64",
        "IntelMKL/2024.2.3/winx64",
        "hdf5/winx64",
        "qt/5.15.19/winx64/bin",
    ),
    # 271 might change in the future.
    271: (
        "IntelCompiler/2025.3.2/winx64",
        "IntelMKL/2024.2.3/winx64",
        "hdf5/winx64",
        "libtorch/2.11/winx64/lib",
        "qt/6.8.8/winx64/bin",
    ),
}


def _platform_folder() -> str:
    return "winx64" if os.name == "nt" else "linx64"


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
        return self.aisol / "bin" / _platform_folder()

    @property
    def dll_dir(self) -> Path:
        """Platform-specific folder holding the Mechanical shared libraries.

        Examples
        --------
        >>> dll_dir = Installation(261, Path("/ansys_inc/v261")).dll_dir
        >>> dll_dir.parent.as_posix()
        '/ansys_inc/v261/aisol/dll'
        >>> dll_dir.name in ("winx64", "linx64")
        True
        """
        return self.aisol / "dll" / _platform_folder()

    @property
    def act_libraries_dir(self) -> Path:
        """Folder holding the Mechanical Python libraries of the ACT add-in.

        Examples
        --------
        >>> Installation(261, Path("/ansys_inc/v261")).act_libraries_dir.as_posix()
        '/ansys_inc/v261/Addins/ACT/libraries/Mechanical'
        """
        return self.root / "Addins" / "ACT" / "libraries" / "Mechanical"

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

    @property
    def capabilities(self) -> Capabilities:
        """Capabilities of this installation's version.

        Examples
        --------
        >>> Installation(261, Path("/ansys_inc/v261")).capabilities.interactive
        True
        """
        return Capabilities(self.version)

    @property
    def windows_store_dll_dirs(self) -> list[Path] | None:
        """Folders Windows Store Python must add to its DLL search path.

        Windows Store Python doesn't search ``PATH`` for DLLs, so these folders are
        added explicitly. ``None`` means the version isn't recognized.

        Examples
        --------
        >>> dirs = Installation(261, Path("/ansys_inc/v261")).windows_store_dll_dirs
        >>> dirs[1].as_posix()
        '/ansys_inc/v261/Framework/bin/Win64'
        >>> Installation(999, Path("/ansys_inc/v999")).windows_store_dll_dirs is None
        True
        """
        tp_dirs = _WINDOWS_STORE_TP_DIRS.get(self.version)
        if tp_dirs is None:
            return None
        return [
            self.bin_dir,
            self.root / "Framework" / "bin" / "Win64",
            *(self.root / "tp" / tp_dir for tp_dir in tp_dirs),
        ]


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
    discovered = installed(environ).get(version)
    if discovered is None:
        raise RuntimeError(
            f"AWP_ROOT{version} environment variable not found. Set it to the Mechanical "
            f"{version} installation, such as /path/to/ansys_inc/v{version}."
        )
    return discovered


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


def from_environment(
    version: int | None = None, environ: Mapping[str, str] | None = None
) -> Installation | None:
    """Find a Mechanical installation from ``AWP_ROOT*`` variables only.

    The search order is ``AWP_ROOT<version>``, then the requested version from the
    environment, then the latest version from the environment.

    Parameters
    ----------
    version : int, default: None
        Preferred Mechanical version.
    environ : Mapping[str, str], default: None
        Environment to read. ``None`` reads ``os.environ``.

    Returns
    -------
    Installation or None
        Installation found, or ``None`` if no ``AWP_ROOT*`` variable is usable.

    Examples
    --------
    >>> from_environment(242, {"AWP_ROOT261": "/ansys_inc/v261"}).version
    261
    >>> from_environment(261, {}) is None
    True
    """
    environ = os.environ if environ is None else environ
    if version is not None and f"AWP_ROOT{version}" in environ:
        return for_version(version, environ)
    by_version = installed(environ)
    if version in by_version:
        return by_version[version]
    if by_version:
        return by_version[max(by_version)]
    return None


def from_path(path: str | os.PathLike[str]) -> Installation:
    """Get the installation that contains a path.

    The root is the folder above ``aisol`` when ``path`` is inside it. Otherwise,
    the root is ``path`` itself for an existing folder, or its parent for a file.

    Parameters
    ----------
    path : str or os.PathLike
        Mechanical executable, or a folder of the installation.

    Returns
    -------
    Installation
        Installation that contains ``path``.

    Raises
    ------
    RuntimeError
        If the version can't be read from ``path``.

    Examples
    --------
    >>> installation = from_path("/ansys_inc/v261/aisol/.workbench")
    >>> installation.version, installation.root.as_posix()
    (261, '/ansys_inc/v261')
    """
    path = Path(path)
    aisol = next((p for p in (path, *path.parents) if p.name.lower() == "aisol"), None)
    if aisol is not None:
        root = aisol.parent
    elif path.is_dir():
        root = path
    else:
        root = path.parent
    return Installation(atp.version_from_path("mechanical", str(path)), root)


def _locate(version: int | None, locator: Callable[..., str | None] | None) -> Installation | None:
    exe = (locator or atp.get_mechanical_path)(allow_input=False, version=version)
    return from_path(exe) if exe else None


def find(
    version: int | None = None,
    environ: Mapping[str, str] | None = None,
    locator: Callable[..., str | None] | None = None,
    prefer_locator: bool = False,
) -> Installation | None:
    """Find a Mechanical installation, preferring ``AWP_ROOT*`` variables.

    The search order is :func:`from_environment`, then ``locator``.
    With ``prefer_locator``, ``locator`` comes first and the environment is the fallback.
    The root of a located executable follows :func:`from_path`.

    Parameters
    ----------
    version : int, default: None
        Preferred Mechanical version.
    environ : Mapping[str, str], default: None
        Environment to read. ``None`` reads ``os.environ``.
    locator : Callable, default: None
        Called as ``locator(allow_input=False, version=version)`` to get the
        executable path. ``None`` uses ``ansys.tools.common.path.get_mechanical_path``,
        which honors a path saved with ``ansys-tools-path``.
    prefer_locator : bool, default: False
        Whether ``locator`` takes precedence over the ``AWP_ROOT*`` variables.

    Returns
    -------
    Installation or None
        Installation found, or ``None`` if there is none.

    Examples
    --------
    >>> find(242, {"AWP_ROOT261": "/ansys_inc/v261"}).version
    261
    """
    if prefer_locator:
        return _locate(version, locator) or from_environment(version, environ)
    return from_environment(version, environ) or _locate(version, locator)
