# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""License manager test."""

import pytest

TEST_LICENSE = "Ansys Mechanical Premium"


@pytest.mark.embedding
def test_get_all_licenses(embedded_app):
    """Test that the license list is non-empty and contains the expected license."""
    licenses = embedded_app.license_manager.get_all_licenses()
    assert len(licenses) > 0
    assert TEST_LICENSE in licenses


@pytest.mark.embedding
def test_set_license_status(embedded_app):
    """Test enabling and disabling a specific license."""
    lm = embedded_app.license_manager
    lm.set_license_status(TEST_LICENSE, False)
    assert lm.get_license_status(TEST_LICENSE) == lm._license_status.Disabled
    lm.set_license_status(TEST_LICENSE, True)
    assert lm.get_license_status(TEST_LICENSE) == lm._license_status.Enabled


@pytest.mark.embedding
def test_move_to_index(embedded_app):
    """Test moving a license to index 0 and resetting the preference."""
    lm = embedded_app.license_manager
    original_index = lm.get_all_licenses().index(TEST_LICENSE)
    assert original_index > 0

    lm.move_to_index(TEST_LICENSE, 0)
    assert lm.get_all_licenses().index(TEST_LICENSE) == 0

    lm.reset_preference()
    assert lm.get_all_licenses().index(TEST_LICENSE) != 0


@pytest.mark.embedding
def test_session_license(embedded_app):
    """Test enabling and disabling the session license."""
    lm = embedded_app.license_manager

    lm.disable_session_license()
    assert embedded_app.readonly is True

    lm.enable_session_license()
    lm.disable_session_license()

    lm.enable_session_license(TEST_LICENSE)
    assert embedded_app.readonly is False
    lm.disable_session_license()

    lm.enable_session_license(["Ansys Mechanical Enterprise", TEST_LICENSE])
    assert embedded_app.readonly is False


@pytest.mark.embedding
def test_session_license_invalid_type(embedded_app):
    """Test that enable_session_license raises TypeError for invalid input."""
    with pytest.raises(TypeError):
        embedded_app.license_manager.enable_session_license(1)


@pytest.mark.embedding
def test_show(embedded_app, capsys):
    """Test that show() prints license status to stdout."""
    embedded_app.license_manager.show()
    output = capsys.readouterr().out.strip()
    assert "Enabled" in output
    assert TEST_LICENSE in output
