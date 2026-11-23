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

"""Tests for resolving the Mechanical installation."""

import os
from pathlib import Path

import ansys.tools.common.path as atp
from click.testing import CliRunner
import pytest

from ansys.mechanical.core import _installation
from ansys.mechanical.core.embedding.find_mechanical import cli as find_mechanical_cli
from ansys.mechanical.core.misc import get_mechanical_bin, has_grpc_service_pack


def _clear_awp_roots(monkeypatch):
    for key in [key for key in os.environ if key.startswith("AWP_ROOT")]:
        monkeypatch.delenv(key)


@pytest.mark.embedding
def test_find_prefers_requested_awp_root_without_version_folder():
    """Test that find uses AWP_ROOT<version> even when its folder isn't named vNNN."""
    environ = {"AWP_ROOT252": "/ansys_inc/v252", "AWP_ROOT261": "/opt/ansys/2026R1"}

    assert _installation.find(261, environ).root == Path("/opt/ansys/2026R1")


@pytest.mark.embedding
def test_find_uses_aisol_parent_as_locator_root_without_version_folder():
    """Test that find takes the folder above aisol as the root of a located executable."""

    def locator(allow_input, version):
        return "/custom/2026R1/aisol/bin/winx64/AnsysWBU.exe"

    found = _installation.find(None, {}, locator)

    assert (found.version, found.root) == (261, Path("/custom/2026R1"))


@pytest.mark.embedding
@pytest.mark.windows_only
def test_find_mechanical_cli_prints_executable_folder_for_located_install(monkeypatch):
    """Test that find-mechanical prints the executable folder when ansys-tools-path finds it."""
    _clear_awp_roots(monkeypatch)
    exe = r"C:\Program Files\ANSYS Inc\v261\aisol\bin\winx64\AnsysWBU.exe"
    monkeypatch.setattr(atp, "get_mechanical_path", lambda allow_input, version: exe)

    result = CliRunner().invoke(find_mechanical_cli, [])

    assert result.stdout.strip() == r"261 C:\Program Files\ANSYS Inc\v261\aisol\bin\winx64"


@pytest.mark.embedding
def test_find_mechanical_cli_reports_awp_roots_without_version_folder(monkeypatch):
    """Test that find-mechanical doesn't claim AWP_ROOT variables are missing when they're set."""
    _clear_awp_roots(monkeypatch)
    monkeypatch.setenv("AWP_ROOTDV", "/ansys_inc/dev")
    monkeypatch.setattr(atp, "get_mechanical_path", lambda allow_input, version: None)

    result = CliRunner().invoke(find_mechanical_cli, [])

    assert "No AWP_ROOT### env. variables pointing to a v<version> folder found" in result.stderr


@pytest.mark.embedding
def test_find_mechanical_cli_prints_aisol_of_given_path(tmp_path):
    """Test that find-mechanical -p prints the version and aisol folder of the path."""
    root = tmp_path / "v252"
    root.mkdir()

    result = CliRunner().invoke(find_mechanical_cli, ["-p", str(root)])

    assert result.stdout.strip() == f"252 {root / 'aisol'}"


@pytest.mark.embedding
def test_find_mechanical_cli_rejects_path_of_other_version(tmp_path):
    """Test that find-mechanical fails when -r doesn't match the -p version."""
    root = tmp_path / "v252"
    root.mkdir()

    result = CliRunner().invoke(find_mechanical_cli, ["-p", str(root), "-r", "261"])

    assert "does not match the specified version 261" in result.output


@pytest.mark.embedding
def test_installed_ignores_roots_without_version_folder():
    """Test that installed skips AWP_ROOT values without a vNNN folder."""
    environ = {
        "AWP_ROOT252": "/ansys_inc/v252",
        "AWP_ROOT261": "/ansys_inc/v261",
        "AWP_ROOTDV": "/ansys_inc/dev",
        "PATH": "/usr/bin",
    }

    assert sorted(_installation.installed(environ)) == [252, 261]


@pytest.mark.embedding
def test_find_prefers_requested_version_from_environment():
    """Test that find returns the requested version when its AWP_ROOT is set."""
    environ = {"AWP_ROOT252": "/ansys_inc/v252", "AWP_ROOT261": "/ansys_inc/v261"}

    assert _installation.find(252, environ).root == Path("/ansys_inc/v252")


@pytest.mark.embedding
def test_find_falls_back_to_latest_environment_version():
    """Test that find returns the latest AWP_ROOT version when the requested one is unset."""
    environ = {"AWP_ROOT252": "/ansys_inc/v252", "AWP_ROOT261": "/ansys_inc/v261"}

    assert _installation.find(242, environ).version == 261


