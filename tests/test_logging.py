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

"""Testing of log module."""

import logging as deflogging  # Default logging
from pathlib import Path
import re

from conftest import HAS_GRPC
import pytest

from ansys.mechanical.core import (
    LOG,  # Global logger
    logging,
)

## Notes
# Use the next fixtures for:
# - capfd: for testing console printing.
# - caplog: for testing logging printing.

LOG_LEVELS = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
}


def fake_record(
    logger,
    msg="This is a message",
    instance_name="172.1.1.1:10000",
    handler_index=0,
    name_logger=None,
    level=deflogging.DEBUG,
    filename="fn",
    lno=0,
    args=(),
    exc_info=None,
    extra={},
):
    """
    Fake log records using the format from the logger handler.

    Parameters
    ----------
    logger : logging.Logger
        A logger object with at least a handler.
    msg : str, optional
        Message to include in the log record. By default 'This is a message'
    instance_name : str, optional
        Name of the instance. By default '172.1.1.1:10000'
    handler_index : int, optional
        Index of the selected handler in case you want to test a handler different than
        the first one. By default 0
    level : int, optional
        Logging level, by default deflogging.DEBUG
    filename : str, optional
        Name of the file name. [FAKE]. By default 'fn'
    lno : int, optional
        Line where the fake log is recorded [FAKE]. By default 0
    args : tuple, optional
        Other arguments. By default ()
    exc_info : [type], optional
        Exception information. By default None
    extra : dict, optional
        Extra arguments, one of them should be 'instance_name'. By default {}
    """
    sinfo = None
    if not name_logger:
        name_logger = logger.name

    if "instance_name" not in extra.keys():
        extra["instance_name"] = instance_name

    record = logger.makeRecord(
        name_logger,
        level,
        filename,
        lno,
        msg,
        args=args,
        exc_info=exc_info,
        extra=extra,
        sinfo=sinfo,
    )
    handler = logger.handlers[handler_index]
    return handler.format(record)


# if you enable this test remove -s from addopts [tool.pytest.ini_options]
# @pytest.mark.remote_session_launch
# def test_stdout_reading(capfd):
#     print("This is a test")
#
#     out, err = capfd.readouterr()
#     assert out == "This is a test\n"


@pytest.mark.remote_session_launch
def test_only_logger(caplog):
    log_a = deflogging.getLogger("test")
    log_a.setLevel("DEBUG")

    log_a.debug("This is another test")
    assert "This is another test" in caplog.text


@pytest.mark.remote_session_launch
def test_global_logger_exist():
    assert isinstance(LOG.logger, deflogging.Logger)
    assert LOG.logger.name == "pymechanical_global"


@pytest.mark.remote_session_launch
def test_global_logger_has_handlers():
    assert hasattr(LOG, "file_handler")
    assert hasattr(LOG, "std_out_handler")
    assert LOG.logger.hasHandlers
    assert LOG.file_handler or LOG.std_out_handler  # at least a handler is not empty


@pytest.mark.remote_session_launch
def test_global_logger_logging(caplog):
    LOG.logger.setLevel("DEBUG")
    LOG.std_out_handler.setLevel("DEBUG")
    for each_log_name, each_log_number in LOG_LEVELS.items():
        msg = f"This is an {each_log_name} message."
        LOG.logger.log(each_log_number, msg)
        # Make sure we are using the right logger, the right level and message.
        assert caplog.record_tuples[-1] == (
            "pymechanical_global",
            each_log_number,
            msg,
        )


@pytest.mark.remote_session_launch
def test_global_logger_debug_mode():
    assert isinstance(LOG.logger.level, int)


@pytest.mark.remote_session_launch
def test_global_logger_exception_handling(caplog):
    exc = "Unexpected exception"
    with caplog.at_level(logging.ERROR):
        with pytest.raises(Exception):
            LOG.error(exc)  # Log the exception before raising
            raise Exception(exc)

    assert exc in caplog.text


