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

"""Class for running Mechanical on a background thread."""

import atexit
import threading
import time
import typing

import ansys.mechanical.core as mech
from ansys.mechanical.core.embedding.poster import Poster
import ansys.mechanical.core.embedding.utils as utils


def _exit(background_app: "BackgroundApp"):
    """Stop the thread serving the Background App."""
    background_app.stop()
    atexit.unregister(_exit)


class BackgroundApp:
    """Background App."""

    __app: mech.App = None
    __app_thread: threading.Thread = None
    __stopped: bool = False
    __stop_signaled: bool = False
    __poster: Poster = None

    def __init__(self, **kwargs):
        """Construct an instance of BackgroundApp."""
        if BackgroundApp.__app_thread == None:
            BackgroundApp.__app_thread = threading.Thread(
                target=self._start_app, kwargs=kwargs, daemon=True
            )
            BackgroundApp.__app_thread.start()

            while BackgroundApp.__poster is None:
                time.sleep(0.05)
                continue
        else:
            assert (
                not BackgroundApp.__stopped
            ), "Cannot initialize a BackgroundApp once it has been stopped!"

            def new():
                BackgroundApp.__app.new()

            self.post(new)

        atexit.register(_exit, self)

    @property
    def app(self) -> mech.App:
        """Get the App instance of the background thread.

        It is not meant to be used aside from passing to methods using `post`.
        """
        return BackgroundApp.__app

    def post(self, callable: typing.Callable):
        """Post callable method to the background app thread."""
        assert not BackgroundApp.__stopped, "Cannot use background app after stopping it."
        return BackgroundApp.__poster.post(callable)

    def stop(self) -> None:
        """Stop the background app thread."""
        if BackgroundApp.__stopped:
            return
        BackgroundApp.__stop_signaled = True
        while True:
            time.sleep(0.05)
            if BackgroundApp.__stopped:
                break

    def _start_app(self, **kwargs) -> None:
        BackgroundApp.__app = mech.App(**kwargs)
        BackgroundApp.__poster = BackgroundApp.__app.poster
        while True:
            if BackgroundApp.__stop_signaled:
                break
            try:
                utils.sleep(40)
            except:
                pass
        BackgroundApp.__stopped = True
