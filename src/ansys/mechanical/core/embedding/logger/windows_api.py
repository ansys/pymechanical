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

"""Windows API for internal Mechanical logging.

.. note::
   This API does not support some options, namely the base directory
   and log filename.

"""

import logging

from ansys.mechanical.core.embedding.logger import sinks


def _get_logger():
    import clr

    try:
        clr.AddReference("Ans.Common.WB1ManagedUtils")
        import Ansys

        return Ansys.Common.WB1ManagedUtils.Logger
    except:
        raise Exception("Logging cannot be used until after Mechanical embedding is initialized.")


def _get_sink_id(standard_sink_type: int) -> int:
    """Convert standard sink type to sink ID."""
    sink_enum = _get_logger().StandardSinks
    return {
        sinks.StandardSinks.STANDARD_LOG_FILE: sink_enum.StandardLogFile,
        sinks.StandardSinks.CONSOLE: sink_enum.Console,
        sinks.StandardSinks.WINDOWS_DEBUGGER: sink_enum.WindowsDebugger,
        sinks.StandardSinks.WINDOWS_ERROR_MESSAGE_BOX: sink_enum.WindowsErrorMessageBox,
        sinks.StandardSinks.WINDOWS_FATAL_MESSAGE_BOX: sink_enum.WindowsFatalMessageBox,
    }[standard_sink_type]


def _to_wb_logger_severity(level: int):
    """Convert to internal enum."""
    if level <= logging.DEBUG:
        # Level 0 in Workbench logging is trace. Level 1 is debug.
        # Python logging.DEBUG implies trace.
        return _get_logger().LoggerSeverity.Trace
    elif level <= logging.INFO:
        return _get_logger().LoggerSeverity.Info
    elif level <= logging.WARNING:
        return _get_logger().LoggerSeverity.Warning
    elif level <= logging.ERROR:
        return _get_logger().LoggerSeverity.Error
    elif level <= logging.CRITICAL:
        return _get_logger().LoggerSeverity.Fatal
    else:
        # default to info
        return _get_logger().LoggerSeverity.Info


class APIBackend:
    """Provides API backend for Mechanical logging system."""

    def flush(self) -> None:
        """Flush the log manually."""
        return _get_logger().Flush()

    def enable(self, sink: int = sinks.StandardSinks.CONSOLE) -> None:
        """Enable logging."""
        sinkid = _get_sink_id(sink)
        _get_logger().Configuration.EnableSink(sinkid)

    def disable(self, sink: int = sinks.StandardSinks.CONSOLE) -> None:
        """Disable logging."""
        sinkid = _get_sink_id(sink)
        _get_logger().Configuration.DisableSink(sinkid)

    def set_log_level(self, level: int, sink: int = sinks.StandardSinks.CONSOLE) -> None:
        """Set the log level for Mechanical based on the Python log level."""
        if level == logging.NOTSET:
            self.disable(sink)

        sinkid = _get_sink_id(sink)
        wb_level = _to_wb_logger_severity(level)
        _get_logger().Configuration.SetSinkFilterLevel(sinkid, wb_level)

    def set_auto_flush(self, flush: bool) -> None:
        """Set whether to auto flush to the standard log file."""
        _get_logger().Configuration.StandardLogAutoFlush = flush

    def set_directory(self, directory: str) -> None:
        """Set the location to write the log file to."""
        _get_logger().Configuration.StandardLogDirectory = directory

    def set_base_directory(self, base_directory: str) -> None:
        """Set the base location to write the log file to.

        The base directory contains time-stamped subfolders where the log file
        is actually written to. If a base directory is set, it takes precedence over the
        ``set_directory`` location.

        This does not have an API to set at runtime.
        """
        raise Exception("Base directory can only be set before starting the Mechanical instance.")

    def can_log_message(self, level: int) -> bool:
        """Return whether a message with the given severity is outputted to the log."""
        wb_level = _to_wb_logger_severity(level)
        return _get_logger().CanLogMessage(wb_level)

    def log_message(self, level: int, context: str, message: str) -> None:
        """Log the message to the configured logging mechanism."""
        wb_level = _to_wb_logger_severity(level)
        _get_logger().LogMessage(wb_level, context, message)
