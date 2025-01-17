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

import json


def attach_geometry(part_file_path):
    geometry_import_group = Model.GeometryImportGroup
    geometry_import = geometry_import_group.AddGeometryImport()

    geometry_import_format = (
        Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
    )
    geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
    geometry_import.Import(part_file_path, geometry_import_format, geometry_import_preferences)

    return "success"


def generate_mesh():
    Model.Mesh.GenerateMesh()

    return "success"


def add_static_structural_analysis_bc_results():
    analysis = Model.AddStaticStructuralAnalysis()

    fixed_support = analysis.AddFixedSupport()

    selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    selection.Ids = [82]
    fixed_support.Location = selection

    pressure = analysis.AddPressure()

    selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    selection.Ids = [55]
    pressure.Location = selection

    pressure.Magnitude.Output.SetDiscreteValue(0, Quantity(1000, "Pa"))

    # region Context Menu Action
    total_deformation = analysis.Solution.AddTotalDeformation()

    return "success"


def get_ProjectDirectory():
    return ExtAPI.DataModel.Project.ProjectDirectory


def change_mesh_element_size(value):
    mesh = Model.Mesh
    mesh.ElementSize = Quantity(value, "m")
    mesh.GenerateMesh()


def change_pressure_value(value):
    pressure = DataModel.GetObjectsByName("Pressure")[0]
    pressure.Magnitude.Output.SetDiscreteValue(0, Quantity(value, "Pa"))


def return_mesh_statistics():
    mesh = Model.Mesh
    mesh_details = {"Nodes": mesh.Nodes, "Elements": mesh.Elements}
    json_text = json.dumps(mesh_details)
    return json_text


def solve_model():
    Model.Solve(True, "My Computer")


def return_total_deformation():
    td = DataModel.GetObjectsByName("Total Deformation")[0]
    total_deformation_details = {
        "Minimum": str(td.Minimum),
        "Maximum": str(td.Maximum),
        "Average": str(td.Average),
    }
    json_text = json.dumps(total_deformation_details)
    return json_text
