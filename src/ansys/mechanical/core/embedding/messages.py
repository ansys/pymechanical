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

        self.MessageSeverityType = MessageSeverityType
        self.Message = Message

        # Initialize a local cache for messages
        self._messages_df = pd.DataFrame()
        self._update_messages_cache()

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
        if self._messages_df.empty:
            raise IndexError("No messages are available.")
        if index >= len(self._messages_df) or index < 0:
            raise IndexError("Message index out of range.")
        row = self._messages_df.iloc[index]
        return _Message(row)

    def __len__(self):
        """Return the number of messages."""
        return len(self._messages_df)

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
            "info": self.MessageSeverityType.Info,
            "warning": self.MessageSeverityType.Warning,
            "error": self.MessageSeverityType.Error,
        }

        if severity.lower() not in severity_map:
            raise ValueError(f"Invalid severity: {severity}")

        _msg = self.Message(text, severity_map[severity.lower()])
        self._app.ExtAPI.Application.Messages.Add(_msg)

        self._update_messages_cache()

    def show(self, filter="severity;message"):
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
        self._update_messages_cache()

        if self._messages_df.empty:
            print("No messages to display.")
            return

        for _, row in self._messages_df.iterrows():
            msg = _Message(row)
            msg.show(filter)

    def clear(self):
        """Clear all messages."""
        self._app.ExtAPI.Application.Messages.Clear()
        self._update_messages_cache()


class _Message:
    """Lightweight message object for individual message handling."""

    def __init__(self, row):
        """Initialize with a row from the DataFrame."""
        self.row = row

    @property
    def message(self):
        """Return the message text."""
        return self.row["DisplayString"]

    @property
    def severity(self):
        """Return the message severity."""
        return self.row["Severity"].lower()

    @property
    def time_stamp(self):
        """Return the message timestamp."""
        return str(self.row["TimeStamp"])

    @property
    def source(self):
        """Return the message source."""
        return self.row["Source"]

    @property
    def string_id(self):
        """Return the message string ID."""
        return self.row["StringID"]

    @property
    def location(self):
        """Return the message location."""
        return self.row["Location"]

    @property
    def related_objects(self):
        """Return the message related objects."""
        return self.row["RelatedObjects"]

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
        return f"[{self.row['Severity']}] {self.row['DisplayString']}"

    def __repr__(self):
        """Provide a string representation of the message."""
        return repr(self.row)
