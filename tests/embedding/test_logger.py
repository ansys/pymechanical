"""Miscellaneous embedding tests"""
import os
import subprocess
import sys

import pytest


def _run_embedding_log_test_process(rootdir, testname) -> subprocess.Popen:
    """Runs the process and returns it after it finishes"""
    embedded_py = os.path.join(rootdir, "tests", "scripts", "embedding_log_test.py")
    p = subprocess.Popen(
        [sys.executable, embedded_py, testname], stderr=subprocess.PIPE, stdout=subprocess.PIPE
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
    # function runs, which will only be execution if the function doesn't
    # throw. To check for the subprocess success, ensure that the stdout
    # has "@@success@@" (a value written there in the subprocess after the
    # test function runs)
    stdout = process.stdout.read().decode()
    if pass_expected:
        assert "@@success@@" in stdout
    else:
        assert "@@success@@" not in stdout


def _run_embedding_log_test(rootdir: str, testname: str, pass_expected: bool = True) -> str:
    """Test stderr logging using a subprocess.

    Also ensure that the subprocess either passes or fails based on pass_expected
    Mechanical logging all goes into the process stderr at the C level, but capturing
    that from python isn't possible because python's stderr stream isn't aware of content
    that doesn't come from python (or its C/API)

    Returns the stderr
    """
    p = _run_embedding_log_test_process(rootdir, testname)
    stderr = p.stderr.read().decode()
    _assert_success(p, pass_expected)
    return stderr


@pytest.mark.embedding
def test_logging_write_log_before_init(rootdir):
    """Test that an error is thrown when trying to log before initializing"""
    stderr = _run_embedding_log_test(rootdir, "log_before_initialize", False)
    assert "Can't log to the embedding logger until Mechanical is initialized" in stderr


@pytest.mark.embedding
def test_logging_write_info_after_initialize_with_error_level(rootdir):
    """Test that no output is written when an info is logged when configured at the error level."""
    stderr = _run_embedding_log_test(rootdir, "log_info_after_initialize_with_error_level")
    assert "0xdeadbeef" not in stderr


@pytest.mark.embedding
def test_logging_write_error_after_initialize_with_info_level(rootdir):
    """Test that output is written when an error is logged when configured at the info level."""
    stderr = _run_embedding_log_test(rootdir, "log_error_after_initialize_with_info_level")
    assert "Will no one rid me of this turbulent priest?" in stderr


@pytest.mark.embedding
def test_logging_level_before_and_after_initialization(rootdir):
    """Test logging level API  before and after initialization."""
    p = _run_embedding_log_test_process(rootdir, "log_check_can_log_message")
    _assert_success(p, True)
