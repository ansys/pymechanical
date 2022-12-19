"""Initialize the package level imports."""
import logging
from ansys.mechanical.core.logging import Logger

# Create logger for package level use
LOG = Logger(level=logging.ERROR, to_file=False, to_stdout=True)
LOG.debug("Loaded logging module as LOG")

from ansys.mechanical.core._version import __version__
from ansys.mechanical.core.mechanical import (
    change_default_mechanical_path,
    close_all_local_instances,
    find_mechanical,
    get_mechanical_path,
    launch_mechanical,
)

# import few classes / functions
from ansys.mechanical.core.mechanical import Mechanical as Mechanical

try:
    from ansys.mechanical.core.embedding import App, global_variables

    HAS_EMBEDDING = True
except:
    HAS_EMBEDDING = False

# manage the package level ports
LOCAL_PORTS = []

from ansys.mechanical.core.pool import LocalMechanicalPool

BUILDING_GALLERY = False
