import threading
import time
import typing

import rpyc
from rpyc.utils.server import ThreadedServer
import toolz

import ansys.mechanical.core as mech
import ansys.mechanical.core.embedding.utils as utils


class MechanicalService(rpyc.Service):
    def __init__(self, app, poster, methods):
        super().__init__()
        self._app = app
        self._poster = poster
        [self._install_method(method) for method in methods]

    def on_connect(self, conn):
        print("Client connected")
        print(self._app)

    def on_disconnect(self, conn):
        print("Client disconnected")

    def _curry_method(self, methodname):
        wrapped = getattr(self, methodname)
        curried_method = toolz.curry(wrapped)
        print(type(curried_method))

        def posted(*args):
            def curried():
                return curried_method(self._app, *args)
            return self._poster.post(curried)

        return posted

    def _install_method(self, method):
        # install the method with an inner/exposed pair
        print(f"Installing {method}")
        exposed_name = f"exposed_{method.__name__}"
        inner_name = f"inner_{method.__name__}"
        setattr(self, inner_name, method)

        def inner_method(app, *args):
            return method(app, *args)

        def exposed_method(*args):
            f = self._curry_method(inner_name)
            return f(*args)

        setattr(self, inner_name, inner_method)
        setattr(self, exposed_name, exposed_method)


class Server:
    def __init__(
        self,
        service: typing.Type[MechanicalService],
        port: int = 18861,
        version: int = None,
        methods: typing.List[typing.Callable] = [],
    ):
        self._exited = False
        self._app: mech.App = None
        self._poster = None
        self._port = port
        self._service = service
        self._methods = methods
        init_thread = threading.Thread(target=self._start_app, args=(version,))
        print("initializing mechanical")
        init_thread.start()

        while self._app == None:
            time.sleep(0.01)
            continue
        print("done initializing mechanical")

        my_service = self._service(self._app, self._poster, self._methods)
        self._server = ThreadedServer(my_service, port=self._port)

    def start(self) -> None:
        print(
            f"starting mechanical application in server. Listening on port {self._port}\n{self._app}"
        )
        self._server.start()
        self._exited = True

    def _start_app(self, version: int) -> None:
        self._app = mech.App(version=version)
        self._poster = self._app.poster
        while True:
            if self._exited:
                break
            try:
                utils.sleep(400)
            except Exception as e:
                print(str(e))
                pass
        print("out of loop!")