@pytest.mark.embedding
def test_find_uses_locator_root_without_environment():
    """Test that find derives the vNNN root from the locator's executable."""

    def locator(allow_input, version):
        return "/usr/ansys_inc/v252/aisol/.workbench"

    found = _installation.find(None, {}, locator)

    assert (found.version, found.root) == (252, Path("/usr/ansys_inc/v252"))


@pytest.mark.embedding
def test_find_returns_none_when_nothing_found():
    """Test that find returns None without AWP_ROOT or a located executable."""
    assert _installation.find(None, {}, lambda allow_input, version: None) is None


@pytest.mark.embedding
def test_find_prefers_locator_over_environment_when_requested():
    """Test that find returns the located install before AWP_ROOT with prefer_locator."""

    def locator(allow_input, version):
        return "/saved/v252/aisol/.workbench"

    found = _installation.find(None, {"AWP_ROOT261": "/ansys_inc/v261"}, locator, True)

    assert (found.version, found.root) == (252, Path("/saved/v252"))


@pytest.mark.embedding
def test_find_falls_back_to_environment_when_preferred_locator_finds_nothing():
    """Test that find reads AWP_ROOT when the preferred locator returns nothing."""
    found = _installation.find(
        None, {"AWP_ROOT261": "/ansys_inc/v261"}, lambda allow_input, version: None, True
    )

    assert found.root == Path("/ansys_inc/v261")


@pytest.mark.embedding
def test_find_calls_preferred_locator_once_when_nothing_found():
    """Test that find doesn't retry the locator after a preferred lookup fails."""
    calls = []

    def locator(allow_input, version):
        calls.append(version)

    assert _installation.find(None, {}, locator, True) is None
    assert len(calls) == 1


@pytest.mark.embedding
def test_get_mechanical_bin_uses_awp_root_as_install_root(monkeypatch, tmp_path):
    """Test that get_mechanical_bin doesn't append the version folder to AWP_ROOT."""
    root = tmp_path / "v261"
    monkeypatch.setenv("AWP_ROOT261", str(root))

    assert Path(get_mechanical_bin("261")).relative_to(root).parts[0] == "aisol"


@pytest.mark.embedding
def test_for_version_uses_root_discovered_under_other_variable_name():
    """Test that for_version finds a vNNN root declared under a non-versioned AWP_ROOT name."""
    environ = {"AWP_ROOTDV": "/ansys_inc/v271"}

    assert _installation.for_version(271, environ).root == Path("/ansys_inc/v271")


@pytest.mark.embedding
def test_for_version_raises_when_root_not_set():
    """Test that for_version names the missing AWP_ROOT variable."""
    with pytest.raises(RuntimeError, match="AWP_ROOT261"):
        _installation.for_version(261, {})


@pytest.mark.embedding
@pytest.mark.parametrize(
    "path",
    [
        "C:/Program Files/ANSYS Inc/v251/aisol/bin/winx64/AnsysWBU.exe",
        "C:/Program Files/ANSYS Inc/v251/aisol/.workbench",
        "C:/Program Files/ANSYS Inc/v251/aisol",
    ],
)
def test_from_path_uses_folder_above_aisol_as_root(path):
    """Test that from_path takes the folder above aisol as the root for paths inside it."""
    found = _installation.from_path(path)

    assert (found.version, found.root) == (251, Path("C:/Program Files/ANSYS Inc/v251"))


@pytest.mark.embedding
def test_from_path_uses_installation_folder_as_root(tmp_path):
    """Test that from_path takes an existing folder outside aisol as the root."""
    root = tmp_path / "v252"
    root.mkdir()

    assert _installation.from_path(root) == _installation.Installation(252, root)


@pytest.mark.embedding
def test_from_path_reads_release_folder_version(tmp_path):
    """Test that from_path reads the version from a 2026R1-style folder."""
    root = tmp_path / "2026R1"
    root.mkdir()

    assert _installation.from_path(root).version == 261


@pytest.mark.embedding
def test_from_path_raises_when_version_unknown():
    """Test that from_path lets the version parsing error through."""
    with pytest.raises(RuntimeError):
        _installation.from_path("/custom/mechanical.exe")


@pytest.mark.embedding
def test_has_grpc_service_pack_reads_given_installation(tmp_path):
    """Test that has_grpc_service_pack reads builddate.txt from the given installation."""
    root = tmp_path / "v252"
    root.mkdir()
    (root / "builddate.txt").write_text("2025 R2 SP03\n", encoding="utf-8")

    assert has_grpc_service_pack(_installation.Installation(252, root)) is True


@pytest.mark.embedding
def test_has_grpc_service_pack_rejects_given_installation_without_service_pack(tmp_path):
    """Test that has_grpc_service_pack is False when the given installation lacks the pack."""
    root = tmp_path / "v252"
    root.mkdir()
    (root / "builddate.txt").write_text("2025 R2\n", encoding="utf-8")

    assert has_grpc_service_pack(_installation.Installation(252, root)) is False
