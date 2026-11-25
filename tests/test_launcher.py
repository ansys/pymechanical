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

"""Test for MechanicalLauncher."""

import pytest

import ansys.mechanical.core.launcher as launcher
from ansys.mechanical.core.misc import is_windows


@pytest.mark.remote_session_launch
def test_verify_path_exists():
    """Test for verifying that the path exists."""
    if is_windows():
        windows_path = (
            "C:\\does_not_exist\\Program Files\\ANSYS Inc\\v111\\aisol\\bin\\winx64\\AnsysWBU.exe"
        )
        with pytest.raises(FileNotFoundError):
            launcher.MechanicalLauncher.verify_path_exists(windows_path)
    else:
        linux_path = "/usr/does_not_exist/ansys_inc/v111/aisol/.workbench"
        with pytest.raises(FileNotFoundError):
            launcher.MechanicalLauncher.verify_path_exists(linux_path)


@pytest.mark.remote_session_launch
def test_verify_mode_exists():
    """Test for verifying that the mode exists."""
    additional_args = None
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMech")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMesh")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeRest")

    additional_args = []
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMech")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMesh")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeRest")

    additional_args = ["-AppModeMech"]
    assert launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMech")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMesh")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeRest")

    additional_args = ["-AppModeMesh"]
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMech")
    assert launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMesh")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeRest")

    additional_args = ["-AppModeRest"]
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMech")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMesh")
    assert launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeRest")


def _fake_installation(tmp_path, version, builddate):
    """Create a Mechanical folder layout with a builddate.txt and return its executable."""
    root = tmp_path / f"v{version}"
    exe = root / "aisol" / "bin" / "winx64" / "AnsysWBU.exe"
    exe.parent.mkdir(parents=True)
    exe.touch()
    (root / "builddate.txt").write_text(builddate, encoding="utf-8")
    return str(exe)


@pytest.mark.remote_session_launch
def test_command_line_reads_service_pack_of_launched_installation(tmp_path):
    """Test that secure gRPC flags follow the builddate.txt of the launched executable."""
    exe = _fake_installation(tmp_path, 252, "2025 R2 SP03\n")
    mech_launcher = launcher.MechanicalLauncher(True, 10000, exe, transport_mode="insecure")

    args = mech_launcher._MechanicalLauncher__get_commandline_args()

    assert "--transport-mode" in args


@pytest.mark.remote_session_launch
def test_command_line_rejects_secure_mode_without_service_pack(tmp_path):
    """Test that a secure mode raises when the launched installation lacks the pack."""
    exe = _fake_installation(tmp_path, 252, "2025 R2\n")
    mech_launcher = launcher.MechanicalLauncher(True, 10000, exe, transport_mode="wnua")

    with pytest.raises(Exception, match="does not support secure transport modes"):
        mech_launcher._MechanicalLauncher__get_commandline_args()
