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

"""Logging module.

This module supplies the general framework for logging in PyMechanical. This module is
built upon the `logging <https://docs.python.org/3/library/logging.html>`_ package.
The intent is not for this module to replace the ``logging`` package but rather to provide
a way for the ``logging`` package and PyMechancial to interact.

The loggers used in the module include the name of the instance, which
is intended to be unique.  This name is printed in all the active
outputs and is used to track the different Mechanical instances.


Usage
-----

Global logger
~~~~~~~~~~~~~
There is a global logger named ``pymechanical_global``, which is created at
``ansys.mechanical.core.__init__``.  If you want to use this global logger,
you must call it at the top of your module:

.. code:: python

   from ansys.mechanical.core import LOG

You can rename this logger to avoid conflicts with other loggers (if any):

.. code:: python

   from ansys.mechanical.core import LOG as logger


The default logging level of ``LOG`` is ``ERROR``. To change this and output
lower-level messages, you can use this code:

.. code:: python

   LOG.logger.setLevel("DEBUG")
   LOG.file_handler.setLevel("DEBUG")  # If present.
   LOG.stdout_handler.setLevel("DEBUG")  # If present.


Alternatively, you can use this code:

.. code:: python

   LOG.setLevel("DEBUG")

This alternative code ensures that all the handlers are set to the
input log level.

By default, this logger does not log to a file. If you want,
you can add a file handler:

.. code:: python

   import os

   file_path = os.path.join(os.getcwd(), "pymechanical.log")
   LOG.log_to_file(file_path)

The preceding code sets the logger to also be redirected to this file. If you
want to change the characteristics of this global logger from the beginning
of the execution, you must edit the file ``__init__`` in the
``ansys.mechanical.core`` directory.

To log using this logger, call the desired method as a normal logger:

.. code:: pycon

    >>> import logging
    >>> from ansys.mechanical.core.logging import Logger
    >>> LOG = Logger(level=logging.DEBUG, to_file=False, to_stdout=True)
    >>> LOG.debug("This is LOG debug message.")

    DEBUG -  -  <ipython-input-24-80df150fe31f> - <module> - This is the LOG debug message.


Instance Logger
~~~~~~~~~~~~~~~
Every time an instance of the :class:`Mechanical <ansys.mechanical.core.mechanical.Mechanical>`
ckass is created, a logger is created and stored here:

* ``LOG._instances``. This field is a ``dict`` where the key is the name of the
  created logger.

These logger instances inherit the ``pymechanical_global`` output handlers and
logging level unless otherwise specified. The way this logger works is very
similar to the global logger. You can add a file handler if you want using the
:func:`log_to_file() <PyMechanicalCustomAdapter.log_to_file>` method or change
the log level using the :func:`logger.Logging.setLevel` method.

You can use this logger like this:

.. code:: pycon

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mechanical = launch_mechanical()
    >>> mechanical.log.info("This is a useful message")

    INFO - GRPC_127.0.0.1:50056 -  <ipython-input-19-f09bb2d8785c> - <module> -
    This is a useful message

Other loggers
~~~~~~~~~~~~~
You can create your own loggers using the Python ``logging`` package as
you would do in any other script. There are no conflicts between these loggers.

"""

from copy import copy
from datetime import datetime
import logging
import sys
import weakref

# Default configuration
LOG_LEVEL = logging.DEBUG
"""Default log level configuration."""
FILE_NAME = "pymechanical.log"
"""Default file name."""

# For convenience
DEBUG = logging.DEBUG
"""Constant for logging.DEBUG."""
INFO = logging.INFO
"""Constant for logging.INFO."""
WARN = logging.WARN
"""Constant for logging.WARN."""
ERROR = logging.ERROR
"""Constant for logging.ERROR."""
CRITICAL = logging.CRITICAL
"""Constant for logging.CRITICAL."""

# Formatting
STDOUT_MSG_FORMAT = "%(levelname)s - %(instance_name)s -  %(module)s - %(funcName)s - %(message)s"
"""Standard output message format."""

FILE_MSG_FORMAT = STDOUT_MSG_FORMAT
"""File message format."""

