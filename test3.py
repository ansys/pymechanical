"""Reproduce mesh-data access after closing and reopening a Mechanical project."""

from pathlib import Path

import ansys.mechanical.core as mech

if __name__ == "__main__":
    project_path = Path(__file__).resolve().parent / "tests" / "assets" / "cube-hole.mechdb"
    dummy_path = Path(__file__).resolve().parent / "dummy.mechdb"
    app = mech.App(version=251)
    try:
        globals().update(mech.global_variables(app, True))
        app.open(str(project_path))
        mesh_data = app.DataModel.MeshDataByName(app.DataModel.MeshDataNames[0])
        original_node_count = mesh_data.NodeCount
        print(f"{project_path.name} node count: {original_node_count}", flush=True)
        app.save_as(str(dummy_path), overwrite=True)

        app.open(str(dummy_path))

        mesh_data = app.DataModel.MeshDataByName(app.DataModel.MeshDataNames[0])
        print(f"{dummy_path.name} node count: {mesh_data.NodeCount}", flush=True)
    finally:
        app.close()
        app.exit()
        app._dispose()
