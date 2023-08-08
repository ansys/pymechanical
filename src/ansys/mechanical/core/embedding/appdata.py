"""Temporary Appdata for Ansys Mechanical"""

import os
import shutil
import sys
import warnings


class TmpUser:
    """Create Unique User Profile (for AppData)."""

    def __init__(self, defaultProfile, profileName):
        """Initialize TmpUser class."""
        self.defaultProfile = defaultProfile
        self.profileName = profileName

    @property
    def profile_name(self) -> str:
        """Return the profile name"""
        return self.profileName

    def set_env(self, env):
        """Set environment variables for new user profile."""
        home = self.profileName
        if "win" in sys.platform:
            env["USERPROFILE"] = home
            env["APPDATA"] = os.path.join(home, "AppData/Roaming")
            env["LOCALAPPDATA"] = os.path.join(home, "AppData/Local")
            env["TMP"] = os.path.join(home, "AppData/Local/Temp")
            env["TEMP"] = os.path.join(home, "AppData/Local/Temp")
        elif "lin" in sys.platform:
            env["HOME"] = home

    def exists(self):
        """Check if unique profile name already exists."""
        if os.path.exists(self.profileName):
            return True
        else:
            return False

    def mkdirs(self):
        """Create unique user profile & set up directory tree."""
        os.makedirs(self.profileName)
        if "win" in sys.platform:
            locs = ["AppData/Roaming", "AppData/Local", "AppData/Local/Temp", "Documents"]
        elif "lin" in sys.platform:
            locs = [".config", "temp/reports"]

        for loc in locs:
            os.makedirs(os.path.join(self.profileName, loc))

    def copy_profiles(self):
        """Copy directories from current user into new user profile."""
        if "win" in sys.platform:
            locs = ["AppData/Roaming/Ansys", "AppData/Local/Ansys"]
        elif "lin" in sys.platform:
            locs = [".mw/Application Data/Ansys", ".config/Ansys"]
        for loc in locs:
            shutil.copytree(
                os.path.join(self.defaultProfile, loc), os.path.join(self.profileName, loc)
            )

def set_private_appdata(pid) -> TmpUser:
    """Set up unique user sessions when running parallel instances."""
    defaultProfile = os.path.expanduser("~")
    profileName = os.path.join(defaultProfile, f"PyMechanical-{pid}")

    newProfile = TmpUser(defaultProfile, profileName)

    if newProfile.exists():
        newProfile.delete_dir()

    newProfile.mkdirs()

    newProfile.copy_profiles()

    newProfile.set_env(os.environ)

    warnings.warn(
        "Using the private_appdata option creates temporary directories when "
        "running the pymechanical instances in parallel. "
        f"There may be leftover files in {profileName}."
    )

    return newProfile