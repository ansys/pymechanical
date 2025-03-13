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
"""Remote Procedure Call (RPC) server."""

import fnmatch
import os

from .server import MechanicalEmbeddedServer
from .utils import remote_method

class DefaultServiceMethods:
    """Default service methods for MechanicalEmbeddedServer."""

    def __init__(self, app):
        """Initialize the DefaultServiceMethods."""
        self._app = app

    def __repr__(self):
        """Return the representation of the instance."""
        return '"ServiceMethods instance"'

    @remote_method
    def run_python_script(
        self, script: str, enable_logging=False, log_level="WARNING", progress_interval=2000
    ):
        """Run scripts using Internal python engine."""
        result = self._app.execute_script(script)
        return result

    @remote_method
    def run_python_script_from_file(
        self,
        file_path: str,
        enable_logging=False,
        log_level="WARNING",
        progress_interval=2000,
    ):
        """Run scripts using Internal python engine."""
        return self._app.execute_script_from_file(file_path)

    @remote_method
    def clear(self):
        """Clear the current project."""
        self._app.new()

    @property
    @remote_method
    def project_directory(self):
        """Get the project directory."""
        return self._app.execute_script("""ExtAPI.DataModel.Project.ProjectDirectory""")

    @remote_method
    def list_files(self):
        """List all files in the project directory."""
        list = []
        mechdbPath = self._app.execute_script("""ExtAPI.DataModel.Project.FilePath""")
        if mechdbPath != "":
            list.append(mechdbPath)
        rootDir = self._app.execute_script("""ExtAPI.DataModel.Project.ProjectDirectory""")

        for dirPath, dirNames, fileNames in os.walk(rootDir):
            for fileName in fileNames:
                list.append(os.path.join(dirPath, fileName))
        files_out = "\n".join(list).splitlines()
        if not files_out:  # pragma: no cover
            print("No files listed")
        return files_out

    @remote_method
    def _get_files(self, files, recursive=False):
        self_files = self.list_files()  # to avoid calling it too much

        if isinstance(files, str):
            if files in self_files:
                list_files = [files]
            elif "*" in files:
                list_files = fnmatch.filter(self_files, files)
                if not list_files:
                    raise ValueError(
                        f"The `'files'` parameter ({files}) didn't match any file using "
                        f"glob expressions in the remote server."
                    )
            else:
                raise ValueError(
                    f"The `'files'` parameter ('{files}') does not match any file or pattern."
                )

        elif isinstance(files, (list, tuple)):
            if not all([isinstance(each, str) for each in files]):
                raise ValueError(
                    "The parameter `'files'` can be a list or tuple, but it "
                    "should only contain strings."
                )
            list_files = files
        else:
            raise ValueError(
                f"The `file` parameter type ({type(files)}) is not supported."
                "Only strings, tuple of strings, or list of strings are allowed."
            )

        return list_files


class MechanicalDefaultServer(MechanicalEmbeddedServer):
    """Default server with default service methods."""

    def __init__(self, **kwargs):
        """Initialize the MechanicalDefaultServer."""
        super().__init__(impl=DefaultServiceMethods, **kwargs)
