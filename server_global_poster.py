import threading
import time
import typing

import rpyc
from rpyc.utils.server import ThreadedServer
import toolz

import ansys.mechanical.core as mech
import ansys.mechanical.core.embedding.utils as utils

class remote_method:
    def __init__(self, func):
        self._func = func
    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)
    def __call_method__(self, instance, *args, **kwargs):
        return self._func(instance, *args, **kwargs)
    def __get__(self, obj, objtype):
        from functools import partial
        func = partial(self.__call_method__, obj)
        func._is_remote = True
        func.__name__ = self._func.__name__
        func._owner = obj
        return func

def get_remote_methods(obj) -> typing.Generator[typing.Tuple[str, typing.Callable], None, None]:
    for methodname in dir(obj):
        if methodname.startswith("__"):
            continue
        method = getattr(obj, methodname)
        if not callable(method):
            continue
        if hasattr(method, "_is_remote") and method._is_remote is True:
            yield methodname, method

class MechanicalService(rpyc.Service):
    def __init__(self, app, poster, functions=[], impl=None):
        super().__init__()
        self._app = app
        self._poster = poster
        self._install_functions(functions)
        self._install_class(impl)

    def _install_functions(self, methods):
        [self._install_function(method) for method in methods]

    def _install_class(self, impl):
        if impl is None:
            return
        for methodname, method in get_remote_methods(impl):
            print(f"installing {methodname} of {impl}")
            self._install_method(method)

    def on_connect(self, conn):
        print("Client connected")
        print(self._app)

    def on_disconnect(self, conn):
        print("Client disconnected")

    def _curry_method(self, method, realmethodname):
        def posted(*args):
            def curried():
                original_method = getattr(method._owner, realmethodname)
                result=original_method(*args)
                return result
            return self._poster.post(curried)

        return posted

    def _curry_function(self, methodname):
        wrapped = getattr(self, methodname)
        curried_method = toolz.curry(wrapped)

        def posted(*args):
            def curried():
                return curried_method(self._app, *args)
            return self._poster.post(curried)

        return posted

    def _install_method(self, method):
        # install the method with an inner/exposed pair
        exposed_name = f"exposed_{method.__name__}"
        inner_name = f"inner_{method.__name__}"

        def inner_method(*args):
            result = method(*args)
            return result

        def exposed_method(*args):
            f = self._curry_method(method, method.__name__)
            result = f(*args)
            return result

        setattr(self, inner_name, inner_method)
        setattr(self, exposed_name, exposed_method)

    def _install_function(self, function):
        # install the method with an inner/exposed pair
        print(f"Installing {function}")
        exposed_name = f"exposed_{function.__name__}"
        inner_name = f"inner_{function.__name__}"

        def inner_method(app, *args):
            return function(app, *args)

        def exposed_method(*args):
            f = self._curry_function(inner_name)
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
        impl = None,
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

        while self._poster is None:
            time.sleep(0.01)
            continue
        print("done initializing mechanical")

        self._impl = impl(self._app)
        my_service = self._service(self._app, self._poster, self._methods, self._impl)
        self._server = ThreadedServer(my_service, port=self._port)

    def start(self) -> None:
        print(
            f"starting mechanical application in server. Listening on port {self._port}\n{self._app}"
        )
        self._server.start()
        '''try:
            try:
                conn.serve_all()
            except KeyboardInterrupt:
                print("User interrupt!")
        finally:
            conn.close()'''
        self._exited = True

    def _start_app(self, version: int) -> None:
        print("starting app")
        self._app = mech.App(version=version)
        print("started app")
        self._poster = self._app.poster
        while True:
            if self._exited:
                break
            try:
                utils.sleep(40)
            except Exception as e:
                print(str(e))
                pass
        print("out of loop!")
