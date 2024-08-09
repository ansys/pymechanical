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
"""Utilities necessary for remote calls."""
import typing


class remote_method:
    """Decorator for passing remote methods.

    Parameters
    ----------
    func : Callable
        The function to be decorated as a remote method.
    """

    def __init__(self, func):
        """Initialize with the given function."""
        self._func = func

    def __call__(self, *args, **kwargs):
        """Call the stored function with provided arguments."""
        return self._func(*args, **kwargs)

    def __call_method__(self, instance, *args, **kwargs):
        """Call the stored function with the instance and provided arguments."""
        return self._func(instance, *args, **kwargs)

    def __get__(self, obj, objtype):
        """Return a partially applied method."""
        from functools import partial

        func = partial(self.__call_method__, obj)
        func._is_remote = True
        func.__name__ = self._func.__name__
        func._owner = obj
        return func


def get_remote_methods(obj) -> typing.Generator[typing.Tuple[str, typing.Callable], None, None]:
    """Yield names and methods of an object's remote methods.

    A remote method is identified by the presence of an attribute `_is_remote` set to `True`.

    Parameters
    ----------
    obj: Any
        The object to inspect for remote methods.

    Yields
    ------
    Generator[Tuple[str, Callable], None, None]
        A tuple containing the method name and the method itself
        for each remote method found in the object.
    """
    for methodname in dir(obj):
        if methodname.startswith("__"):
            continue
        method = getattr(obj, methodname)
        if not callable(method):
            continue
        if hasattr(method, "_is_remote") and method._is_remote is True:
            yield methodname, method
