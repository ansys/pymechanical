"""Miscellaneous embedding tests"""
import os
import subprocess
import sys
import typing

import pytest


def _run_embedding_log_test_process(rootdir, testname) -> subprocess.Popen:
    """Runs the process and returns it after it finishes"""
    embedded_py = os.path.join(rootdir, "tests", "scripts", "embedding_log_test.py")
    p = subprocess.Popen(
        [sys.executable, embedded_py, testname], stderr=subprocess.PIPE, stdout=subprocess.PIPE
    )
    p.wait()
    return p


def _get_success(process: subprocess.Popen) -> int:
    """Return whether the process succeeds or fails."""
    if os.name == "nt":
        return process.returncode == 0

    # HACK! On linux, due to bug #85, there is always a crash on shutdown
    # so instead there's a print("success") that happens after the test
    # function runs, which will only be execution if the function doesn't
    # throw. To check for the subprocess success, ensure that the stdout
    # is "success"
    stdout = process.stdout.read().decode()
    return "@@success@@" in stdout


def _run_embedding_log_test(rootdir, testname) -> typing.Tuple[str, bool]:
    """Test stderr logging using a subprocess.

    Mechanical logging all goes into the process stderr at the C level, but capturing
    that from python isn't possible because python's stderr stream isn't aware of content
    that doesn't come from python (or its C/API)

    Returns the stderr and whether the process was successful
    """
    p = _run_embedding_log_test_process(rootdir, testname)
    stderr = p.stderr.read().decode()
    return stderr, _get_success(p)


@pytest.mark.embedding
def test_logging_write_log_before_init(rootdir):
    """Test that an error is thrown when trying to log before initializing"""
    stderr, success = _run_embedding_log_test(rootdir, "log_before_initialize")
    assert not success
    assert "Can't log to the embedding logger until Mechanical is initialized" in stderr


@pytest.mark.embedding
def test_logging_write_info_after_initialize_with_error_level(rootdir):
    """Test that no output is written when an info is logged when configured at the error level."""
    stderr, success = _run_embedding_log_test(rootdir, "log_info_after_initialize_with_error_level")
    assert "0xdeadbeef" not in stderr
    assert success


@pytest.mark.embedding
def test_logging_write_error_after_initialize_with_info_level(rootdir):
    """Test that output is written when an error is logged when configured at the info level."""
    stderr, success = _run_embedding_log_test(rootdir, "log_error_after_initialize_with_info_level")
    assert "Will no one rid me of this turbulent priest?" in stderr
    assert success


@pytest.mark.embedding
def test_logging_level_before_and_after_initialization(rootdir):
    """Test logging level API  before and after initialization."""
    p = _run_embedding_log_test_process(rootdir, "log_check_can_log_message")
    assert _get_success(p)
