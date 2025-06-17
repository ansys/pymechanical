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

"""Temporary Appdata for Ansys Mechanical."""

from pathlib import Path
import shutil
import sys
import warnings


class UniqueUserProfile:
    """Create Unique User Profile (for AppData)."""

    def __init__(self, profile_name: str, copy_profile: bool = True, dry_run: bool = False):
        """Initialize UniqueUserProfile class."""
        self._default_profile = Path("~").expanduser()
        self._location = self._default_profile / "PyMechanical-AppData" / profile_name
        self._dry_run = dry_run
        self.copy_profile = copy_profile
        self.initialize()

    def initialize(self) -> None:
        """
        Initialize the new profile location.

        Args:
            copy_profile (bool): If False, the copy_profile method will be skipped.
        """
        if self._dry_run:
            return
        if self.exists():
            self.cleanup()
        self.mkdirs()
        if self.copy_profile:
            self.copy_profiles()

    def cleanup(self) -> None:
        """Cleanup unique user profile."""
        if self._dry_run:
            return

        # Remove the appdata directory if it exists
        shutil.rmtree(self.location, ignore_errors=True)

        if self.location.is_dir():
            warnings.warn(
                f"The `private appdata` option was used, but {self.location} was not removed"
            )

    @property
    def location(self) -> str:
        """Return the profile name."""
        return self._location

    def update_environment(self, env) -> None:
        """Set environment variables for new user profile."""
        home = self.location
        if "win" in sys.platform:
            appdata_dir = home / "AppData"
            appdata_local_temp = str(appdata_dir / "Local" / "Temp")

            env["USERPROFILE"] = str(home)
            env["APPDATA"] = str(appdata_dir / "Roaming")
            env["LOCALAPPDATA"] = str(appdata_dir / "Local")
            env["TMP"] = appdata_local_temp
            env["TEMP"] = appdata_local_temp
        elif "lin" in sys.platform:
            env["HOME"] = str(home)

    def exists(self) -> bool:
        """Check if unique profile name already exists."""
        return self.location.exists()

    def mkdirs(self) -> None:
        """Create a unique user profile & set up the directory tree."""
        self.location.mkdir(parents=True, exist_ok=True)
        if "win" in sys.platform:
            locs = ["AppData/Roaming", "AppData/Local", "Documents"]
        elif "lin" in sys.platform:
            locs = [".config", "temp/reports"]

        for loc in locs:
            dir_name = self.location / loc
            dir_name.mkdir(parents=True, exist_ok=True)

    def copy_profiles(self) -> None:
        """Copy current user directories into a new user profile."""
        if "win" in sys.platform:
            locs = ["AppData/Roaming/Ansys", "AppData/Local/Ansys"]
        elif "lin" in sys.platform:
            locs = [".mw/Application Data/Ansys", ".config/Ansys"]
        for loc in locs:
            default_profile_loc = self._default_profile / loc
            temp_appdata_loc = self.location / loc
            if default_profile_loc.exists():
                shutil.copytree(default_profile_loc, temp_appdata_loc)
