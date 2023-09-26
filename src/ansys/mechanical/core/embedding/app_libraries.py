# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
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

from ansys.tools.path.path import _get_unified_install_base_for_version


def add_mechanical_python_libraries(version: int):
    """Add the Mechanical libraries path to sys.path."""
    install, _ = _get_unified_install_base_for_version(version)
    location = os.path.join(install, "Addins", "ACT", "libraries", "Mechanical")
    sys.path.append(location)
