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

"""Hook to register obsolete warnings."""

import typing
import warnings

# TODO: Investigate `warnings.showwarning = my_special_function` in order to better
#       control the printing behavior of warnings. But this is global state, so the
#       function should only affect warnings that are thrown here.


def _get_method_to_check(method_info: typing.Any) -> typing.Any:
    """Get the reflection method to check for obsolete attributes.

    If it's a getter or setter, it has to be done in a different way.
    """
    if not method_info.IsSpecialName:
        return method_info
    type_props = [prop for prop in method_info.DeclaringType.GetProperties()]
    getters = [t for t in type_props if t.GetGetMethod() == method_info]
    setters = [t for t in type_props if t.GetSetMethod() == method_info]
    if len(getters) > 0:
        return getters[0]
    if len(setters) > 0:
        return setters[0]
    return None


def _on_obsolete_message(sender: typing.Any, args: typing.Any):
    method_info = _get_method_to_check(args.Method)
    if not method_info:
        return

    attribs = method_info.GetCustomAttributes(True)
    obsolete_attributes = [
        attrib for attrib in attribs if attrib.GetType().ToString() == "System.ObsoleteAttribute"
    ]
    for obsolete_attribute in obsolete_attributes:
        message = f"Obsolete: '{method_info.Name}': {obsolete_attribute.Message}"
        warnings.warn(message, UserWarning, stacklevel=2)


def connect_warnings(app: "ansys.mechanical.core.embedding.app.App"):
    """Connect Mechanical warnings to the `warnings` Python module."""
    if int(app.version) < 241:
        return

    app._app.OnObsoleteMessage += _on_obsolete_message


def disconnect_warnings(app):
    """Disconnect Mechanical warnings from the `warnings` Python module."""
    if int(app.version) < 241:
        return

    app._app.OnObsoleteMessage -= _on_obsolete_message
