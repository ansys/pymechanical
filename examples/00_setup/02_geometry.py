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

""".. _ref_geometry:

Geometry
--------

This section contains a few utility scripts for working with Geometry,
including importing, analyzing, and accessing geometric data, as well
as utilizing it for downstream preprocessing operations in Mechanical
simulations. Coordinate Systems too are covered here.
"""

# %%
# Import Geometry
# ~~~~~~~~~~~~~~~

from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file
import logging
from ansys.mechanical.core.embedding.logger import Configuration

Configuration.configure(level=logging.DEBUG, to_stdout=True, base_directory=None)

app = App(globals=globals())

# Download the geometry file for the example
geom_file_path = download_file("example_06_bolt_pret_geom.agdb", "pymechanical", "00_basic")
# Alternatively, you can specify a local file path
# or geom_file_path = r"C:\geometry.agdb"

# Import the geometry into the Mechanical model
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()

# Set preferences for geometry import
geometry_import_preferences.ProcessLines = True
geometry_import_preferences.NamedSelectionKey = ""
geometry_import_preferences.ProcessNamedSelections = True
geometry_import_preferences.ProcessMaterialProperties = True

# Perform the geometry import
geometry_import.Import(geom_file_path, geometry_import_format, geometry_import_preferences)

# Plot the imported geometry
app.plot()

# Print the tree structure of the Mechanical model
app.print_tree()

# %%
# Get all bodies
# ~~~~~~~~~~~~~~~~~

# Retrieve all body objects from the geometry
body_objects = Model.Geometry.GetChildren(DataModelObjectCategory.Body, True)
# Alternatively, use the following method:
# bodies_objects = Model.Geometry.GetChildren(Ansys.ACT.Automation.Mechanical.Body, True)

# Extract geometric body wrappers for each body object
bodies = [body.GetGeoBody() for body in body_objects]  # GeoBodyWrapper
# or
# import itertools
# nested_list = [x.Bodies for x in ExtAPI.DataModel.GeoData.Assemblies[0].AllParts]
# bodies = list(itertools.chain(*nested_list))

# Access details of the first body object and its geometric properties
bo = body_objects[0]  # Access Object Details and RMB options
b = bodies[0]  # Access Geometric Properties: 'Area', 'GeoData', 'Centroid', 'Faces', etc.

# %%
# Find Body with Largest Volume
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set the active unit system to Standard NMM
ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMM

# Create a list of body names, volumes, and IDs for unsuppressed bodies
body_names_volumes = []
for body in body_objects:
    if body.Suppressed == 0 and body.Volume:
        body_names_volumes.append((body.Name, body.Volume, body.GetGeoBody().Id))

# Sort the list and retrieve the body with the largest volume
sorted_name_vol = sorted(body_names_volumes)
bodyname, volu, bodyid = sorted_name_vol.pop()

# Print details of the largest body
print(f"Unit System is: {ExtAPI.Application.ActiveUnitSystem}")
print(f"Name of the Largest Body: '{bodyname}'")
print(f"Its Volume: {round(volu.Value, 2)} {volu.Unit}")
print(f"Its id: {bodyid}")

# %%
# Find Body by its ID
# ~~~~~~~~~~~~~~~~~~~~~~
# Retrieve a body object using its ID
b2 = DataModel.GeoData.GeoEntityById(bodyid)
print(f"Body Name: {b2.Name}, Body Id: {b2.Id}")

# %%
# Find the Part that the body belongs to
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Retrieve the name of a body and the part it belongs to using its ID
body_name = DataModel.GeoData.GeoEntityById(59).Name
part_name = DataModel.GeoData.GeoEntityById(59).Part.Name
print(f"The Body named '{body_name}' belongs to the part named '{part_name}'")

# %%
# Find Body by its ID AND print its Faces, Centroid, etc.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Retrieve a body object and its faces, centroids, etc.
body2 = DataModel.GeoData.GeoEntityById(bodyid)

# Get face IDs and centroids for each face
face_ids = [face.Id for face in body2.Faces]
centroids_of_each_face = [DataModel.GeoData.GeoEntityById(face_id).Centroid for face_id in face_ids]

# Print face IDs and their centroids
for face_id, centroid in zip(face_ids, centroids_of_each_face):
    print(f"Face ID: {face_id}", f"List: {list(centroid)}")

# %%
# Get all Vertices
# ~~~~~~~~~~~~~~~~~~~

# Retrieve all vertex IDs from the geometry
vertices = []
geo = DataModel.GeoData
for asm in geo.Assemblies:
    for part in asm.Parts:
        for body in part.Bodies:
            for i in range(0, body.Vertices.Count):
                vertices.append(body.Vertices[i].Id)
print(f"Vertices: {vertices}")

# %%
# Get all edges of a given length
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Retrieve all edges with a specified length
ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMM
use_length = 0.100

geo = DataModel.GeoData
edgelist = []

# Iterate through assemblies, parts, and bodies to find edges of the given length
for asm in geo.Assemblies:
    for part in asm.Parts:
        for body in part.Bodies:
            for edge in body.Edges:
                if abs(edge.Length - use_length) <= use_length * 0.01:
                    edgelist.append(edge.Id)
