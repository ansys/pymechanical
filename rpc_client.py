import os
from typing import Union

from ansys.mechanical.core.embedding.rpc import Client
from ansys.mechanical.core.embedding.rpc import DefaultServiceMethods

from mod import ServiceMethods

port = int(os.getenv("SERVER_PORT", "18861"))  # Get port from env, default to 18861
host = os.getenv("SERVER_HOST", "localhost")  # Get host from env, default to localhost

if __name__ == "__main__":
    print("Connecting to server at", host, port)
    client = Client(host, port)
    client: Union[DefaultServiceMethods, ServiceMethods] = client
    print(client.project_directory)

    # Installed via class
    print("Project Name :", client.get_project_name())
   
    print("changing project name:", client.change_project_name("PyAnsys"))
    print("Project Name (Client 1):", client.get_project_name())

    client.exit()