DEFAULT_STDOUT_HEADER = """
LEVEL - INSTANCE NAME - MODULE - FUNCTION - MESSAGE
"""
"""Default standard output header."""

DEFAULT_FILE_HEADER = DEFAULT_STDOUT_HEADER
"""Default file header."""

NEW_SESSION_HEADER = f"""
===============================================================================
       NEW SESSION - {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
==============================================================================="""
"""Default new session header containing date and time."""

string_to_loglevel = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARN": logging.WARN,
    "WARNING": logging.WARN,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class PyMechanicalCustomAdapter(logging.LoggerAdapter):
    """Keeps the reference to the name of the Mechanical instance dynamic.

    The standard approach supplies extra input to the logger. If this approach
    was used, Mechanical instances would have to be inputted every time a log
    is created.

    Using an adapter means that the reference to the Mechanical instance must only
    be specified once.
    """

    level = (
        None  # This is maintained for compatibility with ``suppress_logging``, but it does nothing.
    )
    file_handler = None
    stdout_handler = None

    def __init__(self, logger, extra=None):
        """Initialize the PyMechanical custom adapter."""
        # super().__init__(logger,extra)

        self.logger = logger
        if extra is not None:
            self.extra = weakref.proxy(extra)
        else:
            self.extra = None
        self.file_handler = logger.file_handler
        self.std_out_handler = logger.std_out_handler

    def process(self, msg, kwargs):
        """Process the message."""
        kwargs["extra"] = {}
        # These are the extra parameters to send to the log.
        kwargs["extra"][
            "instance_name"
        ] = self.extra.name  # Here self.extra is the argument to pass to the log records.
        return msg, kwargs

    def log_to_file(self, filename=FILE_NAME, level=LOG_LEVEL):
        """Add a file handler to the logger.

        Parameters
        ----------
        filename : str, optional
            Name of the file where logs are recorded. The default is ``FILE_NAME``.
        level : str, optional
            Level of logging. The default is ``None``, in which case the ``"DEBUG"``
            level is used. Options are ``"DEBUG"``, ``"INFO"``, ``"WARNING"``,
            and ``"ERROR"``.
        """
        self.logger = addfile_handler(
            self.logger, filename=filename, level=level, write_headers=True
        )
        self.file_handler = self.logger.file_handler

    def log_to_stdout(self, level=LOG_LEVEL):
        """Add a standard output handler to the logger.

        Parameters
        ----------
        level : str, optional
            Level of logging. The default is ``None``, in which case the ``"DEBUG"``
            level is used. Options are ``"DEBUG"``, ``"INFO"``, ``"WARNING"``,
            and ``"ERROR"``.
        """
        if self.std_out_handler:
            raise Exception("Stdout logger is already defined.")

        self.logger = add_stdout_handler(self.logger, level=level)
        self.std_out_handler = self.logger.std_out_handler

    def setLevel(self, level="DEBUG"):
        """Change the log level of the object and the attached handlers.

        Parameters
        ----------
        level : str, optional
            Level of logging. The default is ``"DEBUG"``. Options are ``"DEBUG"``,
            ``"INFO"``, ``"WARNING"``, and ``"ERROR"``.
        """
        if isinstance(level, str):
            level = string_to_loglevel[level.upper()]
        self.logger.setLevel(level)
        for each_handler in self.logger.handlers:
            each_handler.setLevel(level)
        self.level = level


class PyMechanicalPercentStyle(logging.PercentStyle):
    """Controls the way PyMechanical formats the percent style."""

    def __init__(self, fmt, *, defaults=None):
        """Initialize the PyMechanical percent style."""
        # super().__init__(fmt)

        self._fmt = fmt or self.default_format
        self._defaults = defaults

    def _format(self, record):
        defaults = self._defaults
        if defaults:
            values = defaults | record.__dict__
        else:
            values = record.__dict__

        # We can do here any changes we want in record, for example adding a key.

        # We could create an if here if we want conditional formatting, and even
        # change the record.__dict__.
        # Since now we don't want to create conditional fields, it is fine to keep
        # the same MSG_FORMAT for all of them.

        # For the case of logging exceptions to the logger.
        values.setdefault("instance_name", "")

        return STDOUT_MSG_FORMAT % values


