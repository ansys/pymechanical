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


class NamedSelectionManager:
    """Handles creation of named selections."""

    def __init__(self, app):
        self.app = app

    def create_from_ids(self, name: str, body_ids: list[int]):
        """
        Create a named selection using a list of body IDs, directly passed into script.
        """
        script = f"""
body_ids = {body_ids}  # Injected directly

selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
selection.Ids = body_ids
ExtAPI.SelectionManager.NewSelection(selection)

named_sel = ExtAPI.DataModel.Project.Model.AddNamedSelection()
named_sel.Name = "{name}"
named_sel.Location = selection

ExtAPI.SelectionManager.ClearSelection()
"""
        self.app.run_python_script(script)

    def list_all(self) -> list[str]:
        import json

        script = """
import json
ns_list = ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[
    Ansys.ACT.Automation.Mechanical.NamedSelection
](True)
json.dumps([ns.Name for ns in ns_list])
"""
        json_str = self.app.run_python_script(script)
        return json.loads(json_str)
