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
import subprocess
import sys

import pytest


def _unset_var(env, var) -> None:
    if var in env:
        del env[var]


def _get_env_without_logging_variables():
    # unset all logging environment variables.
    env = os.environ.copy()
    _unset_var(env, "ANSYS_WORKBENCH_LOGGING")
    _unset_var(env, "ANSYS_WORKBENCH_LOGGING_FILTER_LEVEL")
    _unset_var(env, "ANSYS_WORKBENCH_LOGGING_CONSOLE")
    _unset_var(env, "ANSYS_WORKBENCH_LOGGING_AUTO_FLUSH")
    _unset_var(env, "ANSYS_WORKBENCH_LOGGING_DIRECTORY")
    return env


def _run_embedding_log_test_process(rootdir, pytestconfig, testname) -> subprocess.Popen:
    """Runs the process and returns it after it finishes"""
    version = pytestconfig.getoption("ansys_version")
    embedded_py = os.path.join(rootdir, "tests", "scripts", "embedding_log_test.py")
    p = subprocess.Popen(
        [sys.executable, embedded_py, version, testname],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        env=_get_env_without_logging_variables(),
    )
    p.wait()
    return p


def _assert_success(process: subprocess.Popen, pass_expected: bool) -> int:
    """Asserts the outcome of the process matches pass_expected"""
    if os.name == "nt":
        passing = process.returncode == 0
        assert passing == pass_expected

    # HACK! On linux, due to bug #85, there is always a crash on shutdown
    # so instead there's a print("success") that happens after the test
    # function runs that will only be executed if the function doesn't
    # throw. To check for the subprocess success, ensure that the stdout
    # has "@@success@@" (a value written there in the subprocess after the
    # test function runs)
    stdout = process.stdout.read().decode()
    if pass_expected:
        assert "@@success@@" in stdout
    else:
        assert "@@success@@" not in stdout


def _run_embedding_log_test(
    rootdir: str, pytestconfig, testname: str, pass_expected: bool = True
) -> str:
    """Test stderr logging using a subprocess.

    Also ensure that the subprocess either passes or fails based on pass_expected
    Mechanical logging all goes into the process stderr at the C level, but capturing
    that from python isn't possible because python's stderr stream isn't aware of content
    that doesn't come from python (or its C/API)

    Returns the stderr
    """
    p = _run_embedding_log_test_process(rootdir, pytestconfig, testname)
    stderr = p.stderr.read().decode()
    _assert_success(p, pass_expected)
    return stderr


@pytest.mark.embedding
@pytest.mark.timeout(90)
def test_logging_write_log_before_init(rootdir, pytestconfig):
    """Test that an error is thrown when trying to log before initializing"""
    stderr = _run_embedding_log_test(rootdir, pytestconfig, "log_before_initialize", False)
    assert "Can't log to the embedding logger until Mechanical is initialized" in stderr


@pytest.mark.embedding
@pytest.mark.timeout(90)
def test_logging_write_info_after_initialize_with_error_level(rootdir, pytestconfig):
    """Test that no output is written when an info is logged when configured at the error level."""
    stderr = _run_embedding_log_test(
        rootdir, pytestconfig, "log_info_after_initialize_with_error_level"
    )
    assert "0xdeadbeef" not in stderr


@pytest.mark.parametrize("addin_configuration", ["Mechanical", "WorkBench"])
@pytest.mark.embedding
@pytest.mark.minimum_version(241)
@pytest.mark.timeout(180)
def test_addin_configuration(rootdir, pytestconfig, addin_configuration):
    """Test that mechanical can start with both the Mechanical and WorkBench configuration."""
    stderr = _run_embedding_log_test(
        rootdir, pytestconfig, f"log_configuration_{addin_configuration}"
    )
    assert f"{addin_configuration} configuration!" in stderr


@pytest.mark.embedding
@pytest.mark.timeout(90)
def test_logging_write_error_after_initialize_with_info_level(rootdir, pytestconfig):
    """Test that output is written when an error is logged when configured at the info level."""
    stderr = _run_embedding_log_test(
        rootdir, pytestconfig, "log_error_after_initialize_with_info_level"
    )
    assert "Will no one rid me of this turbulent priest?" in stderr


@pytest.mark.embedding
def test_logging_level_before_and_after_initialization(rootdir, pytestconfig):
    """Test logging level API  before and after initialization."""
    p = _run_embedding_log_test_process(rootdir, pytestconfig, "log_check_can_log_message")
    _assert_success(p, True)
