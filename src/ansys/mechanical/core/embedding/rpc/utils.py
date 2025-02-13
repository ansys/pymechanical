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
"""Utilities necessary for remote calls."""
import typing
from typing import TypeVar, TypeVarTuple, Generic

TRet = TypeVar("TRet")
TArgs = TypeVarTuple("TArgs")

import collections.abc

import sys
if sys.version_info >= (3, 12):
    class _x_12:
        BAR=2
    q = _x_12
else:
    class _x_11:
        FOO=1
    q = _x_11


class remote_method(Generic[TRet, *TArgs]):
    """Decorator for passing remote methods."""

    def __init__(self, func):
        """Initialize with the given function."""
        self._func = func

    def __call__(self, *args, **kwargs):
        """Call the stored function with provided arguments."""
        return self._func(*args, **kwargs)

    def __call_method__(self, instance, *args, **kwargs):
        """Call the stored function with the instance and provided arguments."""
        return self._func(instance, *args, **kwargs)

    def __get__(self, obj, objtype) -> collections.abc.Callable[[TArgs], TRet]:
        """Return a partially applied method."""
        from functools import partial

        func = partial(self.__call_method__, obj)
        func._is_remote = True
        func.__name__ = self._func.__name__
        func._owner = obj
        return func

x = remote_method[bool, int, int, int](None).__get__(None, None)
y = remote_method[bool, int](None).__get__(None, None)
z = remote_method[bool](None).__get__(None, None)
x()
y()
z()



class MethodType:
    """Enum for method or property types."""

    METHOD = 0
    PROP = 1


def try_get_remote_method(methodname: str, obj: typing.Any) -> typing.Tuple[str, typing.Callable]:
    """Try to get a remote method."""
    method = getattr(obj, methodname)
    if not callable(method):
        return None
    if hasattr(method, "_is_remote") and method._is_remote is True:
        return (methodname, method)


def try_get_remote_property(attrname: str, obj: typing.Any) -> typing.Tuple[str, property]:
    """Try to get a remote property."""
    objclass: typing.Type = obj.__class__
    class_attribute = getattr(objclass, attrname)
    getmethod = None
    setmethod = None

    if class_attribute.fget:
        if isinstance(class_attribute.fget, remote_method):
            getmethod = class_attribute.fget
            getmethod._owner = obj
    if class_attribute.fset:
        if isinstance(class_attribute.fset, remote_method):
            setmethod = class_attribute.fset
            setmethod._owner = obj

    return (attrname, property(getmethod, setmethod))


def get_remote_methods(
    obj,
) -> typing.Generator[typing.Tuple[str, typing.Callable, MethodType], None, None]:
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
        for each remote method found in the object
    """
    print(f"Getting remote methods on {obj}")
    objclass = obj.__class__
    for attrname in dir(obj):
        if attrname.startswith("__"):
            continue
        print(attrname)
        if hasattr(objclass, attrname):
            class_attribute = getattr(objclass, attrname)
            if isinstance(class_attribute, property):
                attrname, prop = try_get_remote_property(attrname, obj)
                yield attrname, prop, MethodType.PROP
                continue
        result = try_get_remote_method(attrname, obj)
        if result != None:
            attrname, method = result
            yield attrname, method, MethodType.METHOD
