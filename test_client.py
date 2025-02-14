import os
import subprocess
import sys
import typing

from ansys.mechanical.core.embedding.rpc.client import Client
from ansys.mechanical.core.embedding.rpc.server import DefaultServiceMethods

LAUNCHING = False
PORT = 18864
VER = 251


def launch_mechanical(port: int, version: int) -> typing.Tuple[DefaultServiceMethods, subprocess.Popen]:
    """Start the server as a subprocess using `port`."""
    port = port  # Port can be dynamic
    version = version
    server_enable_logging = True
    log_level = "INFO"
    server_script = r"/home/staff/dkunhamb/repos/pymechanical/tests/scripts/rpc_server_embedded.py"
    env_copy = os.environ.copy()
    print(f"enable_logging: {server_enable_logging}", "from server")
    p = subprocess.Popen([sys.executable, server_script, str(port), str(version), str(server_enable_logging), str(log_level)], env=env_copy)
    # TODO - pass a flag to client to cleanup_on_exit to match what Mechanical class does,
    #   which exits the process if true
    client_logging = True
    log_level = "INFO"
    client: DefaultServiceMethods = Client("localhost", PORT, enable_logging=client_logging, log_level=log_level)
    print(f"enable_logging: {client_logging} from client script with level {log_level}")
    return client, p


def test_launch():
    print(f"Launching server test_launch")
    client, client_process = launch_mechanical(PORT, VER)
    client.project_name = "hello"
    print(client.project_name)
    print(client.project_directory)
    print(client.run_python_script("ExtAPI.DataModel.Project"))
    client.exit()

def test_connect():
    client = Client("localhost", PORT)
    client.project_name = "hello"
    print(client.project_name)
    print(client.project_directory)
    print(client.run_python_script("ExtAPI.DataModel.Project"))
    client.exit()

if __name__ == "__main__":
    LAUNCHING = True
    if LAUNCHING:
        print("Launching true")
        test_launch()
    else:
        test_connect()
