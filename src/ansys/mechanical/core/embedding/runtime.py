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

"""Runtime initialize for pythonnet in embedding."""

import os

from ansys.mechanical.core.embedding.logger import Logger


def __register_container_codecs():
    import Python.Runtime.Codecs as codecs

    codecs.ListDecoder.Instance.Register()
    codecs.SequenceDecoder.Instance.Register()
    codecs.IterableDecoder.Instance.Register()


def __register_function_codec():
    import clr

    clr.AddReference("Ansys.Mechanical.CPython")
    import Ansys

    Ansys.Mechanical.CPython.Codecs.FunctionCodec.Register()


def initialize(version: int) -> None:
    """Initialize the runtime.

    Pythonnet is already initialized but we need to
    do some special codec handling to make sure the
    interop works well for Mechanical. These are
    need to handle (among other things) list and other
    container conversions between C# and python
    """
    Logger.info("Initialize pythonnet interop handling")
    __register_container_codecs()
    if version >= 242 or os.name == "nt":
        # function codec is distributed with pymechanical on linux only
        # at version 242 or later
        __register_function_codec()
