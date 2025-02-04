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

import pandas as pd


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
        self._messages_df = pd.DataFrame()

    def _update_messages_cache(self):
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

        self._messages_df = pd.DataFrame(data)

    def __repr__(self):
        """Provide a DataFrame representation of all messages."""
        self._update_messages_cache()
        return repr(self._messages_df)

    def __str__(self):
        """Provide a custom string representation of the messages."""
        if self._messages_df.empty:
            return "No messages to display."

        formatted_messages = [
            f"[{row['Severity']}] : {row['DisplayString']}"
            for _, row in self._messages_df.iterrows()
        ]
        return "\n".join(formatted_messages)

    def __getitem__(self, index):
        """Allow indexed access to messages."""
        if len(self._messages) == 0:
            raise IndexError("No messages are available.")
        if index >= len(self._messages) or index < 0:
            raise IndexError("Message index out of range.")
        row = self._messages[index]
        return Message(row)

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

        self._update_messages_cache()

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

    # TODO: add functionality to filter only errors, warnings, info

    def show(self, filter="severity;message"):
        # TODO : add max number of messages to display
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
        ... message: User clicked the start button.

        >>> app.messages.show(filter="time_stamp;severity;message")
        ... time_stamp: 1/30/2025 12:10:35 PM
        ... severity: info
        ... message: User clicked the start button.
        """
        if self._app.ExtAPI.Application.Messages.Count == 0:
            print("No messages to display.")
            return

        for message in self._messages:
            msg = Message(message)
            msg.show(filter)

    def clear(self):
        """Clear all messages."""
        self._messages.Clear()


class Message:
    """Lightweight message object for individual message handling."""

    def __init__(self, message: "Ansys.Mechanical.Application.Message"):
        """Initialize with a row from the DataFrame."""
        self._msg = message

    @property
    def message(self):
        """Return the message text."""
        return self._msg.DisplayString

    @property
    def severity(self):
        """Return the message severity."""
        return self._msg.Severity

    @property
    def time_stamp(self):
        """Return the message timestamp."""
        return str(self._msg.TimeStamp)

    @property
    def source(self):
        """Return the message source."""
        return self._msg.Source

    @property
    def string_id(self):
        """Return the message string ID."""
        return self._msg.StringID

    @property
    def location(self):
        """Return the message location."""
        return self._msg.Location

    @property
    def related_objects(self):
        """Return the message related objects."""
        return self._msg.RelatedObjects

    def show(self, filter="severity;message"):
        """Show the message details.

        Parameters
        ----------
        filter : str, optional
            Semicolon separated list of message attributes to display.
            Default is "severity;message".
            if filter is "*", all available attributes will be displayed.
            other options are "time_stamp", "source", "location", "related_objects".

        Examples
        --------
        >>> app.messages[0].show()
        ... severity: info
        ... message: User clicked the start button.

        >>> app.messages[0].show(filter="*")
        ... severity: info
        ... message: User clicked the start button.
        ... time_stamp: 1/30/2025 12:10:35 PM
        ... source: None
        ... string_id: None
        ... location: Ansys.ACT.Core.Utilities.SelectionInfo
        ... related_objects: None
        """
        if filter == "*":
            selected_columns = [
                "time_stamp",
                "severity",
                "message",
                "source",
                "string_id",
                "location",
                "related_objects",
            ]
        else:
            selected_columns = [col.strip() for col in filter.split(";")]

        for key in selected_columns:
            print(f"{key}: {getattr(self, key, "Specified filter not found.")}")

    def __str__(self):
        """Provide a string representation of the message."""
        return f"[{self._msg.Severity}] {self._msg.DisplayString}"

    def __repr__(self):
        """Provide a string representation of the message."""
        return f"[{self._msg.Severity}] {self._msg.DisplayString}"
