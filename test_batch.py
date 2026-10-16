# ruff: noqa: F821
"""Compare mesh node counts when reopening a project inside native Mechanical."""

from System.IO import Path

project_path = Path.GetFullPath("tests/assets/cube-hole.mechdb")
dummy_path = Path.GetFullPath("dummy.mechdb")

ExtAPI.DataModel.Project.Open(project_path)
mesh_data = ExtAPI.DataModel.MeshDataByName(ExtAPI.DataModel.MeshDataNames[0])
print("After first open: {0}".format(mesh_data.NodeCount))

ExtAPI.DataModel.Project.SaveAs(dummy_path, True)
mesh_data = ExtAPI.DataModel.MeshDataByName(ExtAPI.DataModel.MeshDataNames[0])
print("After SaveAs: {0}".format(mesh_data.NodeCount))

ExtAPI.DataModel.Project.Open(dummy_path)
mesh_data = ExtAPI.DataModel.MeshDataByName(ExtAPI.DataModel.MeshDataNames[0])
print("After second open: {0}".format(mesh_data.NodeCount))
