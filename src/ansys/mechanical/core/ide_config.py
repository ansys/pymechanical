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

"""Convenience CLI to run mechanical."""

import json
import os
from pathlib import Path
import re
import site
import sys
import warnings

import ansys.tools.common.path as atp
import click


def get_stubs_location():
    """Find the ansys-mechanical-stubs installation location in site-packages.

    Returns
    -------
    pathlib.Path
        The path to the ansys-mechanical-stubs installation in site-packages.
    """
    site_packages = site.getsitepackages()
    prefix_path = sys.prefix.replace("\\", "\\\\")
    site_packages_regex = re.compile(f"{prefix_path}.*site-packages$")
    site_packages_paths = list(filter(site_packages_regex.match, site_packages))

    if len(site_packages_paths) >= 1:
        # Get the stubs location
        stubs_location = Path(site_packages_paths[0]) / "ansys" / "mechanical" / "stubs"
        return stubs_location

    raise Exception("Could not retrieve the location of the ansys-mechanical-stubs package.")


def get_stubs_versions(stubs_location: Path):
    """Retrieve the revision numbers in ansys-mechanical-stubs.

    Parameters
    ----------
    pathlib.Path
        The path to the ansys-mechanical-stubs installation in site-packages.

    Returns
    -------
    list
        The list containing minimum and maximum versions in the ansys-mechanical-stubs package.
    """
    # Get revision numbers in stubs folder
    revns = [
        int(revision.name[1:])
        for revision in stubs_location.iterdir()
        if revision.is_dir() and revision.name.startswith("v")
    ]
    return revns


def _vscode_impl(
    target: str = "user",
    revision: int = None,
):
    """Get the IDE configuration for autocomplete in VS Code.

    Parameters
    ----------
    target: str
        The type of settings to update. Either "user" or "workspace" in VS Code.
        By default, it's ``user``.
    revision: int
        The Mechanical revision number. For example, "252".
        If unspecified, it finds the default Mechanical version from ansys-tools-path.
    """
    # Update the user or workspace settings
    settings_json = "the settings.json file"
    if target == "user":
        # Get the path to the user's settings.json file depending on the platform
        if "win" in sys.platform:
            settings_json = (
                Path(os.environ.get("APPDATA")) / "Code" / "User" / "settings.json"
            )  # pragma: no cover
        elif "lin" in sys.platform:
            settings_json = (
                Path(os.environ.get("HOME")) / ".config" / "Code" / "User" / "settings.json"
            )
    elif target == "workspace":
        # Get the current working directory
        current_dir = Path.cwd()
        # Get the path to the settings.json file based on the git root & .vscode folder
        settings_json = current_dir / ".vscode" / "settings.json"

    # Location where the stubs are installed -> .venv/Lib/site-packages, for example
    stubs_location = get_stubs_location() / f"v{revision}"

    # The settings to add to settings.json for autocomplete to work
    settings_json_data = {
        "python.autoComplete.extraPaths": [str(stubs_location)],
        "python.analysis.extraPaths": [str(stubs_location)],
    }
    # Pretty print dictionary
    pretty_dict = json.dumps(settings_json_data, indent=4)

    print(f"Update {settings_json} with the following information:\n")

    if target == "workspace":
        print(
            "Note: Please ensure the .vscode folder is in the root of your project or repository.\n"
        )

    print(pretty_dict)


def _cli_impl(
    ide: str = "vscode",
    target: str = "user",
    revision: int = None,
):
    """Provide the user with the path to the settings.json file and IDE settings.

    Parameters
    ----------
    ide: str
        The IDE to set up autocomplete settings. By default, it's ``vscode``.
    target: str
        The type of settings to update. Either "user" or "workspace" in VS Code.
        By default, it's ``user``.
    revision: int
        The Mechanical revision number. For example, "252".
        If unspecified, it finds the default Mechanical version from ansys-tools-path.
    """
    # Get the ansys-mechanical-stubs install location
    stubs_location = get_stubs_location()
    # Get all revision numbers available in ansys-mechanical-stubs
    revns = get_stubs_versions(stubs_location)

    # Check if the user revision number is less or greater than the min and max revisions
    # in the ansys-mechanical-stubs package location
    if revision < min(revns):
        raise Exception(f"PyMechanical Stubs are not available for {revision}")
    elif revision > max(revns):
        warnings.warn(
            f"PyMechanical Stubs are not available for {revision}. Using {max(revns)} instead.",
            stacklevel=2,
        )
        revision = max(revns)

    # Check the IDE and raise an exception if it's not VS Code
    if ide != "vscode":
        raise Exception(f"{ide} is not supported at the moment.")

    return _vscode_impl(target, revision)


@click.command()
@click.help_option("--help", "-h")
@click.option(
    "--ide",
    default="vscode",
    type=str,
    help="The IDE being used. By default, it's ``vscode``.",
)
@click.option(
    "--target",
    default="user",
    type=str,
    help="The type of settings to update - either ``user`` or ``workspace`` settings in VS Code.",
)
@click.option(
    "--revision",
    default=None,
    type=int,
    help='The Mechanical revision number, e.g. "252" or "251". If unspecified,\
it finds and uses the default version from ansys-tools-path.',
)
def cli(ide: str, target: str, revision: int) -> None:
    """CLI tool to update settings.json files for autocomplete with ansys-mechanical-stubs.

    Parameters
    ----------
    ide: str
        The IDE to set up autocomplete settings. By default, it's ``vscode``.
    target: str
        The type of settings to update. Either "user" or "workspace" in VS Code.
        By default, it's ``user``.
    revision: int
        The Mechanical revision number. For example, "252".
        If unspecified, it finds the default Mechanical version from ansys-tools-path.

    Usage
    -----
    The following example demonstrates the main use of this tool:

        $ ansys-mechanical-ideconfig --ide vscode --target user --revision 252

    """
    if not revision:
        exe = atp.get_mechanical_path(allow_input=False, version=revision)
        version = atp.version_from_path("mechanical", exe)
    else:
        version = revision

    return _cli_impl(
        ide,
        target,
        version,
    )
