from server_global_poster import MechanicalService, Server

import mod

# option A


server = Server(
    service=MechanicalService,
    port=18861,
    version=242,
    methods=[mod.get_project_name, mod.get_model_name, mod.change_project_name],
    # impl=ServiceMethods
)
server.start()
