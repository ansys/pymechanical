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

"""RSM test."""

import pytest


@pytest.mark.embedding
@pytest.mark.windows_only
def test_remote_solve(printer, embedded_app, graphics_test_mechdb_file):
    """Test to check My Computer Background solve"""
    printer(embedded_app)
    embedded_app.update_globals(globals())
    embedded_app.open(graphics_test_mechdb_file)
    solution = Model.Analyses[0].Solution
    solution.ClearGeneratedData()
    assert str(solution.Status) == "SolveRequired"

    printer("Test My Computer Solve")
    solution.Solve(True, "My Computer")
    assert str(solution.Status) == "Done"
    solution.ClearGeneratedData()
    assert str(solution.Status) == "SolveRequired"

    printer("Test My Computer Background Solve")
    solution.Solve(True, "My Computer, Background")
    solution.GetResults()
    assert str(solution.Status) == "Done"
