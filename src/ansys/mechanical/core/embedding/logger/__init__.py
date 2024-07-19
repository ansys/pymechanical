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

"""Embedding logger.

Module to interact with the built-in logging system of Mechanical.

Usage
-----

Configuring logger
~~~~~~~~~~~~~~~~~~

Configuring the logger can be done using the :class:`Configuration <ansys.mechanical.core.embedding.logger.Configuration>` class:

.. code:: python
  import ansys.mechanical.core as mech
  from ansys.mechanical.core.embedding.logger import Configuration, Logger

  Configuration.configure(level=logging.INFO, to_stdout=True, base_directory=None)
  app = mech.App(version=242)

Then, the :class:`Logger <ansys.mechanical.core.embedding.logger.Logger>` class can be used to write messages to the log:

.. code:: python

   Logger.error("message")


"""

import logging
import os
import typing

from ansys.mechanical.core.embedding import initializer
from ansys.mechanical.core.embedding.logger import environ, linux_api, sinks, windows_api

LOGGING_SINKS: typing.Set[int] = set()
"""Constant for logging sinks."""

LOGGING_CONTEXT: str = "PYMECHANICAL"
"""Constant for logging context."""


def _get_backend() -> (
    typing.Union[windows_api.APIBackend, linux_api.APIBackend, environ.EnvironBackend]
):
    """Get the appropriate logger backend.

    Before embedding is initialized, logging is configured via environment variables.
    After embedding is initialized, logging is configured by making API calls into the
    Mechanical logging system.

    However, the API is mostly the same in both cases, though some methods only work
    in one of the two backends.

    Setting the base directory only works before initializing.
    Actually logging a message or flushing the log only works after initializing.
    """
    # TODO - use abc instead of a union type?
    embedding_initialized = initializer.INITIALIZED_VERSION != None
    if not embedding_initialized:
        return environ.EnvironBackend()
    if os.name == "nt":
        return windows_api.APIBackend()
    return linux_api.APIBackend()


class Configuration:
    """Configures logger for Mechanical embedding."""

    @classmethod
    def configure(cls, level=logging.WARNING, directory=None, base_directory=None, to_stdout=True):
        """Configure the logger for PyMechanical embedding.

        Parameters
        ----------
        level : int, optional
            Level of logging that is defined in the ``logging`` package. The default is 'DEBUG'.
            Options are ``"DEBUG"``, ``"INFO"``, ``"WARNING"``, and ``"ERROR"``.
        directory : str, optional
            Directory to write log file to. The default is ``None``, but by default the log
            will appear somewhere in the system temp folder.
        base_directory: str, optional
            Base directory to write log files to. Each instance of Mechanical will write its
            log to a time-stamped subfolder within this directory. This is only possible to set
            before Mechanical is initialized.
        to_stdout : bool, optional
            Whether to write log messages to the standard output, which is the
            command line. The default is ``True``.
        """
        # Set up the global log configuration.
        cls.set_log_directory(directory)
        cls.set_log_base_directory(base_directory)

        # Set up the sink-specific log configuration and store to global state.
        cls._store_stdout_sink_enabled(to_stdout)
        file_sink_enabled = directory != None or base_directory != None
        cls._store_file_sink_enabled(file_sink_enabled)

        # Commit the sink-specific log configuration global state to the backend.
        cls._commit_enabled_configuration()
        cls.set_log_level(level)

    @classmethod
    def set_log_to_stdout(cls, value: bool) -> None:
        """Configure logging to write to the standard output."""
        cls._store_stdout_sink_enabled(value)
        cls._commit_enabled_configuration()

    @classmethod
    def set_log_to_file(cls, value: bool) -> None:
        """Configure logging to write to a file."""
        cls._store_file_sink_enabled(value)
        cls._commit_enabled_configuration()

    @classmethod
    def set_log_level(cls, level: int) -> None:
        """Set the log level for all configured sinks."""
        if len(LOGGING_SINKS) == 0:
            raise Exception("No logging backend configured!")
        cls._commit_level_configuration(level)

    @classmethod
    def set_log_directory(cls, value: str) -> None:
        """Configure logging to write to a directory."""
        if value == None:
            return
        _get_backend().set_directory(value)

    @classmethod
    def set_log_base_directory(cls, directory: str) -> None:
        """Configure logging to write in a time-stamped subfolder in this directory."""
        if directory == None:
            return
        _get_backend().set_base_directory(directory)

    @classmethod
    def _commit_level_configuration(cls, level: int) -> None:
        for sink in LOGGING_SINKS:
            _get_backend().set_log_level(level, sink)

    @classmethod
    def _commit_enabled_configuration(cls) -> None:
        for sink in LOGGING_SINKS:
            _get_backend().enable(sink)

    @classmethod
    def _store_stdout_sink_enabled(cls, value: bool) -> None:
        if value:
            LOGGING_SINKS.add(sinks.StandardSinks.CONSOLE)
        else:
            LOGGING_SINKS.discard(sinks.StandardSinks.CONSOLE)

    @classmethod
    def _store_file_sink_enabled(cls, value: bool) -> None:
        if value:
            LOGGING_SINKS.add(sinks.StandardSinks.STANDARD_LOG_FILE)
        else:
            LOGGING_SINKS.discard(sinks.StandardSinks.STANDARD_LOG_FILE)


class Logger:
    """Provides the ``Logger`` class for embedding."""

    @classmethod
    def flush(cls):
        """Flush the log."""
        _get_backend().flush()

    @classmethod
    def can_log_message(cls, level: int) -> bool:
        """Get whether a message at this level is logged."""
        return _get_backend().can_log_message(level)

    @classmethod
    def debug(cls, msg: str):
        """Write a debug message to the log."""
        _get_backend().log_message(logging.DEBUG, LOGGING_CONTEXT, msg)

    @classmethod
    def error(cls, msg: str):
        """Write a error message to the log."""
        _get_backend().log_message(logging.ERROR, LOGGING_CONTEXT, msg)

    @classmethod
    def info(cls, msg: str):
        """Write an info message to the log."""
        _get_backend().log_message(logging.INFO, LOGGING_CONTEXT, msg)

    @classmethod
    def warning(cls, msg: str):
        """Write a warning message to the log."""
        _get_backend().log_message(logging.WARNING, LOGGING_CONTEXT, msg)

    @classmethod
    def fatal(cls, msg: str):
        """Write a fatal message to the log."""
        _get_backend().log_message(logging.FATAL, LOGGING_CONTEXT, msg)
