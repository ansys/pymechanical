# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

# /// script
# dependencies = [
#   "ansys-mechanical-core",
#   "marimo>=0.13.0",
# ]
# ///

"""Basic valve analysis - PyMechanical marimo notebook.

This marimo notebook demonstrates a structural analysis of a valve using
PyMechanical's embedded application mode.

Usage
-----
Open in the interactive marimo editor::

    marimo edit valve.py

Run as a read-only interactive web app::

    marimo run valve.py

Execute as a plain Python script (no interactive UI)::

    python valve.py

Notes
-----
This notebook requires a local Ansys Mechanical installation.
It cannot run in a browser-only (WebAssembly) environment because
it depends on the embedded Mechanical application.

Marimo cell ordering
--------------------
Marimo schedules cells based on data-flow dependencies rather than
top-to-bottom order.  ``App(globals=globals())`` injects the Mechanical
scripting globals (``Model``, ``ExtAPI``, ``Ansys``, ``Quantity``,
``Graphics``, ``Tree``, …) into the module namespace — in Python,
``globals()`` always returns the *module*-level ``__dict__``, even when
called inside a cell function.  Sequential simulation steps are chained
using boolean sentinel variables (``geometry_imported``,
``material_assigned``, …).  Each step's cell signature declares the
previous sentinel so marimo enforces the correct execution order.
"""

