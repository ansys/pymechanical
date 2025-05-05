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

"""Message Manager for App."""

# TODO: add functionality to filter only errors, warnings, info
# TODO: add max number of messages to display
# TODO: implement pep8 formatting

try:  # noqa: F401
    import pandas as pd

    HAS_PANDAS = True
    """Whether or not pandas exists."""
except ImportError:
    HAS_PANDAS = False


class MessageManager:
    """Message manager for adding, fetching, and printing messages."""

    def __init__(self, app):
        """Initialize the message manager."""
        self._app = app

        # Import necessary classes
        from Ansys.Mechanical.Application import Message
        from Ansys.Mechanical.DataModel.Enums import MessageSeverityType

        self._message_severity = MessageSeverityType
        self._message = Message
        self._messages = self._app.ExtAPI.Application.Messages

    def _create_messages_data(self):  # pragma: no cover
        """Update the local cache of messages."""
        data = {
            "Severity": [],
            "TimeStamp": [],
            "DisplayString": [],
            "Source": [],
            "StringID": [],
            "Location": [],
            "RelatedObjects": [],
        }
        for msg in self._app.ExtAPI.Application.Messages:
            data["Severity"].append(str(msg.Severity).upper())
            data["TimeStamp"].append(msg.TimeStamp)
            data["DisplayString"].append(msg.DisplayString)
            data["Source"].append(msg.Source)
            data["StringID"].append(msg.StringID)
            data["Location"].append(msg.Location)
            data["RelatedObjects"].append(msg.RelatedObjects)

        return data

    def __repr__(self):  # pragma: no cover
        """Provide a DataFrame representation of all messages."""
        if not HAS_PANDAS:
            return "Pandas is not available. Please pip install pandas to display messages."
        data = self._create_messages_data()
        return repr(pd.DataFrame(data))

    def __str__(self):
        """Provide a custom string representation of the messages."""
        if self._messages.Count == 0:
            return "No messages to display."

        formatted_messages = [f"[{msg.Severity}] : {msg.DisplayString}" for msg in self._messages]
        return "\n".join(formatted_messages)

    def __getitem__(self, index):
        """Allow indexed access to messages."""
        if len(self._messages) == 0:
            raise IndexError("No messages are available.")
        if index >= len(self._messages) or index < 0:
            raise IndexError("Message index out of range.")
        return self._messages[index]

    def __len__(self):
        """Return the number of messages."""
        return self._messages.Count

    def add(self, severity: str, text: str):
        """Add a message and update the cache.

        Parameters
        ----------
        severity : str
            Severity of the message. Can be "info", "warning", or "error".
        text : str
            Message text.

        Examples
        --------
        >>> app.messages.add("info", "User clicked the start button.")
        """
        severity_map = {
            "info": self._message_severity.Info,
            "warning": self._message_severity.Warning,
            "error": self._message_severity.Error,
        }

        if severity.lower() not in severity_map:
            raise ValueError(f"Invalid severity: {severity}")

        _msg = self._message(text, severity_map[severity.lower()])
        self._messages.Add(_msg)

    def remove(self, index: int):
        """Remove a message by index.

        Parameters
        ----------
        index : int
            Index of the message to remove.

        Examples
        --------
        >>> app.messages.remove(0)
        """
        if index >= len(self._app.ExtAPI.Application.Messages) or index < 0:
            raise IndexError("Message index out of range.")
        _msg = self._messages[index]
        self._messages.Remove(_msg)

    def _show_string(self, filter: str = "Severity;DisplayString") -> str:
        if self._messages.Count == 0:
            return "No messages to display."

        if filter == "*":
            selected_columns = [
                "TimeStamp",
                "Severity",
                "DisplayString",
                "Source",
                "StringID",
                "Location",
                "RelatedObjects",
            ]
        else:
            selected_columns = [col.strip() for col in filter.split(";")]

        lines = []
        for msg in self._messages:
            for key in selected_columns:
                line = f"{key}: {getattr(msg, key, 'Specified attribute not found.')}"
                lines.append(line)
        return "\n".join(lines)

    def show(self, filter="Severity;DisplayString") -> None:
        """Print all messages with full details.

        Parameters
        ----------
        filter : str, optional
            Semicolon separated list of message attributes to display.
            Default is "severity;message".
            if filter is "*", all available attributes will be displayed.

        Examples
        --------
        >>> app.messages.show()
        ... severity: info
        ... message: Sample message.

        >>> app.messages.show(filter="time_stamp;severity;message")
        ... time_stamp: 1/30/2025 12:10:35 PM
        ... severity: info
        ... message: Sample message.
        """
        show_string = self._show_string(filter)
        print(show_string)

    def clear(self):
        """Clear all messages."""
        self._messages.Clear()
