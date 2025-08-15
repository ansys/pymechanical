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
from typing import List, Optional, Union

from ansys.mechanical.core import LOG


class LicenseManager:
    """Class to manage licenses in Ansys Mechanical.

    This class provides methods to enable, disable, and check the status of licenses.
    It also allows for moving licenses to specific indices in the license preference list.
    It is initialized with an instance of the Ansys Mechanical application.
    """

    def __init__(self, app):
        """Initialize the message manager."""
        self._app = app
        self._license_preference = self._app.ExtAPI.Application.LicensePreference
        import Ansys

        self._license_status = Ansys.Mechanical.DataModel.Enums.LicenseStatus

    def get_all_licenses(self) -> list[str]:
        """Return list of all licenses."""
        return self._license_preference.GetAllLicenses()

    def get_license_status(
        self, license_name: str
    ) -> "Ansys.Mechanical.DataModel.Enums.LicenseStatus":
        """Return status of the specific license.

        Parameters
        ----------
        license_name : str
            Name of the license to check.

        Returns
        -------
        "Ansys.Mechanical.DataModel.Enums.LicenseStatus"
            The status of the license.
        """
        LOG.info(
            f"{license_name} status: {self._license_preference.GetLicenseStatus(license_name)}"
        )
        return self._license_preference.GetLicenseStatus(license_name)

    def set_license_status(self, license_name: str, status: bool) -> None:
        """Set the status of a license and save the preference.

        Parameters
        ----------
        license_name : str
            Name of the license to set the status for.
        status : bool
            True to enable the license, False to disable it.
        """
        if status:
            self._license_preference.SetLicenseStatus(license_name, self._license_status.Enabled)
            LOG.info(f"{license_name} is enabled.")
        else:
            self._license_preference.SetLicenseStatus(license_name, self._license_status.Disabled)
            LOG.info(f"{license_name} is disabled.")
        self._license_preference.Save()

    def show(self) -> None:
        """Print all active licenses."""
        for lic in self.get_all_licenses():
            print(f"{lic} - {self._license_preference.GetLicenseStatus(lic)}")

    def disable_session_license(self) -> None:
        """Disable all licenses for current session."""
        self._license_preference.DeActivateLicense()

    def enable_session_license(self, license: Optional[Union[str, List[str]]] = None) -> None:
        """Enable license(s) for the current session.

        Parameters
        ----------
        license : Optional[Union[str, List[str]]], optional
            If None, activates the first enabled license in the priority order.
            If a string, activates that specific license.
            If a list of strings, activates all specified licenses in the order provided.
        """
        from System import String
        from System.Collections.Generic import List

        if license is None:
            self._license_preference.ActivateLicense()
        elif isinstance(license, str):
            self._license_preference.ActivateLicense(String(license))
        elif isinstance(license, list):
            licenses = List[String]()
            for lic in license:
                licenses.Add(String(lic))
            self._license_preference.ActivateLicense(licenses)
        else:
            raise TypeError("License must be None, a string, or a list of strings.")
        LOG.info(f"License(s) {license} enabled for the current session.")

    def move_to_index(self, license_name: str, location: int) -> None:
        """Move a license preference.

        Move license to zero-based index location in the license preference list.
        This is useful for setting the preferred license location.

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
        >>> license_manager.move_to_index('Ansys Mechanical Premium', 0)
        """
        LOG.info(f"Moving license preference for {license_name} to location {location}")
        self._license_preference.MoveLicenseToLocation(license_name, location)
        self._license_preference.Save()

    def reset_preference(self) -> None:
        """Reset the license preference."""
        self._license_preference.Reset()
