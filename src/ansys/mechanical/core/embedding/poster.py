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

"""Use the Poster class to post functions to Mechanical's main thread."""

import typing


class Poster:
    """Class which can post a python callable function to Mechanical's main thread."""

    def __init__(self):
        """Create a new instance of Poster."""
        import clr

        clr.AddReference("Ans.Common.WB1ManagedUtils")
        import Ans

        self._poster = Ans.Common.WB1ManagedUtils.TaskPoster

    def post(self, callable: typing.Callable):
        """Post the callable to Mechanical's main thread.

        The main thread needs to be receiving posted messages
        in order for this to work from a background thread. Use
        the `sleep` routine from the `utils` module to make
        Mechanical available to receive messages.

        Returns the result of `callable` if any.
        """
        import System

        func = System.Func[System.Object](callable)
        return self._poster.Get[System.Object](func)
