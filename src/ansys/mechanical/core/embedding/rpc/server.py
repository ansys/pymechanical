# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Remote Procedure Call (RPC) server."""

from pathlib import Path
import threading
import time
import typing

import rpyc
from rpyc.utils.server import ThreadedServer
import toolz

from ansys.mechanical.core.embedding.app import App
from ansys.mechanical.core.embedding.background import BackgroundApp
import ansys.mechanical.core.embedding.utils

from .utils import MethodType, get_free_port, get_remote_methods

# TODO : implement logging


class ForegroundAppBackend:
    """Backend for the python server where mechanical uses the main thread."""

    def __init__(self, app: App):
        """Create a new instance of ForegroundAppBackend."""
        self._app = app
        self._poster = app.poster

    def try_post(self, callable: typing.Callable) -> typing.Any:
        """Try to post to mechanical's main thread."""
        return self._poster.try_post(callable)

    def get_app(self) -> App:
        """Get the app object."""
        return self._app


class BackgroundAppBackend:
    """Backend for the python server where mechanical uses the background thread."""

    def __init__(self, backgroundapp: BackgroundApp):
        """Create a new instance of BackgroundAppBackend."""
        self._backgroundapp = backgroundapp

    def try_post(self, callable: typing.Callable) -> typing.Any:
        """Try to post to mechanical's main thread."""
        return self._backgroundapp.try_post(callable)

    def get_app(self) -> App:
        """Get the app object."""
        return self._backgroundapp.app


