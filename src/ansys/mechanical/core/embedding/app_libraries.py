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

"""System to add python libraries shipped with mechanical to the path.

Mechanical ships some pure Python modules that can be imported within
Mechanical's console window. These modules are located in

`/path/to/Ansys Inc/vNnn/Addins/ACT/libraries/Mechanical`

For example, the following files can be found there:

- ansys.py
- chart.py
- comhelper.py
- dialogs.py
- engineeringdata.py
- graphics.py
- materials.py
- mechanical.py
- units.py
- wbjn.py

Some (but not all) of these are usable from within an embedded instance
of Mechanical in Python.

This module provides a method to add that path to `sys.path` so that they
can be imported with the `import` statement.

"""

import os
import sys
import warnings

from ansys.tools.path import get_mechanical_path

from ansys.mechanical.core.embedding.app import App


def add_mechanical_python_libraries(app_or_version):
    """Add the Mechanical libraries path to sys.path."""
    installdir = []
    if isinstance(app_or_version, int):
        warnings.warn(
            "Passing version to add_mechanical_python_libraries() is deprecated."
            "Please pass an instance of App() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        exe = get_mechanical_path(allow_input=False, version=app_or_version)
        while os.path.basename(exe) != f"v{app_or_version}":
            exe = os.path.dirname(exe)
        installdir.append(exe)
    elif isinstance(app_or_version, App):
        installdir.append(os.environ[f"AWP_ROOT{app_or_version.version}"])
    else:
        raise ValueError(f"Invalid input: expected an integer (version) or an instance of App().")

    location = os.path.join(installdir[0], "Addins", "ACT", "libraries", "Mechanical")
    sys.path.append(location)
