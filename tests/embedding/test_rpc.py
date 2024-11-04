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

import threading
import time

import pytest
import rpyc

from ansys.mechanical.core.embedding.rpc import Client, MechanicalEmbeddedServer


def get_project_name(app: "ansys.mechanical.core.embedding.App"):
    return app.DataModel.Project.Name


@pytest.fixture(scope="module")
def start_server():
    server = MechanicalEmbeddedServer(
        port=18861,
        version=242,
        methods=[get_project_name],
        # impl=mod.ServiceMethods,
    )
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    yield
    server.stop()
    server_thread.join()


def test_client(start_server, printer):
    c1 = Client("localhost", 18861)
    server = c1.root

    project_name = server.get_project_name()
    printer(project_name)
    assert project_name == "Project"
    c1.close()
