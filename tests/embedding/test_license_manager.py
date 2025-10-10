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

"""License manager test."""

import pytest


@pytest.mark.embedding
def test_license_manager(embedded_app, capsys):
    """Test message manager."""
    test_license = "Ansys Mechanical Premium"
    assert len(embedded_app.license_manager.get_all_licenses()) > 0
    assert embedded_app.readonly is False, "App should be editable after enabling session license"
    all_licenses = embedded_app.license_manager.get_all_licenses()
    assert test_license in all_licenses, "Expected license not found in the list"

    # Enable and disable specific license
    status = embedded_app.license_manager.get_license_status(test_license)
    assert (
        status == embedded_app.license_manager._license_status.Enabled
    ), "License should be enabled"

    embedded_app.license_manager.set_license_status(test_license, False)
    status = embedded_app.license_manager.get_license_status(test_license)
    assert (
        status == embedded_app.license_manager._license_status.Disabled
    ), "License should be disabled"

    embedded_app.license_manager.set_license_status(test_license, True)
    status = embedded_app.license_manager.get_license_status(test_license)
    assert (
        status == embedded_app.license_manager._license_status.Enabled
    ), "License should be enabled"

    license_list = embedded_app.license_manager.get_all_licenses()
    assert license_list.index(test_license) == 1, "License should be at index 1"
    embedded_app.license_manager.move_to_index(test_license, 0)
    license_list = embedded_app.license_manager.get_all_licenses()
    assert license_list.index(test_license) == 0, "License should be at index 0"

    embedded_app.license_manager.reset_preference()
    license_list = embedded_app.license_manager.get_all_licenses()
    assert license_list.index(test_license) == 1, "License should be at index 1 after reset"

    # Enable session license with all cases
    embedded_app.license_manager.disable_session_license()
    assert embedded_app.readonly is True, "App should be readonly after disabling session license"
    embedded_app.license_manager.enable_session_license()
    embedded_app.license_manager.disable_session_license()
    embedded_app.license_manager.enable_session_license(test_license)
    assert embedded_app.readonly is False
    embedded_app.license_manager.disable_session_license()
    embedded_app.license_manager.enable_session_license(
        ["Ansys Mechanical Enterprise", test_license]
    )
    assert embedded_app.readonly is False

    with pytest.raises(TypeError):
        embedded_app.license_manager.enable_session_license(1)

    embedded_app.license_manager.show()
    captured = capsys.readouterr()
    printed_output = captured.out.strip()
    assert "Enabled" in printed_output
    assert test_license in printed_output
