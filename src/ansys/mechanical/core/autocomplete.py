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

"""Convenience CLI to run mechanical."""

import json
import os
from pathlib import Path
import re
import sys
import sysconfig

import ansys.tools.path as atp
import click


# bonus, see if this works: "from ansys.mechanical.core.stubs_importer import *"
def valid_json(json_file):
    """Check if the settings.json file can be loaded.

    Parameters
    ----------
    json_file: pathlib.Path
        The path to the settings.json file.

    Returns
    -------
    bool
        ``True`` if the JSON file can be loaded.
        ``False`` if the JSON file cannot be loaded due to invalid syntax.
    """
    # If the JSON file has invalid format, return False
    with open(json_file, "r") as file:
        try:
            data = json.load(file)
            return True
        except json.decoder.JSONDecodeError:
            return False


def _cli_impl(
    ide: str = None,
    location: str = None,
    revision: int = None,
):
    if ide != "vscode":
        raise Exception(f"{ide} is not a supported IDE at the moment.")

    if location == "user":
        if "win" in sys.platform:
            settings_json = Path(os.environ.get("APPDATA")) / "Code" / "User" / "settings.json"
        elif "lin" in sys.platform:
            settings_json = (
                Path(os.environ.get("HOME")) / ".config" / "Code" / "User" / "settings.json"
            )

    elif location == "workspace":
        # C:/Users/kmcadams/pyansys/pymechanical/.vscode/settings.json
        settings_json = ""
        raise Exception(f"Cannot update settings.json in the {location} settings yet.")

    stubs_location = (
        Path(sysconfig.get_paths()["purelib"]) / "ansys" / "mechanical" / "stubs" / f"v{revision}"
    )
    last_comma = r"\,(?!\s*?[\{\[\"\'\w])"
    valid = valid_json(settings_json)

    # If the JSON isn't valid
    if not valid:
        # Open the JSON, delete the trailing comma
        with open(settings_json, "r") as file:
            data = file.readlines()
            data_joined = "".join(data)
            data_joined = re.sub(last_comma, "", data_joined)

        # Overwrite the JSON without the trailing comma
        with open(settings_json, "w") as file:
            file.write(data_joined)

    # Open the properly formatted JSON file
    with open(settings_json, "r") as file:
        data = json.load(file)

    settings_json_data = {
        "python.autoComplete.extraPaths": [str(stubs_location)],
        "python.analysis.extraPaths": [str(stubs_location)],
    }

    # Combine the existing JSON with the autocomplete paths
    combined_dict = {**data, **settings_json_data}

    # Write the updated data back to the file
    with open(settings_json, "w") as file:
        json.dump(combined_dict, file, indent=4)


@click.command()
@click.help_option("--help", "-h")
@click.option(
    "--ide",
    default="vscode",
    type=str,
    help="The IDE being used.",
)
@click.option(
    "--location",
    default="user",
    type=str,
    help="Whether to update the settings.json file on the workspace or user level.",
)
@click.option(
    "--revision",
    default=None,
    type=int,
    help='Ansys Revision number, e.g. "242" or "241". If none is specified\
, uses the default from ansys-tools-path',
)
def cli(ide: str, location: str, revision: int):
    """CLI tool to run mechanical.

    USAGE:

    The following example demonstrates the main use of this tool:

        $ ansys-mechanical-autocomplete --ide vscode --location user --revision 242

    """
    exe = atp.get_mechanical_path(allow_input=False, version=revision)
    version = atp.version_from_path("mechanical", exe)

    return _cli_impl(
        ide,
        location,
        version,
    )
