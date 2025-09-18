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

""".. _ref_mesh:

Mesh
----

This section has helper scripts for Named Selections.
"""

# sphinx_gallery_start_ignore
from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

app = App(globals=globals())

# Download and import the geometry file
geom_file_path = download_file("example_06_bolt_pret_geom.agdb", "pymechanical", "00_basic")
geometry_import = Model.GeometryImportGroup.AddGeometryImport()

# Define geometry import format and preferences
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessLines = True
geometry_import_preferences.NamedSelectionKey = ""
geometry_import_preferences.ProcessNamedSelections = True
geometry_import_preferences.ProcessMaterialProperties = True

# Import the geometry into the project
geometry_import.Import(geom_file_path, geometry_import_format, geometry_import_preferences)
# sphinx_gallery_end_ignore


# Plot the imported geometry
app.plot()

# Print the Mechanical tree structure
app.print_tree()

# %%
# Set Global Mesh Settings
# ~~~~~~~~~~~~~~~~~~~~~~~~
mesh=Model.Mesh
mesh.ElementSize = Quantity('37 [mm]')
mesh.ElementOrder = ElementOrder.Linear



# %%
# Insert a Local Meshing Control for a Named Selection
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get all named selections and pick the one named "shank"
NSall = Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
use_nsel = [i for i in NSall if i.Name == "shank"][0]

# Add an Automatic Method mesh control scoped to the named selection
ms = Model.Mesh.AddAutomaticMethod()
ms.Location = use_nsel
ms.Method = ms.Method.AllTriAllTet
ms.Algorithm = ms.Algorithm.PatchConforming


# %%
# Generate Mesh
# ~~~~~~~~~~~~~
# Generate the mesh and print mesh object state
Model.Mesh.GenerateMesh()
print(Model.Mesh.ObjectState)


# %%
# Get Element Count of a meshed body
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Access mesh data
meshdata = DataModel.MeshDataByName("Global")
print(use_nsel.Ids[0])

# Retrieve body entity from geometry
geoBody = DataModel.GeoData.GeoEntityById(use_nsel.Ids[0])
body = Model.Geometry.GetBody(geoBody)

# Get mesh region corresponding to that body and print element count
meshregion = meshdata.MeshRegionById(geoBody.Id)
print(body.Name, meshregion.ElementCount)

# %%
# Clear generated mesh
# ~~~~~~~~~~~~~~~~~~~~~~~~
Model.Mesh.ClearGeneratedData()


# %%
# Insert a Sweep Method (Scoping Method: Named Selection)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get all named selections and pick the one named "bodies_5"
NSall = Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
use_nsel = [i for i in NSall if i.Name == "bodies_5"][0]

# Add a sweep meshing method scoped to the named selection
mesh = Model.Mesh
mesh_method = mesh.AddAutomaticMethod()
mesh_method.Location = use_nsel
mesh_method.Method = MethodType.Sweep

# %%
# Insert a Mesh Sizing Control (Scoping Method: Geometry Selection)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get all named selections and pick the one containing "bottom_surface"
NSall = Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
ns = [i for i in NSall if "bottom_surface" in i.Name][0]

# Extract bottom face and its edges
bot_face = DataModel.GeoData.GeoEntityById(ns.Ids[0])
body_ids = [edge.Id for edge in bot_face.Edges]

# Create a geometry selection object from edges
sel = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
sel.Ids = body_ids

# Apply mesh sizing control to the selection
mesh = Model.Mesh
mesh_sizing = mesh.AddSizing()
mesh_sizing.Location = sel
mesh_sizing.Behavior = SizingBehavior.Hard


# sphinx_gallery_start_ignore
# Save the project as a .mechdat file (currently commented out)

from pathlib import Path

output_path = Path.cwd() / "out"
test_mechdat_path = str(output_path / "test5.mechdat")
# app.save_as(test_mechdat_path, overwrite=True)


# Close the Mechanical application
app.close()
# Delete any downloaded example files
delete_downloads()
# sphinx_gallery_end_ignore
