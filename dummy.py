"""Open the saved dummy project in a fresh process and print its node count."""

from pathlib import Path

import ansys.mechanical.core as mech

if __name__ == "__main__":
    project_path = Path(__file__).resolve().parent / "dummy.mechdb"
    if not project_path.is_file():
        raise FileNotFoundError(project_path)

    app = mech.App(version=251)
    try:
        app.open(str(project_path))
        mesh_data = app.DataModel.MeshDataByName(app.DataModel.MeshDataNames[0])
        print(f"{project_path.name} node count: {mesh_data.NodeCount}", flush=True)
    finally:
        app.close()
        app.exit()
        app._dispose()
