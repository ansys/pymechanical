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


class GeometryGroup:
    """Geometry import group object for the model."""

    def __init__(self, app, group_name: str):
        """Initialize the geometry group with the application instance and group name."""
        self.app = app
        self.group_name = group_name

    def import_geometry(self, file_path: str):
        """Import geometry into the group."""
        script = f"""
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessNamedSelections = True
geometry_import_preferences.NamedSelectionKey = ""
{self.group_name}.Import(r"{file_path}", geometry_import_format, geometry_import_preferences)
"""
        self.app.run_python_script(script)


class GeoData:
    """Handles geometry information and body-level queries and operations."""

    def __init__(self, app):
        self.app = app

    def get_body_ids_by_name(self, name: str):
        """
        Returns list of body IDs whose names match exactly.
        """
        script = f"""
matched_ids = []
geo = ExtAPI.DataModel.GeoData
for asm in geo.Assemblies:
    for part in asm.Parts:
        for body in part.Bodies:
            if body.Name == "{name}":
                matched_ids.append(body.Id)
matched_ids
"""
        return self.app.run_python_script(script)

    def get_body_ids_by_prefix(self, prefix: str):
        """
        Returns list of body IDs whose names start with the given prefix.
        """
        script = f"""
import System
import json

bodyIds = System.Collections.Generic.List[System.Int32]()
geo = ExtAPI.DataModel.GeoData

for asm in geo.Assemblies:
    for part in asm.Parts:
        for body in part.Bodies:
            if body.Name.startswith("{prefix}"):
                bodyIds.Add(body.Id)

json.dumps(list(bodyIds))  # Serialize as JSON string
"""
        return self.app.run_python_script(script)

    def get_body_ids_excluding_prefix(self, prefix: str):
        """
        Returns list of body IDs whose names do NOT start with the given prefix.
        """
        script = f"""
import System
import json

bodyIds = System.Collections.Generic.List[System.Int32]()
geo = ExtAPI.DataModel.GeoData

for asm in geo.Assemblies:
    for part in asm.Parts:
        for body in part.Bodies:
            if not body.Name.startswith("{prefix}"):
                bodyIds.Add(body.Id)

json.dumps(list(bodyIds))  # Serialize as JSON string
    """
        return self.app.run_python_script(script)

    def assign_material_by_name(self, name: str, material: str):
        """
        Assign the given material to bodies with exact matching name.
        """
        script = f"""
parts = ExtAPI.DataModel.Project.Model.Geometry.Children
for part in parts:
    for body in part.Children:
        if body.Name == "{name}":
            body.Material = "{material}"
"""
        self.app.run_python_script(script)

    def assign_materials_by_prefix(self, prefix: str, material: str):
        """
        Assign the given material to all bodies whose name starts with the given prefix.
        """
        script = f"""
parts = ExtAPI.DataModel.Project.Model.Geometry.Children
for part in parts:
    for body in part.Children:
        if body.Name.startswith("{prefix}"):
            body.Material = "{material}"
"""
        self.app.run_python_script(script)

    def assign_materials_by_ids(self, body_ids: list[int], material: str):
        script = f"""
body_ids = {body_ids}  # Direct injection of list

parts = ExtAPI.DataModel.Project.Model.Geometry.Children
geo = ExtAPI.DataModel.GeoData
for asm in geo.Assemblies:
    for part in asm.Parts:
        for body in part.Bodies:
            if body.Id in body_ids:
                body_obj = ExtAPI.DataModel.GetObjectsByName(body.Name)
                if body_obj and len(body_obj) > 1:
                    body_obj[1].Material = "{material}"
                else:
                    body_obj[0].Material = "{material}"
"""
        self.app.run_python_script(script)
