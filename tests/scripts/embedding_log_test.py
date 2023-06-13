"""Test cases for embedding logging."""

import logging
import sys

import ansys.mechanical.core as mech
from ansys.mechanical.core.embedding.logger import Configuration, Logger


def log_before_initialize():
    """Write a log without initializing the embedded instance."""
    Logger.error("message")


def log_info_after_initialize_with_error_level():
    """Log at the info level after initializing with the error level."""
    Configuration.configure(level=logging.ERROR, to_stdout=True, base_directory=None)
    _ = mech.App(version=232)
    Logger.info("0xdeadbeef")


def log_error_after_initialize_with_info_level():
    """Log at the info level after initializing with the error level."""
    _ = mech.App(version=232)
    Configuration.configure(level=logging.INFO, to_stdout=True, base_directory=None)
    Logger.error("Will no one rid me of this turbulent priest?")


def log_check_can_log_message():
    """Configure logger before app initialization and check can_log_message."""
    Configuration.configure(level=logging.WARNING, to_stdout=True, base_directory=None)
    assert Logger.can_log_message(logging.DEBUG) is False
    assert Logger.can_log_message(logging.INFO) is False
    assert Logger.can_log_message(logging.WARNING) is True
    assert Logger.can_log_message(logging.ERROR) is True
    assert Logger.can_log_message(logging.FATAL) is True
    _ = mech.App(version=232)
    Configuration.set_log_level(logging.INFO)
    assert Logger.can_log_message(logging.DEBUG) is False
    assert Logger.can_log_message(logging.INFO) is True
    assert Logger.can_log_message(logging.WARNING) is True
    assert Logger.can_log_message(logging.ERROR) is True
    assert Logger.can_log_message(logging.FATAL) is True


if __name__ == "__main__":
    test_name = sys.argv[1]
    tests = {
        "log_before_initialize": log_before_initialize,
        "log_info_after_initialize_with_error_level": log_info_after_initialize_with_error_level,
        "log_error_after_initialize_with_info_level": log_error_after_initialize_with_info_level,
        "log_check_can_log_message": log_check_can_log_message,
    }
    tests[test_name]()
    print("@@success@@")
