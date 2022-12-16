import clr
import os
from pathlib import Path
import sys

from .resolver import resolve

INITIALIZED_VERSION = None

def initialize(version):
    global INITIALIZED_VERSION
    if INITIALIZED_VERSION != None:
        assert INITIALIZED_VERSION == version
        return

    def _initpath():
        install_path = Path(os.environ[f"AWP_ROOT{version}"])
        bin_path = install_path / "aisol" / "bin" / "winx64"
        sys.path.append(str(bin_path.resolve()))
        return install_path

    _installpath = _initpath()
    clr.AddReference("Ansys.Mechanical.Embedding")
    import Ansys
    resolve(version, _installpath)