@pytest.mark.remote_session_launch
def test_global_logger_debug_levels(caplog):
    """Testing for all the possible logging level that the output is recorded
    properly for each type of msg.
    """
    for each_level in [
        deflogging.DEBUG,
        deflogging.INFO,
        deflogging.WARN,
        deflogging.ERROR,
        deflogging.CRITICAL,
    ]:
        with caplog.at_level(each_level, LOG.logger.name):  # changing root logger level:
            for each_log_name, each_log_number in LOG_LEVELS.items():
                msg = f"This is an {each_log_name} message."
                LOG.logger.log(each_log_number, msg)
                # Make sure we are using the right logger, the right level and message.
                if each_log_number >= each_level:
                    assert caplog.record_tuples[-1] == (
                        "pymechanical_global",
                        each_log_number,
                        msg,
                    )
                else:
                    assert caplog.record_tuples[-1] != (
                        "pymechanical_global",
                        each_log_number,
                        msg,
                    )


@pytest.mark.skipif(not HAS_GRPC, reason="Requires GRPC")
@pytest.mark.remote_session_launch
def test_global_logger_format():
    # Since we cannot read the format of our logger, because pytest just don't
    # show the console output or if it does, it formats the logger with its
    # own formatter, we are going to check the logger handlers and output by faking a record.
    # This method is not super robust, since we are input fake data to ``logging.makeRecord``.
    # There are things such as filename or class that we cannot evaluate without going
    # into the code.

    assert "instance" in logging.FILE_MSG_FORMAT
    assert "instance" in logging.STDOUT_MSG_FORMAT

    log = fake_record(
        LOG.logger,
        msg="This is a message",
        level=deflogging.DEBUG,
        extra={"instance_name": "172.1.1.1"},
    )
    assert re.findall("(?:[0-9]{1,3}\\.){3}[0-9]{1,3}", log)
    assert "DEBUG" in log
    assert "This is a message" in log


@pytest.mark.skipif(not HAS_GRPC, reason="Requires GRPC")
@pytest.mark.remote_session_launch
def test_instance_logger_format(mechanical):
    # Since we cannot read the format of our logger, because pytest just dont show the
    # console output or     # if it does, it formats the logger with its own formatter,
    # we are going to check the logger handlers and output by faking a record.
    # This method is not super robust, since we are input fake data to ``logging.makeRecord``.
    # There are things such as filename or class that we cannot evaluate without going
    # into the code.

    log = fake_record(
        mechanical._log.logger,
        msg="This is a message",
        level=deflogging.DEBUG,
        extra={"instance_name": "172.1.1.1"},
    )
    assert re.findall("(?:[0-9]{1,3}\\.){3}[0-9]{1,3}", log)
    assert "DEBUG" in log
    assert "This is a message" in log


@pytest.mark.remote_session_launch
def test_global_methods(caplog):
    LOG.logger.setLevel("DEBUG")
    LOG.std_out_handler.setLevel("DEBUG")

    msg = "This is a debug message"
    LOG.debug(msg)
    assert msg in caplog.text

    msg = "This is an info message"
    LOG.info(msg)
    assert msg in caplog.text

    msg = "This is a warning message"
    LOG.warning(msg)
    assert msg in caplog.text

    msg = "This is an error message"
    LOG.error(msg)
    assert msg in caplog.text

    msg = "This is a critical message"
    LOG.critical(msg)
    assert msg in caplog.text

    msg = 'This is a 30 message using "log"'
    LOG.log(30, msg)
    assert msg in caplog.text


