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

"""Miscellaneous utilities."""
import ctypes
import os


def sleep(ms: int) -> None:
    """Non-blocking sleep for `ms` milliseconds.

    Mechanical should still work during the sleep.
    """
    import clr

    clr.AddReference("Ans.Common.WB1ManagedUtils")
    import Ansys

    Ansys.Common.WB1ManagedUtils.TestHelper().Wait(ms)


def load_library_windows(library: str) -> int:  # pragma: no cover
    """Load a library into the python process on windows."""
    if os.name != "nt":
        return 0

    try:
        LOAD_WITH_ALTERED_SEARCH_PATH = 8
        dll = ctypes.CDLL(
            library, use_errno=True, use_last_error=True, winmode=LOAD_WITH_ALTERED_SEARCH_PATH
        )
        return dll._handle
    except:
        return 0
