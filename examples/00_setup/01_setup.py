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

""".. _ref_setup_1:

App
---

This section has helper scripts to start an embedded instance of Mechanical
Application and import/open a file.

This is a prerequisite step for the other helper scripts in the following pages.

"""

# %%
# Create an embedded instance and open an existing Mechanical file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ansys.mechanical.core import App
from ansys.mechanical.core.examples import delete_downloads, download_file

mechdat_path = download_file("cantilever.mechdat", "pymechanical", "embedding")

# The following line creates an instance of the app, extracts the global API entry points,
# and merges them into your Python global variables.

app = App(db_file=mechdat_path, globals=globals())
print(app)

# Alternatively, you can use the update_globals method of the App class to
# update the global variables.The second argument, if set to False updates
# globals without enums like "SelectionTypeEnum" or "LoadDefineBy"
# app = App()
# app.update_globals(globals(), False)

# For a specific version , use ;
# app = App(version=241)

# %%
# Import a geometry file
# ~~~~~~~~~~~~~~~~~~~~~~

# sphinx_gallery_start_ignore
app.new()
# sphinx_gallery_end_ignore

geom_file_path = download_file("example_06_bolt_pret_geom.agdb", "pymechanical", "00_basic")
geometry_import = Model.GeometryImportGroup.AddGeometryImport()
geometry_import_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic
geometry_import_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()
geometry_import_preferences.ProcessLines = True
geometry_import_preferences.NamedSelectionKey = ""
geometry_import_preferences.ProcessNamedSelections = True
geometry_import_preferences.ProcessMaterialProperties = True
geometry_import.Import(geom_file_path, geometry_import_format, geometry_import_preferences)
# %%
# Set units
# ~~~~~~~~~

ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMM
ExtAPI.Application.ActiveAngleUnit = AngleUnitType.Radian
ExtAPI.Application.ActiveAngularVelocityUnit = AngularVelocityUnitType.RadianPerSecond
# %%
# View messages in Mechanical using PyMechanical
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app.messages.show()
# %%
# Plot and print the tree to check the model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Plot
app.plot()

# Print the tree
app.print_tree()

# %%
# Save the model
# ~~~~~~~~~~~~~~

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
