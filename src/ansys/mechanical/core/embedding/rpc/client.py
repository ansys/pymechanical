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

    def _connect(self):
        self._wait_until_ready()
        self.connection = rpyc.connect(self.host, self.port)
        self.root = self.connection.root
        print(f"Connected to {self.host}:{self.port}")

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
