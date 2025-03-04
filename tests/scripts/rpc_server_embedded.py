# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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
"""Start rpc sever for embedded instance."""
import sys

import ansys.mechanical.core as mech
from ansys.mechanical.core.embedding.rpc import DefaultServiceMethods
from ansys.mechanical.core.embedding.rpc.server import MechanicalEmbeddedServer
from ansys.mechanical.core.embedding.rpc.utils import remote_method


def change_project_name_method(app: mech.App, name: str):
    """Change the project name of `app` to `name`."""
    app.DataModel.Project.Name = name


def get_project_name_method(app: mech.App):
    return app.DataModel.Project.Name


def get_model_name_method(app):
    return app.Model.Name


class ServiceMethods:
    def __init__(self, app):
        self._app = app

    def __repr__(self):
        return '"ServiceMethods instance"'

    @remote_method
    def get_model_name_impl(self):
        return self._app.Model.Name

    def get_model_name_no_wrapper(self):
        return self._app.Model.Name

    @remote_method
    def change_project_name_impl(self, name: str):
        self._app.DataModel.Project.Name = name

    @remote_method
    def get_project_name_impl(self):
        return self.helper_func()

    def helper_func(self):
        return self._app.DataModel.Project.Name


if __name__ == "__main__":
    _port = int(sys.argv[1])
    _version = int(sys.argv[2])

    server = MechanicalEmbeddedServer(
        port=_port,
        version=_version,
        impl=[DefaultServiceMethods, ServiceMethods],
        methods=[get_project_name_method, change_project_name_method, get_model_name_method],
    )
    server.start()