print(f"Edgelist: {edgelist}")

# %%
# Get all circular edges of a given radius
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Retrieve all circular edges with a specified radius
import math

radius = 0.018  # Target radius
circumference = 2 * math.pi * radius  # Calculate circumference

geo = DataModel.GeoData
circlelist = []

# Iterate through assemblies, parts, and bodies to find circular edges
for asm in geo.Assemblies:
    for part in asm.Parts:
        for body in part.Bodies:
            for edge in body.Edges:
                if (
                    abs(edge.Length - circumference) <= circumference * 0.01
                    and str(edge.CurveType) == "GeoCurveCircle"
                ):
                    circlelist.append(edge.Id)
print(f"Circle list: {circlelist}")

# %%
# Get Radius of a selected edge
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Retrieve the radius of a specific edge if it is circular
my_edge = DataModel.GeoData.GeoEntityById(27)
my_edge_radius = my_edge.Radius if str(my_edge.CurveType) == "GeoCurveCircle" else 0.0
print(f"Edge radius is: {my_edge_radius}")

# %%
# Create a Named Selection from a list of body Ids
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create a named selection for a list of body IDs
mylist = [bodyid]

selection_manager = ExtAPI.SelectionManager
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
selection.Ids = mylist
selection_manager.NewSelection(selection)

ns2 = Model.AddNamedSelection()
ns2.Name = "bodies2"
ns2.Location = selection

# %%
# Find a Named Selection with a prefix
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Retrieve a named selection whose name starts with a specific prefix
NSall = Model.NamedSelections.GetChildren[Ansys.ACT.Automation.Mechanical.NamedSelection](True)
my_nsel = [i for i in NSall if i.Name.startswith("b")][0]
print(f"Named selection name: {my_nsel.Name}")

# %%
# Create a Named Selection of all bodies with a cylindrical face
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

geo = DataModel.GeoData
cyl_body_ids = []

for asm in geo.Assemblies:
    for part in asm.Parts:
        for body in part.Bodies:
            countcyl = 0
            print(f"countcyl {countcyl} for body {body}")
            for face in body.Faces:
                if (
                    face.SurfaceType
                    == Ansys.ACT.Interfaces.Geometry.GeoSurfaceTypeEnum.GeoSurfaceCylinder
                ):
                    countcyl += 1
            if countcyl != 0:
                cyl_body_ids.append(body.Id)

print(f"Bodies with cylindrical face IDs: {cyl_body_ids}")

selection_manager = ExtAPI.SelectionManager
selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
selection.Ids = cyl_body_ids

ns2 = Model.AddNamedSelection()
ns2.Name = "bodies_with_cyl_face"
ns2.Location = selection
selection_manager.ClearSelection()

print("Cleared selection")

# %%
# Modify material assignment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Assign a specific material to all bodies in the model
allbodies = Model.GetChildren(DataModelObjectCategory.Body, True)
for body in allbodies:
    body.Material = "Structural Steel"

# %%
# Get all Coordinate Systems
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Retrieve all coordinate systems in the model
tree_CS = Model.CoordinateSystems

# %%
# Add a cylindrical coordinate system
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create a new coordinate system
csys = Model.CoordinateSystems.AddCoordinateSystem()

print("Added coordinate system")

# place csys origin at arbitrary (0,25,50) location
csys.SetOriginLocation(Quantity(0, "in"), Quantity(25, "in"), Quantity(50, "in"))
# set primary X axis to arbitrary (1,2,3) direction
csys.PrimaryAxisDirection = Vector3D(1, 2, 3)
# %%
# Add a cartesian coordinate system at a location (0,25,50) inches
# with primary X axis towards an arbitrary (1,2,3) direction
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
csys = Model.CoordinateSystems.AddCoordinateSystem()
# place csys origin at arbitrary (0,25,50) location
csys.SetOriginLocation(Quantity(0, "in"), Quantity(25, "in"), Quantity(50, "in"))
# set primary X axis to arbitrary (1,2,3) direction
csys.PrimaryAxisDirection = Vector3D(1, 2, 3)

# %%
# Find a coordinate system by name
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Create a new coordinate system
csys = app.Model.CoordinateSystems.AddCoordinateSystem()

print("Added 2nd coordinate system")

# place csys origin at arbitrary (0,25,50) location
csys.SetOriginLocation(Quantity(0, "in"), Quantity(25, "in"), Quantity(50, "in"))
# set primary X axis to arbitrary (1,2,3) direction
csys.PrimaryAxisDirection = Vector3D(1, 2, 3)

# Save the Mechanical database file
from pathlib import Path

output_path = Path.cwd() / "out"
test_mechdat_path = str(output_path / "test.mechdat")
print("Set mechdat path")

app.save_as(test_mechdat_path, overwrite=True)
print("Saved mechdat")
# sphinx_gallery_start_ignore
# Close the application and delete downloaded files
app.close()
print("Closed app")
delete_downloads()
print("Deleted downloads")
# sphinx_gallery_end_ignore
