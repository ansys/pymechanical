import mod

from ansys.mechanical.core.embedding.rpc import (
    MechanicalService,
    Server,
    run_python_script,
    run_python_script_from_file,
)

# old: launch_mechanical
# server = RemoteMechanical(port=,version=)

"""
option 1, derive from the grpc-compatible implementation of the remote server and add
more remote methods to it

class MyRemoteMechanical(RemoteMechanical):
    def __init__(self, ***):
        super().__init__(self, kwargs)
    @remote_method
    def my_remote_method(self):
        return 1

option 2, implement a remote server providing all needed remote methods

"""
server = Server(
    service=MechanicalService,
    port=18861,
    version=242,
    # methods=[mod.run_python_script, mod.run_python_script_file, mod.download],
    # methods=[mod.get_project_name, mod.get_model_name],
    methods=[run_python_script, run_python_script_from_file],
    impl=mod.ServiceMethods,
)
server.start()