class MechanicalService(rpyc.Service):
    """Starts Mechanical app services."""

    def __init__(self, backend, functions=[], impl=[]):
        """Initialize the service."""
        super().__init__()
        self._backend = backend
        self._install_functions(functions)
        self._install_classes(impl)

    def _try_post(self, callable: typing.Callable) -> typing.Any:
        return self._backend.try_post(callable)

    def _get_app(self) -> App:
        return self._backend.get_app()

    def on_connect(self, conn):
        """Handle client connection."""
        print("Client connected")

    def on_disconnect(self, conn):
        """Handle client disconnection."""
        print("Client disconnected")

    def _install_functions(self, methods):
        """Install the given list of methods."""
        if not methods:
            return
        [self._install_function(method) for method in methods]

    def _install_classes(self, impl):
        """Install the given list of classes."""
        if not impl:
            return
        [self._install_class(_impl) for _impl in impl]

    def _install_class(self, impl):
        """Install methods from the given implemented class."""
        if impl is None:
            return
        for methodname, method, methodtype in get_remote_methods(impl):
            if methodtype == MethodType.METHOD:
                self._install_method(method)
            elif methodtype == MethodType.PROP:
                self._install_property(method, methodname)

    def _curry_property(self, prop, propname, get: bool):
        """Curry the given property."""

        def posted(*arg):
            def curried():
                if get:
                    return getattr(prop._owner, propname)
                else:
                    setattr(prop._owner, propname, *arg)

            return self._try_post(curried)

        return posted

    def _curry_method(self, method, realmethodname):
        """Curry the given method."""

        def posted(*args, **kwargs):
            def curried():
                original_method = getattr(method._owner, realmethodname)
                result = original_method(*args, **kwargs)
                return result

            return self._try_post(curried)

        return posted

    def _curry_function(self, methodname):
        """Curry the given function."""
        wrapped = getattr(self, methodname)
        curried_method = toolz.curry(wrapped)

        def posted(*args, **kwargs):
            def curried():
                return curried_method(self._get_app(), *args, **kwargs)

            return self._try_post(curried)

        return posted

    def _install_property(self, prop: property, propname: str):
        """Install property with inner and exposed pairs."""
        if prop.fget:
            exposed_get_name = f"exposed_propget_{propname}"

            def exposed_propget():
                """Convert to exposed getter."""
                f = self._curry_property(prop.fget, propname, True)
                result = f()
                return result

            setattr(self, exposed_get_name, exposed_propget)
        if prop.fset:
            exposed_set_name = f"exposed_propset_{propname}"

            def exposed_propset(arg):
                """Convert to exposed getter."""
                f = self._curry_property(prop.fset, propname, True)
                result = f(arg)
                return result

            setattr(self, exposed_set_name, exposed_propset)

    def _install_method(self, method):
        methodname = method.__name__
        self._install_method_with_name(method, methodname, methodname)

    def _install_method_with_name(self, method, methodname, innername):
        """Install methods of impl with inner and exposed pairs."""
        exposed_name = f"exposed_{methodname}"

        def exposed_method(*args, **kwargs):
            """Convert to exposed method."""
            f = self._curry_method(method, innername)
            result = f(*args, **kwargs)
            return result

        setattr(self, exposed_name, exposed_method)

    def _install_function(self, function):
        """Install a functions with inner and exposed pairs."""
        exposed_name = f"exposed_{function.__name__}"
        inner_name = f"inner_{function.__name__}"

        def inner_method(app, *args, **kwargs):
            """Convert to inner method."""
            return function(app, *args, **kwargs)

        def exposed_method(*args, **kwargs):
            """Convert to exposed method."""
            f = self._curry_function(inner_name)
            return f(*args, **kwargs)

        setattr(self, inner_name, inner_method)
        setattr(self, exposed_name, exposed_method)

    def exposed_service_upload(self, remote_path, file_data):
        """Handle file upload request from client."""
        if not remote_path:
            raise ValueError("The remote file path is empty.")

        remote_dir = Path(remote_path).parent

        if remote_dir:
            remote_dir.mkdir(parents=True, exist_ok=True)

        with Path(remote_path).open("wb") as f:
            f.write(file_data)

        print(f"File {remote_path} uploaded successfully.")

    def exposed_service_download(self, remote_path):
        """Handle file download request from client."""
        # Check if the remote file exists
        if not Path(remote_path).exists():
            raise FileNotFoundError(f"The file {remote_path} does not exist on the server.")

        if Path(remote_path).is_dir():
            files = []
            remote_path_obj = Path(remote_path)
            for file_path in remote_path_obj.rglob("*"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(remote_path_obj)
                    files.append(str(relative_path))
            return {"is_directory": True, "files": files}

        with Path(remote_path).open("rb") as f:
            file_data = f.read()

        print(f"File {remote_path} downloaded successfully.")
        return file_data

    def exposed_service_exit(self):
        """Exit the server."""
        print("Shutting down server ...")
        self._exit_f()
        print("Server stopped")


class MechanicalEmbeddedServer:
    """Start rpc server."""

    def __init__(
        self,
        port: int = None,
        version: int = None,
        methods: typing.List[typing.Callable] = [],
        impl: typing.List = [],
    ):
        """Initialize the server."""
        self._exited = False
        use_background_app = False
        if use_background_app:
            self._app_instance = BackgroundApp(version=version)
            self._backend = BackgroundAppBackend(self._app_instance)
        else:
            self._app_instance = App(version=version)
            self._backend = ForegroundAppBackend(self._app_instance)
        self._port = get_free_port(port)
        self._install_methods(methods)
        self._install_classes(impl)
        self._server = ThreadedServer(self._create_service(), port=self._port)

    def _create_service(self):
        service = MechanicalService(self._backend, self._methods, self._impl)

        def exit_f():
            self.stop()

        service._exit_f = exit_f
        return service

    def _is_stopped(self):
        return self._app_instance is None

    def _wait_exit(self) -> None:
        if self._exit_thread is None:
            return
        self._exit_thread.join()

    def _start_background_app(self) -> None:
        """Start server on specified port."""
        self._exit_thread: threading.Thread = None
        self._server.start()
        print("Server exited!")
        self._wait_exit()
        self._exited = True

    def _stop_background_app(self):
        """Return immediately but will stop the server.

        Mechanical is running on the background but
        the rpyc server is running on the main thread
        this signals for the server to stop, and the main
        thread will wait until the server has stopped.
        """

        def stop_f():  # wait for all connections to close
            while len(self._server.clients) > 0:
                time.sleep(0.005)
            self._app_instance.stop()
            self._app_instance = None
            self._backend = None
            self._server.close()
            self._exited = True

        self._exit_thread = threading.Thread(target=stop_f)
        self._exit_thread.start()

    def _start_foreground_app(self):
        self._server_stopped = False

        def start_f():
            print("Server started!")
            self._server.start()
            print("Server exited!")

        self._server_thread = threading.Thread(target=start_f)
        self._server_thread.start()
        while True:
            if self._server_stopped:
                break
            try:
                ansys.mechanical.core.embedding.utils.sleep(40)
            except Exception as e:
                print(f"An error occurred: {e}")
        self._server_thread.join()

    def _stop_foreground_app(self):
        self._server_stopped = True
        self._server.close()
        # self._server_thread.join()

    def _get_app_repr(self) -> str:
        def f():
            return repr(self._backend.get_app())

        return self._backend.try_post(f)

    def start(self) -> None:
        """Start server on specified port."""
        print(
            f"Starting mechanical application in server.\n"
            f"Listening on port {self._port}\n{self._get_app_repr()}"
        )
        if isinstance(self._app_instance, BackgroundApp):
            self._start_background_app()
        else:
            self._start_foreground_app()

    def stop(self) -> None:
        """Stop the server."""
        if self._is_stopped():
            raise Exception("already stopped!")
        if isinstance(self._app_instance, BackgroundApp):
            self._stop_background_app()
        else:
            self._stop_foreground_app()

    def _install_classes(self, impl: typing.Union[typing.Any, typing.List]) -> None:
        app = self._backend.get_app()
        if impl and not isinstance(impl, list):
            impl = [impl]
        self._impl = [i(app) for i in impl] if impl else []

    def _install_methods(
        self, methods: typing.Union[typing.Callable, typing.List[typing.Callable]]
    ) -> None:
        if methods and not isinstance(methods, list):
            methods = [methods]
        self._methods = methods if methods is not None else []
