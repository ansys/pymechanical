# my_client.py
import rpyc

import mod
#import server_methods as mod

if __name__ == "__main__":
    # Connect to the server
    c1 = rpyc.connect("localhost", 18861)

    server: mod = c1.root

    print("connected to server")
    # Access and invoke exposed attributes and methods
    print("Project Name (Client 1):", server.get_project_name())
    print("Model Name (Client 1):", server.get_model_name())
    # Close the connection
    c1.close()

    print("end of first connection")

    # Connect again with a new client
    c2 = rpyc.connect("localhost", 18861)
    server: mod = c2.root
    # Access and invoke exposed attributes and methods
    print("before changing project name")
    server.change_project_name("bar")
    print("Project Name (Client 2):", server.get_project_name())
    print("Project Name (Client 2):", server.get_model_name())

    # Close the connection
    c2.close()
