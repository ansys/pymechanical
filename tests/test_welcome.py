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

"""Welcome screen tests."""

import io
import subprocess
import sys

from click.testing import CliRunner
import pytest

from ansys.mechanical.core import _welcome
from ansys.mechanical.core._version import __version__
from ansys.mechanical.core.run import cli


@pytest.mark.cli
def test_cli_info_shows_welcome():
    """Test that ``--info`` prints the welcome screen and exits successfully."""
    result = CliRunner().invoke(cli, ["--info"])
    assert result.exit_code == 0
    assert "ansys-mechanical-core" in result.output


@pytest.mark.cli
def test_render_welcome_plain_fallback(monkeypatch):
    """Test that the welcome screen renders without ``rich`` installed."""
    monkeypatch.setitem(sys.modules, "rich", None)
    stream = io.StringIO()
    _welcome.render_welcome(file=stream)
    assert "Quick start" in stream.getvalue()


@pytest.mark.cli
def test_render_welcome_quick_start_prompt(monkeypatch):
    """Test that quick start code lines are prefixed with a Python prompt."""
    monkeypatch.setitem(sys.modules, "rich", None)
    stream = io.StringIO()
    _welcome.render_welcome(file=stream)
    assert ">>> from ansys.mechanical.core import App" in stream.getvalue()


@pytest.mark.cli
def test_get_system_info_package_version():
    """Test that system info reports the installed package version."""
    assert _welcome.get_system_info()["Package version"] == __version__


@pytest.mark.cli
def test_package_import_prints_nothing():
    """Test that importing the package does not print the welcome screen."""
    result = subprocess.run(
        [sys.executable, "-c", "import ansys.mechanical.core"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "ansys-mechanical-core" not in result.stdout
