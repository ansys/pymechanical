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

"""Launch embedded instance with build gallery flag."""
import sys

import ansys.mechanical.core as pymechanical


def launch_app(version):
    """Launch embedded instance of app."""
    # Configuration.configure(level=logging.DEBUG, to_stdout=True, base_directory=None)
    app = pymechanical.App(version=version)
    app.update_globals(globals())
    return app


if __name__ == "__main__":
    version = int(sys.argv[1])
    build_gallery_flag = sys.argv[2]
    app1 = launch_app(version)

    if build_gallery_flag == "True":

        pymechanical.BUILDING_GALLERY = True

        app2 = launch_app(version)
        print("Multiple App launched with building gallery flag on")

    elif build_gallery_flag == "False":
        app2 = launch_app(version)
