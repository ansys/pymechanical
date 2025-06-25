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

"""Mesh management for Ansys Mechanical"""


class MeshManager:
    """Handles mesh operations for the model."""

    def __init__(self, app):
        self.app = app

    def add_automatic_method(
        self,
        named_selection: str,
        method: str = "Sweep",
        element_order: str = "Linear",
        sweep_divisions: int = 1,
    ):
        """
        Add an automatic method with specified parameters to a named selection.
        """
        script = f"""
named_selection_obj = ExtAPI.DataModel.GetObjectsByName("{named_selection}")
meshmethod_obj = Model.Mesh.AddAutomaticMethod()
meshmethod_obj.ScopingMethod = GeometryDefineByType.Component
meshmethod_obj.NamedSelection = named_selection_obj[0]
meshmethod_obj.Method = MethodType.{method}
meshmethod_obj.ElementOrder = ElementOrder.{element_order}
meshmethod_obj.SweepNumberDivisions = {sweep_divisions}
"""
        self.app.run_python_script(script)

    def add_sizing(self, named_selection: str, element_size_mm: float):
        """
        Apply a sizing control to the named selection with a given element size.
        """
        script = f"""
named_selection_obj = ExtAPI.DataModel.GetObjectsByName("{named_selection}")
sizing_obj = Model.Mesh.AddSizing()
sizing_obj.NamedSelection = named_selection_obj[0]
sizing_obj.ElementSize = Quantity("{element_size_mm} [mm]")
"""
        self.app.run_python_script(script)

    def generate(self):
        """Generate mesh for the model."""
        self.app.run_python_script("Model.Mesh.GenerateMesh()")
