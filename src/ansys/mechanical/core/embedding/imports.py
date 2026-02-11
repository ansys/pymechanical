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

"""Additional imports for embedded Mechanical."""

from __future__ import annotations

import typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.mechanical.core.embedding import App


def global_entry_points(app: App) -> typing.Dict:
    """Return the global entry points of the application."""
    global_vars = {}
    global_vars["ExtAPI"] = app.ExtAPI
    global_vars["DataModel"] = app.DataModel
    global_vars["Model"] = app.DataModel.Project.Model
    global_vars["Tree"] = app.DataModel.Tree
    global_vars["Graphics"] = app.ExtAPI.Graphics
    return global_vars


def global_variables(app: App, enums: bool = False) -> typing.Dict:
    """Return the Mechanical scripting global variables as a dict.

    It can be used to add all of these as global variables in python
    with this command:

    ``globals().update(global_variables(embedded_app))``

    To also import all the enums, set the parameter enums to true.
    """
    global_vars = global_entry_points(app)

    from ansys.mechanical.core.embedding.app import is_initialized
    from ansys.mechanical.core.embedding.transaction import Transaction

    global_vars["Transaction"] = Transaction

    # Import modules if the app is initialized
    if is_initialized():
        from ansys.mechanical.core.embedding.global_importer import (
            Ansys,
            MechanicalEnums,
            Point,
            Point2D,
            Point3D,
            Quantity,
            SectionPlane,
            System,
            Vector3D,
        )

        global_vars["Quantity"] = Quantity
        global_vars["System"] = System
        global_vars["Ansys"] = Ansys
        global_vars["MechanicalEnums"] = MechanicalEnums
        # Graphics
        global_vars["Point"] = Point
        global_vars["SectionPlane"] = SectionPlane
        # Math
        global_vars["Point2D"] = Point2D
        global_vars["Point3D"] = Point3D
        global_vars["Vector3D"] = Vector3D

    if enums:
        global_vars.update(get_all_enums())

    return global_vars


def get_all_enums() -> typing.Dict[str, typing.Any]:
    """Get all the enums as a dictionary."""
    import ansys.mechanical.core.embedding.enum_importer as enum_importer

    enums = {}
    for attr in dir(enum_importer):
        if not hasattr(enum_importer, attr):
            continue
        the_enum = getattr(enum_importer, attr)
        if type(the_enum).__name__ == "CLRMetatype":
            enums[attr] = the_enum
    return enums
