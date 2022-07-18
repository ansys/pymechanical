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
