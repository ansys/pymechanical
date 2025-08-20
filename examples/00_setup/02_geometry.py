""".. _ref_geometry:

Geometry
--------

This section has helper scripts for Geometry
"""
# %%
# Create an embedded instance and open an existing Mechanical File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

mechdat_path = download_file("cantilever.mechdat", "pymechanical", "embedding")
app = App(db_file=mechdat_path, globals=globals())
print(app)


# %%
# Get all bodies
# ~~~~~~~~~~~~~~~~~
body_objects = Model.Geometry.GetChildren(DataModelObjectCategory.Body, True)
# or
# bodies_objects = Model.Geometry.GetChildren(Ansys.ACT.Automation.Mechanical.Body, True)

bodies = [body.GetGeoBody() for body in body_objects]  # GeoBodyWrapper
# or
# import itertools
# nested_list = [x.Bodies for x in ExtAPI.DataModel.GeoData.Assemblies[0].AllParts]
# bodies = list(itertools.chain(*nested_list))

bo = body_objects[0]  # Access Object Details and RMB options
b = bodies[0]  # Access Geometric Properties: 'Area', 'GeoData', 'Centroid', 'Faces', etc.

# %%
# Find Body with Largest Volume
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMM

body_names_volumes = []
for body in body_objects:
    if body.Suppressed == 0 and body.Volume:
        body_names_volumes.append((body.Name, body.Volume, body.GetGeoBody().Id))

sorted_name_vol = sorted(body_names_volumes)
bodyname, volu, bodyid = sorted_name_vol.pop()
print(f"Unit System is: {ExtAPI.Application.ActiveUnitSystem}")
print(f"Name of the Largest Body: '{bodyname}'")
print(f"Its Volume: {round(volu.Value, 2)} {volu.Unit}")
print(f"Its id: {bodyid}")

# %%
# Find Body by its ID
# ~~~~~~~~~~~~~~~~~~~~~~
b2 = ExtAPI.DataModel.GeoData.GeoEntityById(bodyid)
print(f"Body Name: {b2.Name}, Body Id: {b2.Id}")

# %%
# Find the Part that the body belongs to
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
body_name = ExtAPI.DataModel.GeoData.GeoEntityById(363).Name
part_name = ExtAPI.DataModel.GeoData.GeoEntityById(363).Part.Name
print(f"The Body named '{body_name}' belongs to the part named '{part_name}'")

# %%
# Find Body by its ID AND print its Faces, Centroid, etc.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
body2 = ExtAPI.DataModel.GeoData.GeoEntityById(bodyid)

face_ids = [face.Id for face in body2.Faces]
centroids_of_each_face = [
    ExtAPI.DataModel.GeoData.GeoEntityById(face_id).Centroid for face_id in face_ids
]
for face_id, centroid in zip(face_ids, centroids_of_each_face):
    print(face_id, list(centroid))

# %%
# Get all Vertices
# ~~~~~~~~~~~~~~~~~~~
vertices = []
geo = ExtAPI.DataModel.GeoData
for asm in geo.Assemblies:
    for part in asm.Parts:
        for body in part.Bodies:
            for i in range(0, body.Vertices.Count):
                vertices.append(body.Vertices[i].Id)

print(vertices)

# %%
# Get all edges of a given length
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMM
use_length = 75

geo = ExtAPI.DataModel.GeoData
edgelist = []

for asm in geo.Assemblies:
    for part in asm.Parts:
        for body in part.Bodies:
            for edge in body.Edges:
                if abs(edge.Length - use_length) <= use_length * 0.01:
                    edgelist.append(edge.Id)
print(edgelist)

# %%
# Get all circular edges of a given radius
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import math

radius = 10
circumference = 2 * math.pi * radius

geo = ExtAPI.DataModel.GeoData
circlelist = []

for asm in geo.Assemblies:
    for part in asm.Parts:
        for body in part.Bodies:
            for edge in body.Edges:
                if (
                    abs(edge.Length - circumference) <= circumference * 0.01
                    and str(edge.CurveType) == "GeoCurveCircle"
                ):
                    circlelist.append(edge.Id)
print(circlelist)

# %%
# Get Radius of a selected edge
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
my_edge = ExtAPI.DataModel.GeoData.GeoEntityById(185)
my_edge_radius = my_edge.Radius if str(my_edge.CurveType) == "GeoCurveCircle" else 0.0
print(my_edge_radius)

# %%
# Create a Named Selection from a list of body Ids
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
mylist = [bodyid]

selection_manager = ExtAPI.SelectionManager
selection = ExtAPI.SelectionManager.CreateSelectionInfo(
    SelectionTypeEnum.GeometryEntities
)
selection.Ids = mylist
selection_manager.NewSelection(selection)

ns2 = ExtAPI.DataModel.Project.Model.AddNamedSelection()
ns2.Name = "bodies2"
ns2.Location = selection

# %%
# Find a Named Selection with a prefix
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
NSall = ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren[
    Ansys.ACT.Automation.Mechanical.NamedSelection
](True)
my_nsel = [i for i in NSall if i.Name.startswith("b")][0]
print(my_nsel.Name)

# %%
# Create a Named Selection of all bodies with a cylindrical face
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
geo = ExtAPI.DataModel.GeoData
cyl_body_ids = []

for asm in geo.Assemblies:
    for part in asm.Parts:
        for body in part.Bodies:
            countcyl = 0
            for face in body.Faces:
                if (
                    face.SurfaceType
                    == Ansys.ACT.Interfaces.Geometry.GeoSurfaceTypeEnum.GeoSurfaceCylinder
                ):
                    countcyl = countcyl + 1
            if countcyl != 0:
                cyl_body_ids.append(body.Id)

selection_manager = ExtAPI.SelectionManager
selection = ExtAPI.SelectionManager.CreateSelectionInfo(
    SelectionTypeEnum.GeometryEntities
)
selection.Ids = cyl_body_ids

model = ExtAPI.DataModel.Project.Model
ns2 = model.AddNamedSelection()
ns2.Name = "bodies_with_cyl_face"
ns2.Location = selection
selection_manager.ClearSelection()

# %%
# Modify material assignment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
allbodies = ExtAPI.DataModel.Project.Model.GetChildren(
    DataModelObjectCategory.Body, True
)
for body in allbodies:
    body.Material = "Structural Steel"

# %%
# Get all Coordinate Systems
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
tree_CS = ExtAPI.DataModel.Project.Model.CoordinateSystems