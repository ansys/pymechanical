import mod

from ansys.mechanical.core.embedding.rpc import (
    MechanicalEmbeddedServer,
    run_python_script,
    run_python_script_from_file,
)

server = MechanicalEmbeddedServer(
    port=18861,
    version=241,
    methods=[run_python_script, run_python_script_from_file],
    # impl= mod.ServiceMethods,
)
server.start()
