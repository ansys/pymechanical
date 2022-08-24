"""Initialize the package level imports."""
from ansys.mechanical.core.logging import Logger

# Create logger for package level use
LOG = Logger(level=logging.ERROR, to_file=False, to_stdout=True)
LOG.debug("Loaded logging module as LOG")

from ansys.mechanical.core.mechanical import (
    change_default_mechanical_path,
    close_all_local_instances,
    find_mechanical,
    get_mechanical_path,
    launch_mechanical,
)

# import few classes / functions
from ansys.mechanical.core.mechanical import Mechanical as Mechanical

# manage the package level ports
LOCAL_PORTS = []

from ansys.mechanical.core.pool import LocalMechanicalPool

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

BUILDING_GALLERY = False