class PyMechanicalFormatter(logging.Formatter):
    """Provides for overwriting default format styles with custom format styles.

    Parameters
    ----------
    fmt : optional
        The default is ``STDOUT_MSG_FORMAT``.
    datefmt : optional
        The default is ``None``.
    style : optional
        The default is ``%``.
    validate : bool, optional
        The default is ``None``.
    """

    def __init__(
        self,
        fmt=STDOUT_MSG_FORMAT,
        datefmt=None,
        style="%",
        validate=True,
        defaults=None,
    ):
        """Initialize the PyMechanical formatter."""
        if sys.version_info[1] < 8:  # pragma: no cover
            super().__init__(fmt, datefmt, style)
        else:
            # 3.8: The validate parameter was added
            super().__init__(fmt, datefmt, style, validate)
        self._style = PyMechanicalPercentStyle(fmt, defaults=defaults)  # overwriting


class InstanceFilter(logging.Filter):
    """Ensures that the instance name record always exists."""

    def filter(self, record):
        """Check the log record and return ``True`` to log it or ``False`` to discard it."""
        if not hasattr(record, "instance_name"):
            record.instance_name = ""
        return True


class Logger:
    """Provides for adding handlers to the logger for each Mechanical session.

    This class allows you to add handlers to the logger to output to a file or
    the standard output.

    Parameters
    ----------
    level : int, optional
        Logging level for filtering the messages that are allowed in the logger.
        The default is ``10``, in which case the ``DEBUG`` level is used.
    to_file : bool, optional
        Whether to write log messages to a file. The default is ``False``.
    to_stdout : bool, optional
        Whether to write log messages to the standard output. The default is
        ``True``.
    filename : str, optional
        Name of the file to write log messages to. The default is ``pymechanical.log``.

    Examples
    --------
    Demonstrate logger usage from a Mechanical instance. The logger is automatically
    created when a Mechanical instance is created.

    >>> from ansys.mechanical.core import launch_mechanical
    >>> mechanical = launch_mechanical(loglevel='DEBUG')
    >>> mechanical.log.info('This is a useful message')
    INFO -  -  <ipython-input-24-80df150fe31f> - <module> - This is LOG debug message.

    Import the PyMechanical global logger and add a file output handler.

    >>> import os
    >>> from ansys.mechanical.core import LOG
    >>> file_path = os.path.join(os.getcwd(), 'pymechanical.log')
    >>> LOG.log_to_file(file_path)

    """

    file_handler = None
    std_out_handler = None
    _level = logging.DEBUG
    _instances = {}

    def __init__(self, level=logging.DEBUG, to_file=False, to_stdout=True, filename=FILE_NAME):
        """Customize the logger for PyMechanical.

        Parameters
        ----------
        level : int, optional
            Level of logging that is defined in the ``logging`` package. The default is 'DEBUG'.
            Options are ``"DEBUG"``, ``"INFO"``, ``"WARNING"``, and ``"ERROR"``.
        to_file : bool, optional
            Whether to write log messages to a file. The default is  ``False``.
        to_stdout : bool, optional
            Whether to write log messages to the standard output, which is the
            command line. The default is ``True``.
        filename : str, optional
            Name of the output file. The default is ``pymechanical.log``.
        """
        # Create default main logger.
        self.logger = logging.getLogger("pymechanical_global")
        self.logger.addFilter(InstanceFilter())
        self.logger.setLevel(level)
        self.logger.propagate = True
        self.level = self.logger.level  # TODO: TO REMOVE

        # Write logging methods.
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
        self.log = self.logger.log

        if to_file or filename != FILE_NAME:
            # Record to a file.
            self.log_to_file(filename=filename, level=level)

        if to_stdout:
            self.log_to_stdout(level=level)

        # Use logger to record unhandled exceptions.
        self.add_handling_uncaught_exceptions(self.logger)

    def log_to_file(self, filename=FILE_NAME, level=LOG_LEVEL):
        """Add a file handler to the logger.

        Parameters
        ----------
        filename : str, optional
            Name of the file to write log messages to. The default is
            ``'pymechanical.log'``.
        level : str, optional
            Level of logging. The default is ``10``, in which case the ``"DEBUG"``
            level is used. Options are ``"DEBUG"``, ``"INFO"``,
            ``"WARNING"`` and ``"ERROR"``.

        Examples
        --------
        Write to the ``pymechanical.log`` file in the current working directory.

        >>> from ansys.mechanical.core import LOG
        >>> import os
        >>> file_path = os.path.join(os.getcwd(), 'pymechanical.log')
        >>> LOG.log_to_file(file_path)

        """
        addfile_handler(self, filename=filename, level=level, write_headers=True)

    def log_to_stdout(self, level=LOG_LEVEL):
        """Add a standard output handler to the logger.

        Parameters
        ----------
        level : str, optional
            Level of logging, such as ``DUBUG``. The default is ``LOG_LEVEL``.
        """
        add_stdout_handler(self, level=level)

    def setLevel(self, level="DEBUG"):
        """Change the log level of the object and the attached handlers.

        Parameters
        ----------
        level : str, optional
            Level of logging, such as ``DUBUG``. The default is ``LOG_LEVEL``.
        """
        if isinstance(level, str):
            level = string_to_loglevel[level.upper()]
        self.logger.setLevel(level)
        for each_handler in self.logger.handlers:
            each_handler.setLevel(level)
        self.level = level

    def _make_child_logger(self, suffix, level):
        """Create a child logger.

        Uses the ``getChild`` method to copy attributes between  the ``pymechanical_global``
        logger and a new child logger.

        Parameters
        ----------
        suffix : str
            Name for the child logger.
        level : str, optional
            Level of logging, such as ``DUBUG``. The default is ``LOG_LEVEL``.
        """
        logger = logging.getLogger(suffix)
        logger.std_out_handler = None
        logger.file_handler = None

        if self.logger.hasHandlers:
            for each_handler in self.logger.handlers:
                new_handler = copy(each_handler)

                if each_handler == self.file_handler:
                    logger.file_handler = new_handler
                elif each_handler == self.std_out_handler:
                    logger.std_out_handler = new_handler

                if level:
                    # The logger handlers are copied and changed the loglevel is
                    # the specified log level is lower than the one of the
                    # global.
                    if each_handler.level > string_to_loglevel[level.upper()]:
                        new_handler.setLevel(level)

                logger.addHandler(new_handler)

        if level:
            if isinstance(level, str):
                level = string_to_loglevel[level.upper()]
            logger.setLevel(level)

        else:
            logger.setLevel(self.logger.level)

        logger.propagate = True
        return logger

    def add_child_logger(self, suffix, level=None):
        """Add a child logger to the main logger.

        This child logger is more general than an instance logger, which is designed to
        track the state of a Mechanical instance.

        If the logging level is specified in the arguments, a new logger with a reference
        to the ``_global`` logger handlers is created instead of a child logger.

        Parameters
        ----------
        suffix : str
            Name for the child logger.
        level : str, optional
            Level of logging. The default is ``None``, in which case the ``"DEBUG"``
            level is used. Options are ``"DEBUG"``, ``"INFO"``, ``"WARNING"``,
            and ``"ERROR"``.

        Returns
        -------
        logging.logger
            Logger class.
        """
        name = self.logger.name + "." + suffix
        self._instances[name] = self._make_child_logger(name, level)
        return self._instances[name]

    def _add_mechanical_instance_logger(self, name, mechanical_instance, level):
        if isinstance(name, str):
            instance_logger = PyMechanicalCustomAdapter(
                self._make_child_logger(name, level), mechanical_instance
            )
        elif name is None:
            instance_logger = PyMechanicalCustomAdapter(
                self._make_child_logger("NO_NAMED_YET", level), mechanical_instance
            )
        else:
            raise ValueError("You can only input 'str' classes to this method.")

        return instance_logger

    def add_instance_logger(self, name, mechanical_instance, level=None):
        """Add a logger for a Mechanical instance.

        The logger for a Mechanical instance has an adapter that adds contextual information,
        such as the name of the Mechanical instance. This logger is returned, and you can use it to
        log events as a normal logger. It is also stored in the ``_instances`` field.

        Parameters
        ----------
        name : str
            Name for the new logger.
        mechanical_instance : ansys.mechanical.core.mechanical.Mechanical
            Mechanical instance object. This object should contain the ``name``
            attribute.
        level : str, optional
            Level of logging. The default is ``None``, in which case the ``"DEBUG"``
            level is used. Options are ``"DEBUG"``, ``"INFO"``, ``"WARNING"``,
            and ``"ERROR"``.

        Returns
        -------
        ansys.mechanical.core.logging.PyMechanicalCustomAdapter
            Logger adapter customized to add Mechanical information to the
            logs. You can use this class to log events in the same
            way you would with the ``logger`` class.

        Raises
        ------
        Exception
            You can only input strings as ``name`` to this method.
        """
        count_ = 0
        new_name = name
        while new_name in logging.root.manager.__dict__.keys():
            count_ += 1
            new_name = name + "_" + str(count_)

        self._instances[new_name] = self._add_mechanical_instance_logger(
            new_name, mechanical_instance, level
        )
        return self._instances[new_name]

    def __getitem__(self, key):
        """Get the instance logger based on a key.

        Parameters
        ----------
            key :
        """
        if key in self._instances.keys():
            return self._instances[key]
        else:
            raise KeyError(
                f"There is no instances with name {key}. "
                f"Available keys are {self._instances.keys()}"
            )

    @staticmethod
    def add_handling_uncaught_exceptions(logger):
        """Redirect the output of an exception to a logger.

        Parameters
        ----------
        logger : str
            Name of the logger.
        """

        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

        sys.excepthook = handle_exception


