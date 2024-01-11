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

"""Environment variables for mechanical logging."""

import logging
import os

from ansys.mechanical.core.embedding.logger import sinks


class EnvironBackend:
    """Provides the environment variable backend for Mechanical logging."""

    def flush(self):
        """Flush the log."""
        raise Exception("The embedding log cannot be flushed until Mechanical is initialized.")

    def enable(self, sink: int = sinks.StandardSinks.CONSOLE):
        """Enable the given sink."""
        os.environ["ANSYS_WORKBENCH_LOGGING"] = "1"
        if sink == sinks.StandardSinks.CONSOLE:
            os.environ["ANSYS_WORKBENCH_LOGGING_CONSOLE"] = "1"
        elif sink == sinks.StandardSinks.WINDOWS_DEBUGGER:
            os.environ["ANSYS_WORKBENCH_LOGGING_DEBUGGER"] = "1"
        elif sink == sinks.StandardSinks.WINDOWS_ERROR_MESSAGE_BOX:
            os.environ["ANSYS_WORKBENCH_LOGGING_ERROR_MESSAGE_BOX"] = "1"
        elif sink == sinks.StandardSinks.WINDOWS_FATAL_MESSAGE_BOX:
            os.environ["ANSYS_WORKBENCH_LOGGING_FATAL_MESSAGE_BOX"] = "1"

    def disable(self, sink: int = sinks.StandardSinks.CONSOLE):
        """Disable the log level for this sink."""
        if sink == sinks.StandardSinks.CONSOLE:
            os.environ["ANSYS_WORKBENCH_LOGGING_CONSOLE"] = "0"
        elif sink == sinks.StandardSinks.WINDOWS_DEBUGGER:
            os.environ["ANSYS_WORKBENCH_LOGGING_DEBUGGER"] = "0"
        elif sink == sinks.StandardSinks.WINDOWS_ERROR_MESSAGE_BOX:
            os.environ["ANSYS_WORKBENCH_LOGGING_ERROR_MESSAGE_BOX"] = "0"
        elif sink == sinks.StandardSinks.WINDOWS_FATAL_MESSAGE_BOX:
            os.environ["ANSYS_WORKBENCH_LOGGING_FATAL_MESSAGE_BOX"] = "0"
        else:
            # only disable global logging if none of the sinks match?
            os.environ["ANSYS_WORKBENCH_LOGGING"] = "0"

    def set_log_level(self, level: int, sink: int = sinks.StandardSinks.CONSOLE):
        """Set the log level for this sink based on the Python log level."""
        if level == logging.NOTSET:
            self.disable(sink)
            return

        if level <= logging.DEBUG:
            # level 0 in workbench logging is trace, level 1 is debug.
            # python logging.DEBUG will imply trace.
            os.environ["ANSYS_WORKBENCH_LOGGING_FILTER_LEVEL"] = "0"
        elif level <= logging.INFO:
            os.environ["ANSYS_WORKBENCH_LOGGING_FILTER_LEVEL"] = "2"
        elif level <= logging.WARNING:
            os.environ["ANSYS_WORKBENCH_LOGGING_FILTER_LEVEL"] = "3"
        elif level <= logging.ERROR:
            os.environ["ANSYS_WORKBENCH_LOGGING_FILTER_LEVEL"] = "4"
        elif level <= logging.CRITICAL:
            os.environ["ANSYS_WORKBENCH_LOGGING_FILTER_LEVEL"] = "5"

    def set_auto_flush(self, flush: bool) -> None:
        """Set whether to auto flush to the standard log file."""
        value = "1" if flush else "0"
        os.environ["ANSYS_WORKBENCH_LOGGING_AUTO_FLUSH"] = value

    def set_directory(self, directory: str) -> None:
        """Set the location to write the log file to."""
        os.environ["ANSYS_WORKBENCH_LOGGING_DIRECTORY"] = directory

    def set_base_directory(self, base_directory: str) -> None:
        """Set the base location to write the log file to.

        The base directory contains time-stamped subfolders where the log file
        is actually written to. If a base directory is set, it takes precedence over the
        ``set_directory`` location.
        """
        os.environ["ANSYS_WORKBENCH_LOGGING_BASE_DIRECTORY"] = base_directory

    def can_log_message(self, level: int) -> bool:
        """Return whether a message with the given severity is outputted to the log."""
        if os.environ.get("ANSYS_WORKBENCH_LOGGING", 0) == 0:
            return False

        wb_int_level = int(os.environ.get("ANSYS_WORKBENCH_LOGGING_FILTER_LEVEL", 2))
        if wb_int_level == 0:
            return True
        if wb_int_level == 1:
            # This is not exactly right. WB might be set to DEBUG but the level expected is trace.
            return True
        if wb_int_level == 2:
            return level >= logging.INFO
        if wb_int_level == 3:
            return level >= logging.WARNING
        if wb_int_level == 4:
            return level >= logging.ERROR
        if wb_int_level == 5:
            return level >= logging.CRITICAL

    def log_message(self, level: int, context: str, message: str) -> None:
        """Log the message to the configured logging mechanism."""
        raise Exception("Can't log to the embedding logger until Mechanical is initialized.")
