
import os
import subprocess
import sys

from ansys.mechanical.core.embedding.rpc.client import Client
from ansys.mechanical.core.embedding.rpc.server import DefaultServiceMethods

LAUNCHING = False
PORT = 18864
VER = 242


def launch_mechanical(port: int, version: int) -> Client:
    """Start the server as a subprocess using `port`."""
    port = port  # Port can be dynamic
    version = version
    server_script = r"D:\PyAnsys\Repos\exp\pymechanical\tests\scripts\rpc_server_embedded.py"
    env_copy = os.environ.copy()
    subprocess.Popen([sys.executable, server_script, str(port), str(version)], env=env_copy)
    # TODO - pass a flag to client to cleanup_on_exit to match what Mechanical class does, which exits the process if true
    client = Client("localhost", PORT)
    return client


if __name__ == "__main__":
    LAUNCHING = True
    if LAUNCHING:
        client = None
        print(f"Launching server...")
        client = launch_mechanical(PORT, VER)
    else:
        client = Client("localhost", PORT)

    # c2: DefaultServiceMethods = launch_server() => creates client, returns client.roo

    #client.project_name = "hello"
    #print(client.project_name)

    print(client.project_directory)
    print(client.list_files())
    print(client.get_model_name())