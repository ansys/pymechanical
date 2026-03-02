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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Test cases for embedding logging."""

import logging
import sys

import ansys.mechanical.core as mech
from ansys.mechanical.core.embedding.addins import AddinConfiguration
from ansys.mechanical.core.embedding.logger import Configuration, Logger


def log_before_initialize(version):
    """Write a log without initializing the embedded instance."""
    Logger.error("message")


def log_info_after_initialize_with_error_level(version):
    """Log at the info level after initializing with the error level."""
    Configuration.configure(level=logging.ERROR, to_stdout=True, base_directory=None)
    _ = mech.App(version=version)
    Logger.info("0xdeadbeef")


def log_error_after_initialize_with_info_level(version):
    """Log at the info level after initializing with the error level."""
    _ = mech.App(version=version)
    Configuration.configure(level=logging.INFO, to_stdout=True, base_directory=None)
    Logger.error("Will no one rid me of this turbulent priest?")


def log_configuration_mechanical(version):
    """Log at the info level after app starts with the `Mechanical` configuration."""
    _ = mech.App(version=version, config=AddinConfiguration("Mechanical"))
    Configuration.configure(level=logging.INFO, to_stdout=True, base_directory=None)
    Logger.error("Mechanical configuration!")


def log_configuration_workbench(version):
    """Log at the info level after app starts with the `WorkBench` configuration."""
    _ = mech.App(version=version, config=AddinConfiguration("WorkBench"))
    Configuration.configure(level=logging.INFO, to_stdout=True, base_directory=None)
    Logger.error("WorkBench configuration!")


def log_check_can_log_message(version):
    """Configure logger before app initialization and check can_log_message."""
    Configuration.configure(level=logging.WARNING, to_stdout=True, base_directory=None)
    assert Logger.can_log_message(logging.DEBUG) is False
    assert Logger.can_log_message(logging.INFO) is False
    assert Logger.can_log_message(logging.WARNING) is True
    assert Logger.can_log_message(logging.ERROR) is True
    assert Logger.can_log_message(logging.FATAL) is True
    _ = mech.App(version=version)
    Configuration.set_log_level(logging.INFO)
    assert Logger.can_log_message(logging.DEBUG) is False
    assert Logger.can_log_message(logging.INFO) is True
    assert Logger.can_log_message(logging.WARNING) is True
    assert Logger.can_log_message(logging.ERROR) is True
    assert Logger.can_log_message(logging.FATAL) is True


def log_check_all_log_level(version):
    """Configure logger before app initialization and check can_log_message."""
    Configuration.configure(level=logging.DEBUG, to_stdout=True, base_directory=None)
    assert Logger.can_log_message(logging.FATAL) is True
    _ = mech.App(version=version)
    Logger.debug("debug")
    Logger.info("info")
    Logger.warning("warning")
    Logger.error("error")
    Logger.fatal("fatal")


if __name__ == "__main__":
    version = sys.argv[1]
    test_name = sys.argv[2]
    tests = {
        "log_before_initialize": log_before_initialize,
        "log_info_after_initialize_with_error_level": log_info_after_initialize_with_error_level,
        "log_error_after_initialize_with_info_level": log_error_after_initialize_with_info_level,
        "log_check_can_log_message": log_check_can_log_message,
        "log_configuration_Mechanical": log_configuration_mechanical,
        "log_configuration_WorkBench": log_configuration_workbench,
        "log_check_all_log_level": log_check_all_log_level,
    }
    tests[test_name](int(version))
    print("@@success@@")