@pytest.mark.remote_session_launch
def test_log_to_file(tmpdir):
    """Testing writing to log file.
    Since the default loglevel of LOG is error, debug are not normally recorded to it.
    """
    file_path = str(Path(tmpdir) / "instance.log")
    file_msg_error = "This is a error message"
    file_msg_debug = "This is a debug message"

    # The LOG loglevel is changed in previous test,
    # hence making sure now it is the "default" one.
    LOG.logger.setLevel("ERROR")
    LOG.std_out_handler.setLevel("ERROR")

    if not LOG.file_handler:
        LOG.log_to_file(file_path)

    LOG.error(file_msg_error)
    LOG.debug(file_msg_debug)
    file_path = Path(file_path)
    with file_path.open("r") as fid:
        text = "".join(fid.readlines())

    assert file_msg_error in text
    assert file_msg_debug not in text
    assert "ERROR" in text
    assert "DEBUG" not in text

    LOG.logger.setLevel("DEBUG")
    for each_handler in LOG.logger.handlers:
        each_handler.setLevel("DEBUG")

    file_msg_error = "This debug message should be recorded."
    LOG.error(file_msg_debug)

    file_msg_warning = "This warning message should be recorded."
    LOG.warning(file_msg_warning)

    file_msg_info = "This info message should be recorded."
    LOG.info(file_msg_info)

    file_msg_debug = "This debug message should be recorded."
    LOG.debug(file_msg_debug)

    with file_path.open("r") as fid:
        text = "".join(fid.readlines())

    assert file_msg_error in text
    assert file_msg_warning in text
    assert file_msg_info in text
    assert file_msg_debug in text


@pytest.mark.remote_session_launch
def test_log_instance_name(mechanical):
    # verify we can access via an instance name
    LOG[mechanical.name] == mechanical._log

    with pytest.raises(KeyError):
        LOG[mechanical.name + "something"]


@pytest.mark.remote_session_launch
def test_instance_log_to_file(mechanical, tmpdir):
    """Testing writing to log file.

    Since the default loglevel of LOG is error, debug are not normally recorded to it.
    """
    file_path = str(Path(tmpdir) / "instance.log")
    file_msg_error = "This is a error message"
    file_msg_debug = "This is a debug message"

    if not mechanical._log.file_handler:
        mechanical._log.log_to_file(file_path)

    mechanical.log_message("ERROR", file_msg_error)
    mechanical.log_message("DEBUG", file_msg_debug)

    file_path = Path(file_path)
    with file_path.open("r") as fid:
        text = "".join(fid.readlines())

    assert file_msg_error in text
    assert file_msg_debug not in text
    assert "ERROR" in text
    assert "DEBUG" not in text

    # Set the logging level to 'DEBUG'
    # All the logging levels are recorded
    mechanical._log.logger.setLevel("DEBUG")
    for each_handler in mechanical._log.logger.handlers:
        each_handler.setLevel("DEBUG")

    mechanical.log_message("ERROR", file_msg_error)

    file_msg_warning = "This is a warning message"
    mechanical.log_message("WARNING", file_msg_warning)

    file_msg_info = "This info message should be recorded."
    mechanical.log_message("INFO", file_msg_info)

    file_msg_debug = "This debug message should be recorded."
    mechanical.log_message("DEBUG", file_msg_debug)

    # disable logging
    mechanical._disable_logging = True
    file_msg_error_not_recorded = "This error message will not be recorded."
    mechanical.log_message("ERROR", file_msg_error_not_recorded)

    file_msg_warning_not_recorded = "This warning message should be recorded."
    mechanical.log_message("WARNING", file_msg_warning_not_recorded)

    file_msg_info_not_recorded = "This info message will not be recorded."
    mechanical.log_message("INFO", file_msg_info_not_recorded)

    file_msg_debug_not_recorded = "This debug message will not be recorded."
    mechanical.log_message("DEBUG", file_msg_debug_not_recorded)

    # enable logging
    mechanical._disable_logging = False

    with file_path.open("r") as fid:
        text = "".join(fid.readlines())

    assert file_msg_error in text
    assert file_msg_warning in text
    assert file_msg_info in text
    assert file_msg_error in text

    assert file_msg_error_not_recorded not in text
    assert file_msg_warning_not_recorded not in text
    assert file_msg_info_not_recorded not in text
    assert file_msg_debug_not_recorded not in text


@pytest.mark.remote_session_launch
def test_lowercases():
    # test that all loggers are lowercase
    for each_loglevel in LOG_LEVELS.keys():
        LOG.setLevel(each_loglevel.lower())

        for each_logger in LOG._instances.values():
            each_logger.setLevel(each_loglevel.lower())
