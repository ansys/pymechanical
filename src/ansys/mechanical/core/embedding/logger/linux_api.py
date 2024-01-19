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

"""Internal Mechanical logging Linux API.

.. note::
   The Linux API is needed for version 2023 R2, where the .NET backend is Windows-only.
   This API does not support some options, namely the base directory and log filename.

"""

import ctypes
import logging
import os

from ansys.mechanical.core.embedding import initializer
from ansys.mechanical.core.embedding.logger import sinks


def _get_dll():
    installdir = os.environ[f"AWP_ROOT{initializer.INITIALIZED_VERSION}"]
    dll = ctypes.CDLL(os.path.join(installdir, "aisol/dll/linx64/libAns.Common.WBLogger.so"))

    dll.wb_logger_enable_sink.argtypes = [ctypes.c_int32]

    dll.wb_logger_disable_sink.argtypes = [ctypes.c_int32]

    dll.wb_logger_set_sink_filter_level.argtypes = [ctypes.c_int32, ctypes.c_int32]

    dll.wb_logger_flush.argtypes = []

    dll.wb_logger_set_logging_auto_flush.argtypes = [ctypes.c_int8]

    dll.wb_logger_set_logging_directory.argtypes = [ctypes.c_char_p]

    dll.wb_logger_can_log_message.argtypes = [ctypes.c_int32]
    dll.wb_logger_can_log_message.restype = ctypes.c_int32

    dll.wb_logger_log_message.argtypes = [ctypes.c_int32, ctypes.c_char_p, ctypes.c_char_p]
    return dll


def _get_sink_id(standard_sink_type: int) -> ctypes.c_int32:
    """Convert standard sink type to sink id."""
    return {
        sinks.StandardSinks.STANDARD_LOG_FILE: ctypes.c_int32(1),
        sinks.StandardSinks.CONSOLE: ctypes.c_int32(2),
    }[standard_sink_type]


def _str_to_utf8_ptr(value: str) -> ctypes.c_char_p:
    return ctypes.create_string_buffer(value.encode())


def _bool_to_single_byte_int(value: bool) -> ctypes.c_int8:
    if value:
        return ctypes.c_int8(1)
    return ctypes.c_int8(0)


def _to_wb_logger_severity(level: int) -> ctypes.c_int32:
    """Convert to internal integer."""
    if level <= logging.DEBUG:
        # Level 0 in Workbench logging is trace. Level 1 is debug.
        # Python logging.DEBUG implies trace.
        return ctypes.c_int32(0)
    elif level <= logging.INFO:
        return ctypes.c_int32(2)
    elif level <= logging.WARNING:
        return ctypes.c_int32(3)
    elif level <= logging.ERROR:
        return ctypes.c_int32(4)
    elif level <= logging.CRITICAL:
        return ctypes.c_int32(5)
    else:
        # default to info
        return ctypes.c_int32(2)


class APIBackend:
    """Provides the API backend for the Mechanical logging system."""

    def flush(self) -> None:
        """Flush the log manually."""
        return _get_dll().wb_logger_flush()

    def enable(self, sink: int = sinks.StandardSinks.CONSOLE) -> None:
        """Enable logging."""
        sinkid = _get_sink_id(sink)
        _get_dll().wb_logger_enable_sink(sinkid)

    def disable(self, sink: int = sinks.StandardSinks.CONSOLE) -> None:
        """Disable logging."""
        sinkid = _get_sink_id(sink)
        _get_dll().wb_logger_disable_sink(sinkid)

    def set_log_level(self, level: int, sink: int = sinks.StandardSinks.CONSOLE) -> None:
        """Set the log level for Mechanical based on the Python log level."""
        if level == logging.NOTSET:
            self.disable(sink)

        sinkid = _get_sink_id(sink)
        wb_level = _to_wb_logger_severity(level)
        _get_dll().wb_logger_set_sink_filter_level(sinkid, wb_level)

    def set_auto_flush(self, flush: bool) -> None:
        """Set whether to auto flush to the standard log file."""
        flag = _bool_to_single_byte_int(flush)
        _get_dll().wb_logger_set_logging_auto_flush(flag)

    def set_directory(self, directory: str) -> None:
        """Set the location to write the log file to."""
        value = _str_to_utf8_ptr(directory)
        _get_dll().wb_logger_set_logging_directory(value)

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
        return bool(_get_dll().wb_logger_can_log_message(wb_level))

    def log_message(self, level: int, context: str, message: str) -> None:
        """Log the message to the configured logging mechanism."""
        wb_level = _to_wb_logger_severity(level)
        wb_context = _str_to_utf8_ptr(context)
        wb_message = _str_to_utf8_ptr(message)
        _get_dll().wb_logger_log_message(wb_level, wb_context, wb_message)
