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


class MessageManager:
    def __init__(self, app):
        self.app = app  # Reference to the app instance
        from Ansys.Mechanical.Application import Message
        from Ansys.Mechanical.DataModel.Enums import MessageSeverityType

        self.MessageSeverityType = MessageSeverityType
        self.Message = Message

    def add(self, severity: str, text: str):
        """Add a message."""
        _msg = self.Message(text, self.MessageSeverityType.Error)
        self.app.ExtAPI.Application.Messages.Add(_msg)

    def fetch_app_messages(self):
        """Fetch messages from the app's ExtAPI.Message."""
        # Assuming ExtAPI.Message provides a list of messages in the format (severity, text)
        return [(msg.Severity, msg.DisplayString) for msg in self.app.ExtAPI.Application.Messages]

    def print(self):
        """Print all messages, combining local and app messages."""
        # Fetch messages from ExtAPI.Message
        app_messages = self.fetch_app_messages()
        formatted_app_messages = [f"[{severity}] {text}" for severity, text in app_messages]

        # Combine and display messages
        if formatted_app_messages:
            print("\n".join(formatted_app_messages))
        else:
            print("No messages to display.")

    def __str__(self):
        """Provide a raw print of all messages when accessed as a string."""
        # Fetch messages from ExtAPI.Message
        app_messages = self.fetch_app_messages()
        formatted_app_messages = [f"[{severity}] {text}" for severity, text in app_messages]

        # Combine local and app messages
        all_messages = formatted_app_messages
        return "\n".join(all_messages) if all_messages else "No messages to display."