import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium", app_title="PyMechanical Valve Analysis")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Basic valve analysis

        This notebook demonstrates a **static structural analysis of a valve**
        using PyMechanical's embedded application mode.

        **Workflow**

        1. Import valve geometry (`.pmdb`)
        2. Assign Structural Steel material
        3. Generate mesh (25 mm element size)
        4. Apply fixed support, frictionless support, and adjustable internal pressure
        5. Solve and post-process total deformation

        > **Requirement:** A local Ansys Mechanical installation is required.
        > Set the `ANSYS_VERSION` environment variable or use the
        > `--version` flag with `ansys-mechanical` if needed.
        """
    )
    return


@app.cell
def _():
    from pathlib import Path

    import marimo as mo

    return Path, mo


@app.cell
def _():
    from ansys.mechanical.core import App
    from ansys.mechanical.core.examples import delete_downloads, download_file

    return App, delete_downloads, download_file


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Application setup")
    return


@app.cell
def _(App, mo):
    mech = App(globals=globals())
    mo.md(f"**Mechanical App initialized:** `{mech}`")
    return (mech,)


@app.cell
def _(Path, mech):
    output_path = Path.cwd() / "out"
    output_path.mkdir(exist_ok=True)
    camera = Graphics.Camera
    return camera, output_path


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Step 1 – Geometry import")
    return


@app.cell
def _(download_file, mech):
    geometry_path = download_file("Valve.pmdb", "pymechanical", "embedding")
    mech.helpers.import_geometry(geometry_path, process_named_selections=True)
    geometry_imported = True
    return geometry_imported, geometry_path


@app.cell
def _(camera, mech, mo, output_path, geometry_imported):
    _image_path = output_path / "geometry.png"
    camera.SetFit()
    mech.helpers.export_image(Model.Geometry, _image_path)
    mo.vstack([mo.md("**Imported geometry**"), mo.image(str(_image_path))])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Step 2 – Material assignment")
    return


@app.cell
def _(geometry_imported):
    material_assignment = Model.Materials.AddMaterialAssignment()
    material_assignment.Material = "Structural Steel"

    _sel = ExtAPI.SelectionManager.CreateSelectionInfo(
        Ansys.ACT.Interfaces.Common.SelectionTypeEnum.GeometryEntities
    )
    _sel.Ids = [
        body.GetGeoBody().Id
        for body in Model.Geometry.GetChildren(
            Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Body, True
        )
    ]
    material_assignment.Location = _sel
    material_assigned = True
    return material_assigned, material_assignment


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Step 3 – Meshing")
    return


@app.cell
def _(camera, mech, mo, output_path, material_assigned):
    mesh = Model.Mesh
    mesh.ElementSize = Quantity("25 [mm]")
    mesh.GenerateMesh()

    _image_path = output_path / "mesh.png"
    camera.SetFit()
    mech.helpers.export_image(mesh, _image_path)
    mo.vstack([mo.md("**Mesh — 25 mm element size**"), mo.image(str(_image_path))])
    mesh_generated = True
    return mesh, mesh_generated


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Step 4 – Boundary conditions")
    return


@app.cell
def _(mesh_generated):
    analysis = Model.AddStaticStructuralAnalysis()

    _fixed = analysis.AddFixedSupport()
    _fixed.Location = ExtAPI.DataModel.GetObjectsByName("NSFixedSupportFaces")[0]

    _frictionless = analysis.AddFrictionlessSupport()
    _frictionless.Location = ExtAPI.DataModel.GetObjectsByName("NSFrictionlessSupportFaces")[0]

    pressure = analysis.AddPressure()
    pressure.Location = ExtAPI.DataModel.GetObjectsByName("NSInsideFaces")[0]
    # Time points are fixed; peak magnitude is set reactively by the pressure input cell.
    pressure.Magnitude.Inputs[0].DiscreteValues = [Quantity("0 [s]"), Quantity("1 [s]")]

    return analysis


@app.cell
def _(analysis, camera, mech, mo, output_path):
    _image_path = output_path / "boundary_conditions.png"
    camera.SetFit()
    mech.helpers.export_image(analysis, _image_path)

    peak_pressure = mo.ui.slider(
        start=1,
        stop=100,
        step=0.5,
        value=15,
        label="Peak pressure (MPa)",
        show_value=True,
    )

    mo.hstack(
        [
            mo.image(str(_image_path), width=320),
            mo.vstack(
                [
                    mo.md("### Pressure input"),
                    mo.md(
                        "Adjust the slider and only the **pressure update → "
                        "solve → result** cells re-run automatically."
                    ),
                    peak_pressure,
                ]
            ),
        ],
        align="start",
    )
    return (peak_pressure,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("### Pressure application")
    return


@app.cell
def _(analysis, peak_pressure):
    _pressure = analysis.GetChildren(
        Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Pressure, True
    )[0]
    _pressure.Magnitude.Output.DiscreteValues = [
        Quantity("0 [Pa]"),
        Quantity(f"{peak_pressure.value} [MPa]"),
    ]
    # Return the live value so downstream cells see a real change when the
    # slider moves and are scheduled for re-execution by marimo.
    pressure_applied = peak_pressure.value
    return (pressure_applied,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Step 5 – Results setup & solve")
    return


@app.cell
def _(analysis):
    solution = analysis.Solution
    deformation = solution.AddTotalDeformation()
    return deformation, solution


@app.cell
def _(mo, pressure_applied, solution):
    mo.md("**Solving…** This may take a few minutes.")
    solution.Solve(True)
    # Propagate the pressure value so the deformation display and save cells
    # also see a changed dependency and re-run after each solve.
    solved = pressure_applied
    return (solved,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Step 6 – Post-processing")
    return


@app.cell
def _(camera, deformation, mech, mo, output_path, solved):
    Tree.Activate([deformation])
    _image_path = output_path / "total_deformation_valve.png"
    camera.SetFit()
    mech.helpers.export_image(deformation, _image_path)
    mo.vstack([mo.md("**Total deformation**"), mo.image(str(_image_path))])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Step 7 – Save and clean up")
    return


@app.cell
def _(Path, analysis, mech, mo, output_path, solved):
    mech.messages.show()
    mech.print_tree()

    _solve_out = Path(analysis.WorkingDir) / "solve.out"
    _log_text = _solve_out.read_text() if _solve_out.exists() else "(no solve.out found)"

    mechdat_file = output_path / "valve.mechdat"
    mech.save_as(str(mechdat_file), overwrite=True, remove_lock=True)

    mo.md(
        f"**Project saved to:** `{mechdat_file}`\n\n"
        f"<details><summary>Solver output</summary>\n\n"
        f"```\n{_log_text[:3000]}\n```\n\n</details>"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Step 8 – Clean up")
    return


@app.cell
def _(mo):
    close_btn = mo.ui.button(label="Close Mechanical & delete downloads", kind="danger")
    mo.vstack(
        [
            mo.md(
                "> **When finished:** click the button below to release the "
                "Mechanical process and remove cached example files."
            ),
            close_btn,
        ]
    )
    return (close_btn,)


@app.cell
def _(close_btn, delete_downloads, mech, mo):
    if not close_btn.value:
        mo.stop(True)
    mech.close()
    delete_downloads()
    mo.md("**Mechanical closed and example files deleted.**")
    return


if __name__ == "__main__":
    app.run()
