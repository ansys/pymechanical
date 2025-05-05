# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Launch embedded instance."""
import click

import ansys.mechanical.core as pymechanical
from ansys.mechanical.core.embedding.app import is_initialized


def launch_app(version, private_appdata, test_not_initialized, debug):
    """Launch embedded instance of app."""
    if debug:
        import logging

        from ansys.mechanical.core.embedding.logger import Configuration

        Configuration.configure(level=logging.DEBUG, to_stdout=True, base_directory=None)

    if test_not_initialized:
        init_msg = "The app is initialized" if is_initialized() else "The app is not initialized"
        print(init_msg)

    app = pymechanical.App(
        version=int(version),
        private_appdata=private_appdata,
        copy_profile=False,
        globals=globals(),
    )

    return app


def set_showtriad(version, private_appdata, test_not_initialized, debug, value):
    """Launch embedded instance of app & set ShowTriad to False."""
    app = launch_app(version, private_appdata, test_not_initialized, debug)
    ExtAPI.Graphics.ViewOptions.ShowTriad = value
    app.close()


def print_showtriad(version, private_appdata, test_not_initialized, debug):
    """Return ShowTriad value."""
    app = launch_app(version, private_appdata, test_not_initialized, debug)
    print("ShowTriad value is " + str(app.ExtAPI.Graphics.ViewOptions.ShowTriad))
    app.close()


@click.command()
@click.help_option("--help", "-h")
@click.option(
    "--version",
    default=251,
    type=int,
    help="Mechanical version. For example, 251.",
)
@click.option(
    "--action",
    default="Run",
    type=click.Choice(["Set", "Run", "Reset"], case_sensitive=False),
    help=(
        'The action to perform on the app. Can be "Set", "Run", or "Reset". '
        '"Set" will set the ShowTriad value to False. '
        '"Run" will print the ShowTriad value. '
        '"Reset" will set the ShowTriad value to True.'
    ),
)
@click.option(
    "--private-appdata",
    default="False",
    type=str,
    help="Whether to use a private AppData folder when launching the app.",
)
@click.option(
    "--test_not_initialized",
    is_flag=True,
    default=False,
    help="Test if the app is initialized.",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Set the logging level to DEBUG and print to stdout.",
)
def test_embedded_app_cli(
    version: int, action: str, private_appdata: str, test_not_initialized: bool, debug: bool
):
    """CLI tool to run embedded instance of app.

    Parameters
    ----------
    version : int
        The Mechanical version. For example, 251.
    action : str
        The action to perform on the app. Can be "Set", "Run", or "Reset".
        "Set" will set the ShowTriad value to False.
        "Run" will print the ShowTriad value.
        "Reset" will set the ShowTriad value to True.
    private_appdata : str
        Whether to use a private AppData folder when launching the app.
    test_not_initialized : bool
        Test if the app is initialized.
    debug : bool
        Set the logging level to DEBUG and print to stdout.
    """
    private_appdata = private_appdata == "True"

    if action == "Set":
        set_showtriad(version, private_appdata, test_not_initialized, debug, False)
    elif action == "Run":
        print_showtriad(version, private_appdata, test_not_initialized, debug)
    elif action == "Reset":
        set_showtriad(version, private_appdata, test_not_initialized, debug, True)
    else:
        launch_app(version, private_appdata, test_not_initialized, debug)


if __name__ == "__main__":
    test_embedded_app_cli()
