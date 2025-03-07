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

"""License Manager."""
from ansys.mechanical.core import LOG

# TODO: enable logging


class LicenseManager:
    """Message manager for adding, fetching, and printing messages."""

    def __init__(self, app):
        """Initialize the message manager."""
        self._app = app
        if self._app.version < 252:
            raise ValueError("License manager is only available in Ansys 2022 R1 or later.")

        self._license_preference = self._app.ExtAPI.Application.LicensePreference

    def _get_all_licenses(self):
        """Return all active licenses."""
        return self._license_preference.GetAllLicenses()

    def get_license_status(self, license_name: str):
        """Return the status of a license."""
        return self._license_preference.GetLicenseStatus(license_name)

    def set_license_status(self, license_name: str, status: bool):
        """Set the status of a license."""
        _status = Ansys.Mechanical.DataModel.Enums.LicenseStatus
        if status:
            self._license_preference.SetLicenseStatus(license_name, _status.Enabled)
            LOG.info(f"{license_name} is enabled.")
        else:
            self._license_preference.SetLicenseStatus(license_name, _status.Disabled)
            LOG.info(f"{license_name} is disabled.")

    def show(self):
        """Print all active licenses."""
        for lic in self._get_all_licenses():
            print(f"{lic} - {self.get_license_status(lic)}")

    def activate(self):
        """Activate a license."""
        self._license_preference.ActivateLicense()

    def deactivate(self):
        """Deactivate a license."""
        self._license_preference.DeActivateLicense()

    def switch_preference(self, license_name, location):
        """Switch a license preference.

        Move license to in priority order.

        Parameters
        ----------
        license_name : str
            License name.
        location : int
            Location to move the license to.

        Examples
        --------
        Move Ansys Mechanical Premium to the first location.

        >>> license_manager = LicenseManager(app)
        >>> license_manager.switch_preference('Ansys Mechanical Premium', 0)
        """
        LOG.info(f"Switching license preference for {license_name} to location {location}")
        self._license_preference.MoveLicenseToLocation(license_name, location)
        self._license_preference.Save()

    def reset(self):
        """Reset the license preference."""
        self._license_preference.Reset()
