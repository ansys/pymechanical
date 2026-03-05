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

"""Miscellaneous utilities."""

import ctypes
import os

TEST_HELPER = None


class GetterWrapper(object):
    """Wrapper class around an attribute of an object."""

    def __init__(self, obj, getter):
        """Create a new instance of GetterWrapper."""
        # immortal class which provides wrapped object
        self.__dict__["_immortal_object"] = obj
        # function to get the wrapped object from the immortal class
        self.__dict__["_get_wrapped_object"] = getter

    def __getattr__(self, attr):
        """Wrap getters to the wrapped object."""
        if attr in self.__dict__:
            return getattr(self, attr)
        return getattr(self._get_wrapped_object(self._immortal_object), attr)

    def __setattr__(self, attr, value):
        """Wrap setters to the wrapped object."""
        if attr in self.__dict__:
            setattr(self, attr, value)
        setattr(self._get_wrapped_object(self._immortal_object), attr, value)


def _get_test_helper():
    global TEST_HELPER
    if TEST_HELPER is not None:
        return TEST_HELPER
    import clr

    clr.AddReference("Ans.Common.WB1ManagedUtils")
    import Ansys

    TEST_HELPER = Ansys.Common.WB1ManagedUtils.TestHelper()
    return TEST_HELPER


def sleep(ms: int) -> None:
    """Non-blocking sleep for `ms` milliseconds.

    Mechanical should still work during the sleep.
    """
    _get_test_helper().Wait(ms)


def drain() -> None:
    """Execute all pending work on the main thread.

    Blocks until all the UI messages and other scheduled work complete.
    """
    _get_test_helper().Drain()


def load_library_windows(library: str) -> int:  # pragma: no cover
    """Load a library into the python process on windows."""
    if os.name != "nt":
        return 0

    try:
        load_with_altered_search_path = 8
        dll = ctypes.CDLL(
            library, use_errno=True, use_last_error=True, winmode=load_with_altered_search_path
        )
        return dll._handle
    except OSError:
        return 0
