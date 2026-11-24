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

"""Tests for the Mechanical capabilities of each version."""

from pathlib import Path

import pytest

from ansys.mechanical.core._capabilities import Capabilities
from ansys.mechanical.core._installation import Installation
from ansys.mechanical.core.misc import get_service_pack_message


@pytest.mark.embedding
@pytest.mark.parametrize(
    "name, previous, first",
    [
        ("grpc_launch", 231, 232),
        ("plotting", 241, 242),
        ("linux_function_codec", 241, 242),
        ("license_manager", 251, 252),
        ("interactive", 252, 261),
        ("startup_arguments", 252, 261),
        ("cpython_engine", 252, 261),
        ("object_scenegraph", 252, 261),
        ("license_coordinator", 261, 271),
    ],
)
def test_capability_starts_at_first_release(name, previous, first):
    """Test that each capability is off before its first release and on from it."""
    assert getattr(Capabilities(previous), name) is False
    assert getattr(Capabilities(first), name) is True


@pytest.mark.embedding
@pytest.mark.parametrize(
    "version, expected",
    [(241, None), (242, 5), (251, 4), (252, 3), (253, None), (261, 0), (271, 0)],
)
def test_grpc_service_pack_by_release(version, expected):
    """Test the service pack each release needs for secure gRPC."""
    assert Capabilities(version).grpc_service_pack == expected


@pytest.mark.embedding
@pytest.mark.parametrize("version, expected", [(251, False), (252, False), (261, True)])
def test_clr_host_lite_default_from_2026_r1(version, expected):
    """Test that the lite CLR host is the default from 2026 R1."""
    assert Capabilities(version).clr_host_lite_default is expected


@pytest.mark.embedding
def test_installation_exposes_its_capabilities():
    """Test that an installation reports the capabilities of its version."""
    assert Installation(261, Path("/ansys_inc/v261")).capabilities == Capabilities(261)


@pytest.mark.embedding
def test_windows_store_dll_dirs_include_framework_and_tp_folders():
    """Test that the Windows Store DLL folders include Framework and the release's tp folders."""
    root = Path("/ansys_inc/v261")

    dirs = Installation(261, root).windows_store_dll_dirs

    assert root / "Framework" / "bin" / "Win64" in dirs
    assert root / "tp" / "qt" / "5.15.19" / "winx64" / "bin" in dirs


@pytest.mark.embedding
def test_windows_store_dll_dirs_unknown_for_unrecognized_release():
    """Test that an unrecognized release has no Windows Store DLL folders."""
    assert Installation(999, Path("/ansys_inc/v999")).windows_store_dll_dirs is None


@pytest.mark.embedding
@pytest.mark.parametrize(
    "version, expected",
    [
        (241, "Update to Ansys 2024 R2 or later with required service pack"),
        (251, "Update to Service Pack SP04 or later"),
        (261, ""),
        (232, "Update to Ansys 2024 R2 or later for secure gRPC support."),
    ],
)
def test_get_service_pack_message_by_release(version, expected):
    """Test that the service pack message matches each release's requirement."""
    assert get_service_pack_message(version).startswith(expected)
