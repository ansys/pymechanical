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
"""Client for Mechanical services."""

import os
import time

import rpyc

class Client:
    """Client for connecting to Mechanical services."""

    def __init__(self, host: str, port: int, timeout: float = 60.0):
        """Initialize the client.

        Parameters
        ----------
        host : str, optional
            IP address to connect to the server.  The default is ``None``
            in which case ``localhost`` is used.
        port : int, optional
            Port to connect to the Mecahnical server. The default is ``None``,
            in which case ``10000`` is used.
        timeout : float, optional
            Maximum allowable time for connecting to the Mechanical server.
            The default is ``60.0``.

        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.connection = None
        self.root = None
        self._connect()

    def __getattr__(self, attr):
        if hasattr(self.root, attr):
            return getattr(self.root, attr)
        propget_name = f"propget_{attr}"
        if hasattr(self.root, propget_name):
            exposed_fget =  getattr(self.root, propget_name)
            return exposed_fget()
        return self.__dict__.items[attr]
    """
    def __setattr__(self, attr, value):
        if hasattr(self.root, attr):
            inner_prop = getattr(self.root.__class__, attr)
            if isinstance(inner_prop, property):
                inner_prop.fset(self.root, value)
        else:
            super().__setattr__(attr, value)
    """

    def _connect(self):
        self._wait_until_ready()
        self.connection = rpyc.connect(self.host, self.port)
        self.root = self.connection.root
        print(f"Connected to {self.host}:{self.port}")
        # setattr(self.root, "close", self.close)
        # setattr(self.root, "upload", self.upload)
        # setattr(self.root, "download", self.download)
        print(f"Installed methods")

    def _wait_until_ready(self):
        t_max = time.time() + self.timeout
        while time.time() < t_max:
            try:
                conn = rpyc.connect(self.host, self.port)
                conn.ping()  # Simple ping to check if the connection is healthy
                conn.close()
                print("Server is ready to connect")
                break
            except:
                time.sleep(2)
        else:
            raise TimeoutError(
                f"Server at {self.host}:{self.port} not ready within {self.timeout} seconds."
            )

    def close(self):
        """Close the connection."""
        self.connection.close()
        print(f"Connection to {self.host}:{self.port} closed")

    from ansys.mechanical.core.mechanical import DEFAULT_CHUNK_SIZE

    def upload(
        self,
        file_name,
        file_location_destination=None,
        chunk_size=DEFAULT_CHUNK_SIZE,
        progress_bar=False,
    ):
        print(f"arg: {file_name}, {file_location_destination}")
        print()
        if not os.path.exists(file_name):
            print(f"File {file_name} does not exist.")
            return
        file_base_name = os.path.basename(file_name)
        remote_path = os.path.join(file_location_destination, file_base_name)

        with open(file_name, "rb") as f:
            file_data = f.read()
            self.root.exposed_upload(remote_path, file_data)

        print(f"File {file_name} uploaded to {file_location_destination}")

    def download(
        self,
        files,
        target_dir=None,
        chunk_size=DEFAULT_CHUNK_SIZE,
        progress_bar=None,
        recursive=False,
    ):
        """Download a file from the server."""

        os.makedirs(target_dir, exist_ok=True)

        response = self.root.exposed_download(files)

        if isinstance(response, dict) and response["is_directory"]:
            for relative_file_path in response["files"]:
                full_remote_path = os.path.join(files, relative_file_path)
                local_file_path = os.path.join(target_dir, relative_file_path)
                local_file_dir = os.path.dirname(local_file_path)
                os.makedirs(local_file_dir, exist_ok=True)

                self._download_file(full_remote_path, local_file_path, chunk_size, overwrite=True)
        else:
            self._download_file(
                files, os.path.join(target_dir, os.path.basename(files)), chunk_size, overwrite=True
            )

    def _download_file(self, remote_file_path, local_file_path, chunk_size=1024, overwrite=False):
        """Download a single file from the server."""

        if os.path.exists(local_file_path) and not overwrite:
            print(f"File {local_file_path} already exists locally. Skipping download.")
            return
        response = self.root.exposed_download(remote_file_path)
        if isinstance(response, dict):
            raise ValueError("Expected a file download, but got a directory response.")
        file_data = response

        # Write the file data to the local path
        with open(local_file_path, "wb") as f:
            f.write(file_data)

        print(f"File {remote_file_path} downloaded to {local_file_path}")

    # @property
    # def project_directory(self):
    #     return self.root.exposed_run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")
