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
"""Rpyc server."""

import threading
import time
import typing

from rpyc.utils.server import ThreadedServer

import ansys.mechanical.core as mech
import ansys.mechanical.core.embedding.utils as utils

from .service import MechanicalService


class Server:
    """Start rpyc server."""

    def __init__(
        self,
        service: typing.Type[MechanicalService],
        port: int = 18861,
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
        init_thread.start()

        while self._poster is None:
            time.sleep(0.01)
            continue
        print("done initializing mechanical")

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
