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

"""Miscellaneous embedding tests"""

import os
import sys
import typing

import pytest

from .test_logger import _assert_success


def _run_background_app_test(
    run_subprocess, rootdir: str, pytestconfig, testname: str, pass_expected: bool = True
) -> typing.Tuple[bytes, bytes]:
    """Run the process and return stdout and stderr after it finishes."""
    version = pytestconfig.getoption("ansys_version")
    script = os.path.join(rootdir, "tests", "scripts", "background_app_test.py")

    subprocess_pass_expected = pass_expected
    if pass_expected and os.name != "nt":
        if int(version) < 251:
            subprocess_pass_expected = False

    process, stdout, stderr = run_subprocess(
        [sys.executable, script, version, testname], None, subprocess_pass_expected
    )

    if not subprocess_pass_expected:
        stdout = stdout.decode()
        _assert_success(stdout, pass_expected)
    stderr = stderr.decode()
    return stderr


@pytest.mark.embedding_scripts
@pytest.mark.embedding_backgroundapp
def test_background_app_multiple_instances(rootdir, run_subprocess, pytestconfig):
    """Multiple instances of background app can be used."""
    stderr = _run_background_app_test(
        run_subprocess, rootdir, pytestconfig, "multiple_instances", True
    )
    assert "Project 1" in stderr
    assert "Project 2" in stderr
    assert "Foo 3" in stderr
    assert "Project 4" in stderr


@pytest.mark.embedding_scripts
@pytest.mark.embedding_backgroundapp
def test_background_app_use_stopped(rootdir, run_subprocess, pytestconfig):
    """Multiple instances of background app cannot be used after an instance is stopped."""
    stderr = _run_background_app_test(
        run_subprocess, rootdir, pytestconfig, "test_background_app_use_stopped", False
    )
    assert "Cannot use BackgroundApp after stopping it" in stderr


@pytest.mark.embedding_scripts
@pytest.mark.embedding_backgroundapp
def test_background_app_initialize_stopped(rootdir, run_subprocess, pytestconfig):
    """Multiple instances of background app cannot be used after an instance is stopped."""
    stderr = _run_background_app_test(
        run_subprocess, rootdir, pytestconfig, "test_background_app_initialize_stopped", False
    )
    assert "Cannot initialize a BackgroundApp once it has been stopped!" in stderr
