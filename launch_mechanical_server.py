import os
import subprocess
import sys
import typing

from ansys.mechanical.core.embedding.rpc.client import Client
from ansys.mechanical.core import launch_mechanical

LAUNCHING = False
PORT = 18864
VER = 251




def test_launch():
    print(f"Launching server...")
    client = launch_mechanical(port=PORT, backend="python")
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
        test_launch()
    else:
        test_connect()
