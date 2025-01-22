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


class MessageManager:
    """Message manager for adding, fetching, and printing messages."""

    def __init__(self, app):
        """Initialize the message manager."""
        self._app = app

        # Imports necessary classes
        from Ansys.Mechanical.Application import Message
        from Ansys.Mechanical.DataModel.Enums import MessageSeverityType

        self.MessageSeverityType = MessageSeverityType
        self.Message = Message

    def add(self, severity: str, text: str):
        """Add a message.

        Parameters
        ----------
        severity : str
            Severity of the message. Can be "info", "warning", or "error".
        text : str
            Message text.

        Examples
        --------
        >>> app.message.add("info", "User clicked the start button.")

        Raises
        ------
        ValueError
            If the severity is not "info", "warning", or "error".
        """
        # Map severity to MessageSeverityType
        if severity.lower() == "info":
            _msg = self.Message(text, self.MessageSeverityType.Info)
        elif severity.lower() == "warning":
            _msg = self.Message(text, self.MessageSeverityType.Warning)
        elif severity.lower() == "error":
            _msg = self.Message(text, self.MessageSeverityType.Error)
        else:
            raise ValueError(f"Invalid severity: {severity}")

        _msg = self.Message(text, self.MessageSeverityType.Error)
        self._app.ExtAPI.Application.Messages.Add(_msg)

    def _fetch_app_messages(self, complete_info=False):
        """Fetch messages from the app's ExtAPI.Message."""
        if complete_info:
            return [
                (
                    msg.Severity,
                    msg.TimeStamp,
                    msg.DisplayString,
                    msg.Source,
                    msg.StringID,
                    msg.Location,
                    msg.RelatedObjects,
                )
                for msg in self._app.ExtAPI.Application.Messages
            ]
        return [(msg.Severity, msg.DisplayString) for msg in self._app.ExtAPI.Application.Messages]

    def _get_messages(self, complete_info=False):
        _app_messages = self._fetch_app_messages(complete_info)
        if complete_info:
            formatted_app_messages = []
            for severity, time, text, source, string_id, location, related_objects in _app_messages:
                formatted_app_messages.append(
                    f"[{str(severity).upper()}] {time} : {text} - "
                    f"<source>{source} - <string id>{string_id} - "
                    f"<location>{location} - <related objects>{related_objects}"
                )
        else:
            formatted_app_messages = [
                f"[{str(severity).upper()}] : {text}" for severity, text in _app_messages
            ]

        # Combine local and app messages
        all_messages = formatted_app_messages
        return "\n".join(all_messages) if all_messages else "No messages to display."

    def print(self, complete_info=False):
        """Print all messages, combining local and app messages."""
        print(self._get_messages(complete_info))

    def __str__(self):
        """Provide a raw print of all messages when accessed as a string."""
        return self._get_messages()
