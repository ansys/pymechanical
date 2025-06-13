"""Test script to import geometry into a Mechanical model."""

from ansys.mechanical.core import launch_mechanical
from ansys.mechanical.core.api.model import Model

app = launch_mechanical(batch=False, cleanup_on_exit=False)
model = Model(app)
geo_group = model.add_geometry_group("geo_group")
geo_group.import_geometry(r"D:\PyAnsys\Repos\pymechanical\Eng157.x_t")
