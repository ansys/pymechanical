"""Initialize the package level imports."""
from ansys.mechanical.core.logging import Logger

# Create logger for package level use
LOG = Logger(level=logging.ERROR, to_file=False, to_stdout=True)
LOG.debug("Loaded logging module as LOG")

# import few classes / functions
from ansys.mechanical.core.mechanical import Mechanical as Mechanical
from ansys.mechanical.core.mechanical import close_all_local_instances, launch_mechanical

# manage the package level ports
LOCAL_PORTS = []

from ansys.mechanical.core.pool import LocalMechanicalPool

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))
