# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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


def _run_background_app_test_process(
    rootdir: str, run_subprocess, pytestconfig, testname: str, pass_expected: bool = None
) -> typing.Tuple[bytes, bytes]:
    """Run the process and return stdout and stderr after it finishes."""
    version = pytestconfig.getoption("ansys_version")
    script = os.path.join(rootdir, "tests", "scripts", "background_app_test.py")
    stdout, stderr = run_subprocess(
        [sys.executable, script, version, testname], None, pass_expected
    )
    return stdout, stderr


def _assert_success(stdout: str, pass_expected: bool) -> bool:
    """Check whether the process ran to completion from its stdout

    Duplicate of the `_assert_success` function in test_logger.py
    """

    if pass_expected:
        assert "@@success@@" in stdout
    else:
        assert "@@success@@" not in stdout


def _run_background_app_test(
    run_subprocess, rootdir: str, pytestconfig, testname: str, pass_expected: bool = True
) -> str:
    """Test stderr logging using a subprocess.

    Also ensure that the subprocess either passes or fails based on pass_expected

    Returns the stderr of the subprocess as a string.
    """
    subprocess_pass_expected = pass_expected
    if pass_expected == True and os.name != "nt":
        subprocess_pass_expected = False
    stdout, stderr = _run_background_app_test_process(
        rootdir, run_subprocess, pytestconfig, testname, subprocess_pass_expected
    )
    if not subprocess_pass_expected:
        stdout = stdout.decode()
        _assert_success(stdout, pass_expected)
    stderr = stderr.decode()
    return stderr


@pytest.mark.embedding_scripts
def test_background_app_multiple_instances(rootdir, run_subprocess, pytestconfig):
    """Test that multiple instances of background app can be used."""
    stderr = _run_background_app_test(
        run_subprocess, rootdir, pytestconfig, "multiple_instances", True
    )
    assert "Project 1" in stderr
    assert "Project 2" in stderr
    assert "Foo 3" in stderr
    assert "Project 4" in stderr


@pytest.mark.embedding_scripts
def test_background_app_use_stopped(rootdir, run_subprocess, pytestconfig):
    """Test that multiple instances of background app cannot be used after an instance is stopped."""
    stderr = _run_background_app_test(
        run_subprocess, rootdir, pytestconfig, "test_background_app_use_stopped", False
    )
    assert "Cannot use background app after stopping it" in stderr


@pytest.mark.embedding_scripts
def test_background_app_initialize_stopped(rootdir, run_subprocess, pytestconfig):
    """Test that multiple instances of background app cannot be used after an instance is stopped."""
    stderr = _run_background_app_test(
        run_subprocess, rootdir, pytestconfig, "test_background_app_initialize_stopped", False
    )
    assert "Cannot initialize a BackgroundApp once it has been stopped!" in stderr
