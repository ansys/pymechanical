# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
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
import sys

import ansys.mechanical.core as pymechanical


def launch_app(version, private_appdata):
    """Launch embedded instance of app."""
    app = pymechanical.App(version=version, private_appdata=private_appdata)
    return app


def set_showtriad(version, appdata_option, value):
    """Launch embedded instance of app & set ShowTriad to False."""
    app = launch_app(version, appdata_option)
    app.ExtAPI.Graphics.ViewOptions.ShowTriad = value
    app.close()


def print_showtriad(version, appdata_option):
    """Return ShowTriad value."""
    app = launch_app(version, appdata_option)
    print("ShowTriad value is " + str(app.ExtAPI.Graphics.ViewOptions.ShowTriad))
    app.close()
    

def reset_showtriad(version, appdata_option):
    """Reset ShowTriad value."""
    app = launch_app(version, appdata_option)
    app.ExtAPI.Graphics.ViewOptions.Reset
    app.close()


if __name__ == "__main__":
    version = int(sys.argv[1])
    if len(sys.argv) == 2:
        launch_app(version, False)
        sys.exit(0)

    appdata_option = sys.argv[2]
    action = sys.argv[3]

    private_appdata = appdata_option == "True"
    if action == "Set":
        set_showtriad(version, private_appdata, False)
    elif action == "Run":
        print_showtriad(version, private_appdata)
    elif action == "Reset":
        reset_showtriad(version, appdata_option)
