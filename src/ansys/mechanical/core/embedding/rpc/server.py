# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

import os
import threading
import time
import typing

import rpyc
from rpyc.utils.server import ThreadedServer
import toolz

import ansys.mechanical.core as mech
import ansys.mechanical.core.embedding.utils as utils

from .utils import MethodType, get_remote_methods

# TODO : implement logging




class MechanicalService(rpyc.Service):
    """Starts Mechanical app services."""

    def __init__(self, app, poster, functions=[], impl=None):
        """Initialize the service."""
        super().__init__()
        self._app = app
        self._poster = poster
        self._install_functions(functions)
        self._install_class(impl)
        self.EMBEDDED = True

    def _install_functions(self, methods):
        """Install the given list of methods."""
        [self._install_function(method) for method in methods]

    def _install_class(self, impl):
        """Install methods from the given implemented class."""
        print("install class")
        if impl is None:
            return
        print("methods")
        for methodname, method, methodtype in get_remote_methods(impl):
            print(f"installing {methodname} of {impl}")
            if methodtype == MethodType.METHOD:
                self._install_method(method)
            elif methodtype == MethodType.PROP:
                self._install_property(method)

    def on_connect(self, conn):
        """Handle client connection."""
        print("Client connected")
        print(self._app)

    def on_disconnect(self, conn):
        """Handle client disconnection."""
        print("Client disconnected")

    def _curry_method(self, method, realmethodname):
        """Curry the given method."""

        def posted(*args):
            def curried():
                original_method = getattr(method._owner, realmethodname)
                result = original_method(*args)
                return result

            return self._poster.post(curried)

        return posted

    def _curry_function(self, methodname):
        """Curry the given function."""
        wrapped = getattr(self, methodname)
        curried_method = toolz.curry(wrapped)

        def posted(*args, **kwargs):
            def curried():
                return curried_method(self._app, *args, **kwargs)

            return self._poster.post(curried)

        return posted

    def _install_property(self, property: property):
        """Install property with inner and exposed pairs."""
        # TODO: check how rpyc has property
        print("installing property")

    def _install_method(self, method):
        """Install methods of impl with inner and exposed pairs."""
        exposed_name = f"exposed_{method.__name__}"
        inner_name = f"inner_{method.__name__}"

        def inner_method(*args):
            """Convert to inner method."""
            result = method(*args)
            return result

        def exposed_method(*args):
            """Convert to exposed method."""
            f = self._curry_method(method, method.__name__)
            result = f(*args)
            return result

        setattr(self, inner_name, inner_method)
        setattr(self, exposed_name, exposed_method)

    def _install_function(self, function):
        """Install a functions with inner and exposed pairs."""
        print(f"Installing {function}")
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

    # TODO: Add service for run_script
    def exposed_upload(self, remote_path, file_data):
        if not remote_path:
            raise ValueError("The remote file path is empty.")

        remote_dir = os.path.dirname(remote_path)

        if remote_dir:
            os.makedirs(remote_dir, exist_ok=True)

        with open(remote_path, "wb") as f:
            f.write(file_data)

        print(f"File {remote_path} uploaded successfully.")

    def exposed_download(self, remote_path):
        """Handle file download request from client."""
        # Check if the remote file exists
        if not os.path.exists(remote_path):
            raise FileNotFoundError(f"The file {remote_path} does not exist on the server.")

        if os.path.isdir(remote_path):
            files = []
            for dirpath, _, filenames in os.walk(remote_path):
                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    relative_path = os.path.relpath(full_path, remote_path)
                    files.append(relative_path)
            return {"is_directory": True, "files": files}

        with open(remote_path, "rb") as f:
            file_data = f.read()

        print(f"File {remote_path} downloaded successfully.")
        return file_data


class MechanicalEmbeddedServer:
    """Start rpc server."""

    def __init__(
        self,
        service: typing.Type[rpyc.Service] = MechanicalService,
        port: int = None,
        version: int = None,
        methods: typing.List[typing.Callable] = [],
        impl=None,
    ):
        """Initialize the server."""
        self._exited = False
        self._app: mech.App = None
        self._poster = None
        self._port = port
        self._service = service
        self._methods = methods
        init_thread = threading.Thread(target=self._start_app, args=(version,))
        print("initializing mechanical")
        no_start = False
        if not no_start:
            init_thread.start()

            # TODO: Add check for port
            while self._poster is None:
                time.sleep(0.01)
                continue
            print("done initializing mechanical")

        if impl is None:
            self._impl = None
        else:
            self._impl = impl(self._app)

        my_service = self._service(self._app, self._poster, self._methods, self._impl)
        self._server = ThreadedServer(my_service, port=self._port)

    def start(self) -> None:
        """Start server on specified port."""
        print(
            f"starting mechanical application in server."
            f"Listening on port {self._port}\n{self._app}"
        )
        self._server.start()
        """try:
            try:
                conn.serve_all()
            except KeyboardInterrupt:
                print("User interrupt!")
        finally:
            conn.close()"""
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

    def stop(self) -> None:
        """Stop the server."""
        print("Stopping the server...")
        self._server.close()
        self._exited = True  # Signal the application loop to exit
        print("Server stopped.")


from .utils import remote_method


class DefaultServiceMethods:
    def __init__(self, app):
        print("init DefaultServiceMethods")
        self._app = app

    def __repr__(self):
        return '"ServiceMethods instance"'

    # @property
    @remote_method
    def get_project_name(self):
        return self.helper_func()

    def helper_func(self):
        return self._app.DataModel.Project.Name

    """
    @remote_method
    def get_model_name(self):
        return self._app.Model.Name

    def get_model_name_no_wrapper(self):
        return self._app.Model.Name

    @remote_method
    def change_project_name(self, name: str):
        self._app.DataModel.Project.Name = name
    """


class MechanicalDefaultServer(MechanicalEmbeddedServer):
    def __init__(self, **kwargs):
        super().__init__(service=MechanicalService, impl=DefaultServiceMethods, **kwargs)
