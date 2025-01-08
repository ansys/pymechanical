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

import clr

clr.AddReference("Ans.Common.WB1ManagedUtils")
import time

from Ansys.Common.WB1ManagedUtils import Logger
from Ansys.Common.WB1ManagedUtils.Logger import LoggerSeverity


def log_debug_message(message):
    Logger.LogMessage(LoggerSeverity.Debug, Logger.DesignSpaceContext, message)


def log_info_message(message):
    Logger.LogMessage(LoggerSeverity.Info, Logger.DesignSpaceContext, message)


def log_warning_message(message):
    Logger.LogMessage(LoggerSeverity.Warning, Logger.DesignSpaceContext, message)


def log_error_message(message):
    Logger.LogMessage(LoggerSeverity.Error, Logger.DesignSpaceContext, message)


def log_fatal_message(message):
    Logger.LogMessage(LoggerSeverity.Fatal, Logger.DesignSpaceContext, message)


def log_test():
    return "log_test"


log_debug_message("my debug message")
log_info_message("my info message")
log_warning_message("my warning message")
log_error_message("my error message")
log_fatal_message("my fatal message")
time.sleep(2)

log_test()
