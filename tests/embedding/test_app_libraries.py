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

"""Testing app libraries"""

import os
from pathlib import Path
import sys

from ansys.tools.path import get_mechanical_path
import pytest

from ansys.mechanical.core.embedding import add_mechanical_python_libraries


@pytest.mark.embedding
def test_app_library(embedded_app):
    """Loads one of the libraries and calls a method."""
    _version = embedded_app.version

    # Test with version as input
    exe = Path(get_mechanical_path(_version))
    while exe.name != f"v{_version}":
        exe = exe.parent
    location = exe / "Addins" / "ACT" / "libraries" / "Mechanical"
    add_mechanical_python_libraries(_version)
    assert location in sys.path
    sys.path.remove(location)
    assert location not in sys.path

    # Test with app as input
    add_mechanical_python_libraries(embedded_app)
    install_dir = os.environ[f"AWP_ROOT{embedded_app.version}"]
    location = Path(install_dir) / "Addins" / "ACT" / "libraries" / "Mechanical"
    assert location in sys.path

    # import mechanical library and test a method

    from mechanical import AnalysisTypeName

    analysis_name = AnalysisTypeName(0)
    assert analysis_name == "Static"

    sys.path.remove(location)
    assert location not in sys.path

    # Test value error
    with pytest.raises(ValueError):
        add_mechanical_python_libraries(embedded_app.Model)
