""".. _ref_setup:

App
---

This section has helper scripts for  Embedded App
"""
# %%
# Create an embedded instance and open an existing Mechanical File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

mechdat_path = download_file("cantilever.mechdat", "pymechanical", "embedding")
app = App(db_file = mechdat_path, globals=globals())
print(app)


# %%
# Import a Geometry File
# ~~~~~~~~~~~~~~~~~~~~~~

# sphinx_gallery_start_ignore
app.new()
# sphinx_gallery_end_ignore

geom_file_path = download_file("example_06_bolt_pret_geom.agdb", "pymechanical", "00_basic")
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = (Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic)
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessLines = True
geometry_import_preferences.NamedSelectionKey = ""
geometry_import_preferences.ProcessNamedSelections = True
geometry_import_preferences.ProcessMaterialProperties = True
geometry_import.Import(geom_file_path, geometry_import_format, geometry_import_preferences)


# %%
# Plot and Print the Tree (To check model so far)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Plot
app.plot()

# Print the tree
app.print_tree()


# %%
# Save the model
# ~~~~~~~~~~~~~~~
from pathlib import Path

output_path = Path.cwd() / "out"
test_mechdat_path = str(output_path / "test.mechdat")
app.save_as(test_mechdat_path, overwrite=True)


# sphinx_gallery_start_ignore
# Close the app
app.close()
# Delete the downloaded files
delete_downloads()
# sphinx_gallery_end_ignore