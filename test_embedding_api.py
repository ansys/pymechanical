
from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file
from ansys.mechanical.core.api_embedding import Model
app = App()
app.update_globals(globals())
print(app)

model =Model(app)

geometry_path = download_file(
    "example_06_bolt_pret_geom.agdb", "pymechanical", "00_basic"
)

geometry = model.geometry_group.add_geometry()
geometry.import_geometry(geometry_path)