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

from .geo import GeometryGroup

"""Model and geometry apis."""


class Model:
    """Model object."""

    def __init__(self, app):
        """Initialize the model with the application instance."""
        self.app = app

    def add_geometry_group(self, name: str):
        """Add a geometry import group to the model."""
        self.app.run_python_script(f"{name} = Model.GeometryImportGroup.AddGeometryImport()")
        return GeometryGroup(self.app, name)

    def add_static_structural_analysis(self):
        """Add a static structural analysis to the model."""
        self.app.run_python_script("Model.AddStaticStructuralAnalysis()")
        return Analysis(self.app, "StaticStructural")

    def add_steady_state_thermal_analysis(self):
        """Add a steady state thermal analysis to the model."""
        self.app.run_python_script("Model.AddSteadyStateThermalAnalysis()")
        return Analysis(self.app, "SteadyStateThermal")


class Analysis:
    """Represents an analysis in the model."""

    def __init__(self, app, analysis_type: str):
        self.app = app
        self.analysis_type = analysis_type

    def __repr__(self):
        return f"<Analysis: {self.analysis_type}>"
    