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
"""Test for Miscellaneous Functions."""

import pytest

import ansys.mechanical.core.misc as misc


@pytest.mark.remote_session_launch
def test_valid_start_instance():
    """Test for valid start instance."""
    assert misc.check_valid_start_instance("true")

    assert not misc.check_valid_start_instance("false")

    assert misc.check_valid_start_instance("True")

    assert not misc.check_valid_start_instance("False")

    with pytest.raises(ValueError):
        misc.check_valid_start_instance([])

    with pytest.raises(ValueError):
        misc.check_valid_start_instance("hello")


@pytest.mark.remote_session_launch
def test_is_float():
    """Test for is_float function."""
    assert misc.is_float("1.3")

    assert not misc.is_float("hello")
