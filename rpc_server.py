import os

from ansys.mechanical.core.embedding.rpc import (DefaultServiceMethods,
                                                 MechanicalEmbeddedServer)

import mod

port = int(os.getenv("SERVER_PORT", "18861"))  # Get port from env, default to 18861
print("Starting server at port", port)

server = MechanicalEmbeddedServer(
    port=port,
    # methods=[mod.get_project_name, mod.get_model_name],
    impl=[mod.ServiceMethods, DefaultServiceMethods],
)
server.start()
