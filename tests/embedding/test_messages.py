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

"""Message manager test"""

from pathlib import Path
import re

import pytest


@pytest.mark.embedding
def test_message_manager(embedded_app):
    """Test message manager"""
    # if license checkout takes time then there is a warning message
    # get added to app. So, clear the messages before starting the test
    embedded_app.messages.clear()
    assert len(embedded_app.messages) == 0

    messages_str = str(embedded_app.messages)
    assert "No messages to display." in messages_str

    embedded_app.messages.add("info", "Info message")

    messages_str = str(embedded_app.messages)
    assert "Info message" in messages_str


@pytest.mark.embedding
def test_message_add_and_clear(embedded_app):
    """Test adding and clearing messages"""
    embedded_app.messages.clear()
    assert len(embedded_app.messages) == 0

    embedded_app.messages.add("info", "Info message")
    assert len(embedded_app.messages) == 1
    embedded_app.messages.add("warning", "Warning message")
    assert len(embedded_app.messages) == 2
    embedded_app.messages.add("error", "Error message")
    assert len(embedded_app.messages) == 3

    embedded_app.messages.remove(0)
    assert len(embedded_app.messages) == 2

    with pytest.raises(IndexError):
        embedded_app.messages.remove(10)

    with pytest.raises(ValueError):
        embedded_app.messages.add("trace", "Trace message")


@pytest.mark.embedding
def test_message_show(embedded_app):
    """Test showing messages"""
    embedded_app.messages.clear()
    messages_str = str(embedded_app.messages._show_string())
    assert "No messages to display." in messages_str

    embedded_app.messages.add("info", "Info message")
    messages_str = str(embedded_app.messages._show_string())
    assert "Severity" in messages_str
    assert "DisplayString" in messages_str
    assert "Info message" in messages_str
    messages_str = str(embedded_app.messages._show_string(filter="TimeStamp"))
    assert "TimeStamp" in messages_str

    messages_str = str(embedded_app.messages._show_string(filter="unknown"))
    assert "Specified attribute not found" in messages_str


@pytest.mark.embedding
def test_message_get(embedded_app, assets):
    """Test getting a message"""
    from ansys.mechanical.core.embedding.enum_importer import (
        DataModelObjectCategory,
        MessageSeverityType,
    )

    with pytest.raises(IndexError):
        embedded_app.messages[10]

    embedded_app.open(str(Path(assets) / "cube-hole.mechdb"))
    _messages = embedded_app.messages
    _msg1 = None
    for _msg in _messages:
        if "Image file not found" in _msg.DisplayString:
            _msg1 = _msg
            break
    assert _msg1 is not None, "Expected message not found in messages"
    assert _msg1.Severity == MessageSeverityType.Warning

    message_str = str(_msg1)
    type_str = "Ansys.Mechanical.Application.Message"
    if embedded_app.version < 252:
        # The __repr__ string of previous versions was the type name
        assert type_str in message_str
    else:
        assert type_str not in message_str

    assert "Image file not found" in _msg1.DisplayString
    assert re.search(r"\d", str(_msg1.TimeStamp))
    assert _msg1.Source.DataModelObjectCategory == DataModelObjectCategory.Image
    assert len(_msg1.RelatedObjects) == 0
    assert len(_msg1.Location.Ids) == 0

    with pytest.raises(IndexError):
        embedded_app.messages[10]
