import clr
from pathlib import Path


def _get_embedding():
    try:
        clr.AddReference("Ansys.Mechanical.Embedding")
        import Ansys

        return Ansys.Mechanical.Embedding
    except:
        raise Exception("Cannot use logging until after mechanical embedding is intialized")


class Logging:
    class Level:
        TRACE = 0
        DEBUG = 1
        INFO = 2
        WARNING = 3
        ERROR = 4
        FATAL = 5

    @classmethod
    def config(cls, **kwargs):
        """Similar to logging.basicConfig.  Available options:
        filename -> str
        level -> Logging.Level values
        auto_flush -> bool
        enabled -> bool
        stdout -> bool
        """
        config = _get_embedding().LoggingConfiguration
        if "filename" in kwargs:
            path = Path(kwargs["filename"])
            config.Filename = path.name
            config.Path = str(path.parent)
        if "enabled" in kwargs:
            config.Enabled = kwargs["enabled"]
        if "auto_flush" in kwargs:
            config.AutoFlush = kwargs["auto_flush"]
        if "stdout" in kwargs:
            config.LogToStdOut = kwargs["stdout"]
        if "level" in kwargs:
            config.FilterLevel = kwargs["level"]

    @classmethod
    def log_message(cls, severity: Level, context: str, message: str) -> None:
        """log the message to the configured logging mechanism"""
        _get_embedding().Logging.LogMessage(severity, context, message)

    @classmethod
    def can_log_message(cls, severity: Level) -> bool:
        """returns whether a message with the given severity will be output into the log"""
        return _get_embedding().Logging.CanLogMessage(severity)

    @classmethod
    def flush(cls) -> None:
        """flushes the log manually"""
        return _get_embedding().Logging.Flush()
