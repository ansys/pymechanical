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
import argparse

import ansys.mechanical.core as pymechanical
from ansys.mechanical.core.embedding.app import is_initialized


def launch_app(args):
    """Launch embedded instance of app."""
    if args.debug:
        import logging

        from ansys.mechanical.core.embedding.logger import Configuration

        Configuration.configure(level=logging.DEBUG, to_stdout=True, base_directory=None)

    if args.test_not_initialized:
        init_msg = "The app is initialized" if is_initialized() else "The app is not initialized"
        print(init_msg)

    app = pymechanical.App(
        version=int(args.version),
        private_appdata=args.private_appdata,
        copy_profile=True,
        globals=globals(),
    )

    return app


def set_showtriad(args, value):
    """Launch embedded instance of app & set ShowTriad to False."""
    app = launch_app(args)
    ExtAPI.Graphics.ViewOptions.ShowTriad = value
    app.close()


def print_showtriad(args):
    """Return ShowTriad value."""
    app = launch_app(args)
    print("ShowTriad value is " + str(app.ExtAPI.Graphics.ViewOptions.ShowTriad))
    app.close()


if __name__ == "__main__":
    # Set up argparse for command line arguments from subprocess.
    parser = argparse.ArgumentParser(description="Launch embedded instance of app.")
    parser.add_argument("--version", type=str, help="Mechanical version")
    parser.add_argument("--private_appdata", type=str, help="Private appdata")
    parser.add_argument("--action", type=str, help="Action to perform")
    parser.add_argument("--debug", action="store_true")  # 'store_true' implies default=False
    parser.add_argument(
        "--test_not_initialized", action="store_true"
    )  # 'store_true' implies default=False

    # Get and set args from subprocess
    args = parser.parse_args()
    action = args.action

    args.private_appdata = args.private_appdata == "True"

    if action == "Set":
        set_showtriad(args, False)
    elif action == "Run":
        print_showtriad(args)
    elif action == "Reset":
        set_showtriad(args, True)
    else:
        launch_app(args)
