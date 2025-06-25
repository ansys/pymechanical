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


class ExternalDataManager:
    """Handles external data imports like ECAD traces in Ansys Mechanical."""

    def __init__(self, app):
        self.app = app

    def import_ecad_trace(
        self, def_file: str, identifier: str, named_selection: str, trace_material: str
    ):
        script = f"""
external_data_files = Ansys.Mechanical.ExternalData.ExternalDataFileCollection()
external_data_files.SaveFilesWithProject = True

external_data_file = Ansys.Mechanical.ExternalData.ExternalDataFile()
external_data_files.Add(external_data_file)

external_data_file.Identifier = "{identifier}"
external_data_file.Description = ""
external_data_file.IsMainFile = False
external_data_file.FilePath = r"{def_file}"
external_data_file.ImportSettings = (
    Ansys.Mechanical.ExternalData.ImportSettingsFactory.GetSettingsForFormat(
        Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.ImportFormat.ECAD
    )
)

external_data_file.ImportSettings.UseDummyNetData = False
imported_trace_group = ExtAPI.DataModel.Project.Model.Materials.AddImportedTraceExternalData()
imported_trace_group.ImportExternalDataFiles(external_data_files)

all_traces = ExtAPI.DataModel.GetObjectsByType(
    Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.ImportedTrace
)
imp_trace = [t for t in all_traces if t.Parent.ObjectId == imported_trace_group.ObjectId][0]
imp_trace.Activate()

ns_list = ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[
    Ansys.ACT.Automation.Mechanical.NamedSelection
](True)
ns_object = [ns for ns in ns_list if ns.Name == "{named_selection}"][0]
imp_trace.Location = ns_object
imp_trace.PropertyByName("PROPID_ExternalData").InternalValue = 1

for layer in imp_trace.Layers:
    layer["Trace Material"] = "{trace_material}"

for via in imp_trace.Vias:
    via["Plating Material"] = "{trace_material}"

imp_trace.Import()
"""
        self.app.run_python_script(script)
