import os

from ansys.mechanical.core import launch_mechanical
from ansys.mechanical.core.examples import download_file

mechanical = launch_mechanical(batch=True, cleanup_on_exit=False)
print(mechanical)
result = mechanical.run_python_script("ExtAPI.DataModel.Project")
print(result)
