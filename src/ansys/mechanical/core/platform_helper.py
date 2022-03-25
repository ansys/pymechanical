import os


class PlatformHelper:
    @staticmethod
    def is_windows():
        if os.name == 'nt':
            return True

        return False
