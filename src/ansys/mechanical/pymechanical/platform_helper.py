"""Contain platform related helper functions."""
import os


class PlatformHelper:
    """Contain platform related helper function(s)."""

    @staticmethod
    def is_windows():
        """Find if the host machine is windows or not.

        Returns
        -------
        Returns True if the host machine is Windows otherwise False
        """
        if os.name == "nt":
            return True

        return False
