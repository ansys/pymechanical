"""Temporary Appdata for Ansys Mechanical."""

import os
import shutil
import sys
import warnings


class UniqueUserProfile:
    """Create Unique User Profile (for AppData)."""

    def __init__(self, profile_name):
        """Initialize UniqueUserProfile class."""
        self._default_profile = os.path.expanduser("~")
        self._location = os.path.join(self._default_profile, profile_name)
        self.initialize()

    def initialize(self) -> None:
        """Initialize the new profile location."""
        if self.exists():
            self.cleanup()
        self.mkdirs()
        self.copy_profiles()
        self.warn()

    def cleanup(self) -> None:
        """Cleanup unique user profile."""
        shutil.rmtree(self.location, ignore_errors=True)

    @property
    def location(self) -> str:
        """Return the profile name."""
        return self._location

    def update_environment(self, env) -> None:
        """Set environment variables for new user profile."""
        home = self.location
        if "win" in sys.platform:
            env["USERPROFILE"] = home
            env["APPDATA"] = os.path.join(home, "AppData/Roaming")
            env["LOCALAPPDATA"] = os.path.join(home, "AppData/Local")
            env["TMP"] = os.path.join(home, "AppData/Local/Temp")
            env["TEMP"] = os.path.join(home, "AppData/Local/Temp")
        elif "lin" in sys.platform:
            env["HOME"] = home

    def exists(self) -> bool:
        """Check if unique profile name already exists."""
        return os.path.exists(self.location)

    def mkdirs(self) -> None:
        """Create unique user profile & set up directory tree."""
        os.makedirs(self.location)
        if "win" in sys.platform:
            locs = ["AppData/Roaming", "AppData/Local", "AppData/Local/Temp", "Documents"]
        elif "lin" in sys.platform:
            locs = [".config", "temp/reports"]

        for loc in locs:
            os.makedirs(os.path.join(self.location, loc))

    def copy_profiles(self) -> None:
        """Copy directories from current user into new user profile."""
        if "win" in sys.platform:
            locs = ["AppData/Roaming/Ansys", "AppData/Local/Ansys"]
        elif "lin" in sys.platform:
            locs = [".mw/Application Data/Ansys", ".config/Ansys"]
        for loc in locs:
            shutil.copytree(
                os.path.join(self._default_profile, loc), os.path.join(self.location, loc)
            )

    def warn(self) -> None:
        """Issue warning."""
        warnings.warn(
            "Using the private_appdata option creates temporary directories when "
            "running mechanical in parallel. "
            f"There may be leftover files in {self.location}."
        )
