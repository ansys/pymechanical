import os
from typing import Union

from ansys.mechanical.core.embedding.rpc.client import Client
from ansys.mechanical.core.embedding.rpc.server import DefaultServiceMethods

from mod import ServiceMethods

port = int(os.getenv("SERVER_PORT"))  # Get port from env, default to 18861
host = os.getenv("SERVER_HOST")  # Get host from env, default to localhost

if __name__ == "__main__":
    print("Connecting to server at", host, port)
    client = Client(host, port)
    client2: Union[DefaultServiceMethods, ServiceMethods] = client
    client3: DefaultServiceMethods = client
    client1: ServiceMethods = client
    print(client1.project_directory)

    # Installed via class
    print("Project Name (Client 1):", client1.get_project_name())
    if 0:
        print("Project Name (Client 1):", client2.get_project_name())
    if 0:
        print("Project Name (Client 1):", client3.get_project_name())
    if 0:
        client1._helper_func()

    print("changing project name:", client2.change_project_name("PyAnsys"))
    print("Project Name (Client 1):", client1.get_project_name())

    client1.exit()

# TODO - get autocomplete with rpc methods.
