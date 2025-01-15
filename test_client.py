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
    server_script = r"D:\PyAnsys\Repos\pymechanical\tests\scripts\rpc_server.py"
    env_copy = os.environ.copy()
    subprocess.Popen([sys.executable, server_script, str(port), str(version)], env=env_copy)
    # TODO - pass a flag to client to cleanup_on_exit to match what Mechanical class does, which exits the process if true
    client: DefaultServiceMethods = Client("localhost", PORT)
    return client


if __name__ == "__main__":
    LAUNCHING = True
    if LAUNCHING:
        client: DefaultServiceMethods = None
        print(f"Launching server...")
        client = launch_mechanical(PORT, VER)
    else:
        client = Client("localhost", PORT)

    # c2: DefaultServiceMethods = launch_server() => creates client, returns client.roo

    client.project_name = "hello"
    print(client.project_name)
    print(client.project_directory)
    print(client.run_python_script("""get_myname()"""))
    print(client.project_directory)
    # client.change_project_name("lol")
    # print(client.get_project_name())
    # print(client.run_python_script("ExtAPI.DataModel.Project", False, "WARNING", 2000))

    # print(
    #     client.run_python_script(
    #         "ExtAPI.DataModel.Project",
    #         enable_logging=False,
    #         log_level="WARNING",
    #         progress_interval=2000,
    #     )
    # )
    # print(client.project_directory)

    # will this work ? since file is not in server
# try:
#     server.run_python_script("import test")
# except Exception as e:
#     print(f"Caught unexpected error: {e}")
#     c2.close()


# upload and download files
# tests
#   -Add markers
