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

import os

import pytest


@pytest.mark.embedding
def test_message_manager(embedded_app, capsys):
    """Test message manager"""
    assert embedded_app.messages.count() == 0
    assert embedded_app.messages._messages_df.empty == True

    print(embedded_app.messages)
    captured = capsys.readouterr()
    printed_output = captured.out.strip()
    assert "No messages to display." in printed_output

    assert "Empty" in repr(embedded_app.messages)

    embedded_app.messages.add("info", "Info message")

    assert "INFO" in repr(embedded_app.messages[0])

    print(embedded_app.messages)
    captured = capsys.readouterr()
    printed_output = captured.out.strip()
    assert "Info message" in printed_output


@pytest.mark.embedding
def test_message_add_and_clear(embedded_app):
    """Test adding and clearing messages"""
    embedded_app.messages.add("info", "Info message")
    assert embedded_app.messages.count() == 1
    embedded_app.messages.add("warning", "Warning message")
    assert embedded_app.messages.count() == 2
    embedded_app.messages.add("error", "Error message")
    assert embedded_app.messages.count() == 3
    embedded_app.messages.clear()
    assert embedded_app.messages.count() == 0

    with pytest.raises(ValueError):
        embedded_app.messages.add("trace", "Trace message")


@pytest.mark.embedding
def test_message_show(embedded_app, capsys):
    """Test showing messages"""
    print(embedded_app.messages.show())
    captured = capsys.readouterr()
    printed_output = captured.out.strip()
    assert "No messages to display." in printed_output

    embedded_app.messages.add("info", "Info message")
    embedded_app.messages.show()
    captured = capsys.readouterr()
    printed_output = captured.out.strip()
    assert "Severity" in printed_output
    assert "Message" in printed_output
    assert "Info message" in printed_output
    embedded_app.messages.show(complete_info=True)
    captured = capsys.readouterr()
    printed_output = captured.out.strip()
    assert "TimeStamp" in printed_output


@pytest.mark.embedding
def test_message_get(embedded_app, assets, capsys):
    """Test getting a message"""
    embedded_app.open(os.path.join(assets, "cube-hole.mechdb"))
    _msg1 = embedded_app.messages[0]

    print(_msg1)
    captured = capsys.readouterr()
    printed_output = captured.out.strip()
    assert "WARNING" in printed_output

    assert _msg1.severity == "warning"
    assert "Image file not found" in _msg1.message
    assert "AM" in _msg1.time_stamp or "PM" in _msg1.time_stamp
    print(_msg1.string_id, _msg1.source, _msg1.location, _msg1.related_objects)
    captured = capsys.readouterr()
    printed_output = captured.out.strip()
    assert "Ansys.ACT.Automation.Mechanical.Image" in printed_output
    assert "Ansys.Mechanical.DataModel.Interfaces.IDataModelObject" in printed_output
    assert "Ansys.ACT.Core.Utilities.SelectionInf" in printed_output

    embedded_app.messages[1].show()
    captured = capsys.readouterr()
    printed_output = captured.out.strip()
    assert "The currently selected unit" in printed_output
    assert "Source" not in printed_output

    embedded_app.messages[1].show(complete_info=True)
    captured = capsys.readouterr()
    printed_output = captured.out.strip()
    assert "Source" in printed_output

    with pytest.raises(IndexError):
        embedded_app.messages[10]