def addfile_handler(logger, filename=FILE_NAME, level=LOG_LEVEL, write_headers=False):
    """Add a file handler to the input.

    Parameters
    ----------
    logger : logging.Logger or logging.Logger
        Logger to add the file handler to.
    filename : str, optional
        Name of the output file. The default is ``FILE_NAME``.
    level : str, optional
        Level of logging. The default is ``None``. Options are ``"DEBUG"``, ``"INFO"``,
        ``"WARNING"`` and ``"ERROR"``.
    write_headers : bool, optional
        Whether to write headers to the file. The default is ``False``.

    Returns
    -------
    logger
        Logger object.
    """
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(FILE_MSG_FORMAT))

    if isinstance(logger, Logger):
        logger.file_handler = file_handler
        logger.logger.addHandler(file_handler)

    elif isinstance(logger, logging.Logger):
        logger.file_handler = file_handler
        logger.addHandler(file_handler)

    if write_headers:
        file_handler.stream.write(NEW_SESSION_HEADER)
        file_handler.stream.write(DEFAULT_FILE_HEADER)

    return logger


def add_stdout_handler(logger, level=LOG_LEVEL, write_headers=False):
    """Add a file handler to the stand output handler.

    Parameters
    ----------
    logger : logging.Logger or logging.Logger
        Logger to add the file handler to.
    level : str, optional
        Level of logging. The default is ``None``. Options are ``"DEBUG"``, ``"INFO"``,
        ``"WARNING"`` and ``"ERROR"``.
    write_headers : bool, optional
        Whether to write headers to the file. The default is ``False``.

    Returns
    -------
    logger
        Logger object.
    """
    std_out_handler = logging.StreamHandler()
    std_out_handler.setLevel(level)
    std_out_handler.setFormatter(PyMechanicalFormatter(STDOUT_MSG_FORMAT))

    if isinstance(logger, Logger):
        logger.std_out_handler = std_out_handler
        logger.logger.addHandler(std_out_handler)

    elif isinstance(logger, logging.Logger):
        logger.addHandler(std_out_handler)

    if write_headers:
        std_out_handler.stream.write(DEFAULT_STDOUT_HEADER)

    return logger
