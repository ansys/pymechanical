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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Mock tests for ``App.save_as`` lock-file removal (no ``embedded_app`` fixture)."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ansys.mechanical.core.embedding.app import App

pytestmark = pytest.mark.embedding


@pytest.fixture
def mock_app():
    """Minimal stand-in for ``App`` with only APIs used by ``save_as``."""
    m = MagicMock()
    m.DataModel.Project.SaveAs = MagicMock()
    m.log_warning = MagicMock()
    m.log_error = MagicMock()
    return m


@pytest.mark.embedding
def test_save_as_remove_lock_unlinks_lock_file(mock_app, tmp_path):
    """When ``remove_lock=True`` and ``.mech_lock`` exists, it is removed before SaveAs."""
    project_file = tmp_path / "project.mechdat"
    project_file.write_text("", encoding="utf-8")
    mech_dir = tmp_path / "project_Mech_Files"
    mech_dir.mkdir()
    lock_file = mech_dir / ".mech_lock"
    lock_file.write_text("lock", encoding="utf-8")

    App.save_as(mock_app, str(project_file), overwrite=True, remove_lock=True)

    assert not lock_file.exists()
    mock_app.DataModel.Project.SaveAs.assert_called_once()
    call_args = mock_app.DataModel.Project.SaveAs.call_args[0]
    assert Path(call_args[0]).resolve() == project_file.resolve()
    assert call_args[1] is True
    mock_app.log_warning.assert_called_once()
    assert "Removing the lock file" in mock_app.log_warning.call_args[0][0]


@pytest.mark.embedding
def test_save_as_remove_lock_no_warning_when_lock_missing(mock_app, tmp_path):
    """``remove_lock=True`` does not log when there is no lock file."""
    project_file = tmp_path / "project.mechdat"
    project_file.write_text("", encoding="utf-8")
    mech_dir = tmp_path / "project_Mech_Files"
    mech_dir.mkdir()

    App.save_as(mock_app, str(project_file), overwrite=True, remove_lock=True)

    mock_app.DataModel.Project.SaveAs.assert_called_once()
    mock_app.log_warning.assert_not_called()


@pytest.mark.embedding
def test_save_as_without_remove_lock_preserves_lock_file(mock_app, tmp_path):
    """``remove_lock=False`` leaves an existing ``.mech_lock`` in place."""
    project_file = tmp_path / "project.mechdat"
    project_file.write_text("", encoding="utf-8")
    mech_dir = tmp_path / "project_Mech_Files"
    mech_dir.mkdir()
    lock_file = mech_dir / ".mech_lock"
    lock_file.write_text("lock", encoding="utf-8")

    App.save_as(mock_app, str(project_file), overwrite=True, remove_lock=False)

    assert lock_file.exists()
    mock_app.DataModel.Project.SaveAs.assert_called_once()
    mock_app.log_warning.assert_not_called()
