# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Tests for the known Mechanical defects of each version."""

from pathlib import Path

import pytest

from ansys.mechanical.core._installation import Installation
from ansys.mechanical.core._limitations import Limitations


@pytest.mark.embedding
@pytest.mark.parametrize(
    "name, versions",
    [
        ("material_server_race", (241,)),
        ("unoptimized_startup", (241, 242)),
        ("clr_host_lite_opt_in", (251, 252)),
        ("libx11_shutdown_crash", (251, 252, 261)),
    ],
)
def test_limitation_applies_to_affected_releases(name, versions):
    """Test that each limitation applies only to the releases that have the defect."""
    affected = [v for v in (241, 242, 251, 252, 261) if getattr(Limitations(v), name)]

    assert affected == list(versions)


@pytest.mark.embedding
def test_installation_exposes_its_limitations():
    """Test that an installation reports the limitations of its version."""
    assert Installation(241, Path("/ansys_inc/v241")).limitations == Limitations(241)
