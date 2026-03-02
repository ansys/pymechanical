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
"""Cli for finding mechanical installation."""

import os
from pathlib import Path
import sys

import ansys.tools.common.path as atp
import click


@click.command()
@click.help_option("--help", "-h")
@click.option(
    "-r",
    "--version",
    default=None,
    type=int,
    help='Ansys version number, such as "242" or "241".\
         If a version number is not specified, it uses the default from \
            ansys-tools-path.',
)
@click.option(
    "-p",
    "--path",
    default=None,
    type=click.Path(exists=True, file_okay=False),
    help="Optional path to the Ansys installation directory. "
    "If provided, this path will be used instead of the default.",
)
def cli(version: int, path: str | None = None) -> tuple[int, str]:
    """
    Use the CLI tool to find the Mechanical version and location.

    Parameters
    ----------
    version: int
        Ansys version number.
    path: str, optional
        Optional path to the Ansys installation directory.
        eg: "usr/ansys_inc/v251/"

    Example
    -------
    Get the version and location of the installation directory.

    >>> find-mechanical -r 251
    >>> find-mechanical -p "usr/ansys_inc/v251/"
    """
    # Priority of finding the Mechanical version and path:
    # 1. If both path and version are provided, check if they match and use them
    # 2. If only path is provided, determine the version from the path
    # 3. If neither is provided, check environment variables for AWP_ROOT
    # 3. If multiple AWP_ROOT variables are found, use the highest version
    # 4. If no AWP_ROOT variables are found, use the default from ansys-tools-path
    # 5. If the default path is not found, check saved ansys path from config file
    if path and version:
        if version != atp.version_from_path("mechanical", path):
            raise click.BadParameter(
                f"The provided path {path} does not match the specified version {version}."
            )
        print(version, str(Path(path) / "aisol"))
        sys.exit(0)
    if path and not version:
        _version_from_given_path = atp.version_from_path("mechanical", path)
        print(_version_from_given_path, str(Path(path) / "aisol"))
        sys.exit(0)

    awp_roots = [value for key, value in os.environ.items() if key.startswith("AWP_ROOT")]

    if awp_roots:
        versions_found = []
        for awp_root in awp_roots:
            vfolder = Path(awp_root).name
            _version = vfolder.lstrip("v")
            versions_found.append(int(_version))
        if version in versions_found:
            print(version, str(Path(os.environ[f"AWP_ROOT{version}"]) / "aisol"))
            sys.exit(0)
        if versions_found:
            latest_version = max(versions_found)
            print(latest_version, str(Path(os.environ[f"AWP_ROOT{latest_version}"]) / "aisol"))
            sys.exit(0)

    # Use ansys-tools-path
    _exe = atp.get_mechanical_path(allow_input=False, version=version)
    _version = atp.version_from_path("mechanical", _exe)

    _path = str(Path(_exe).parent)
    print(_version, _path)

    sys.exit(0)
