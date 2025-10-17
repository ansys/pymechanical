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

"""LSDyna analysis test."""

from pathlib import Path

import pytest


@pytest.mark.embedding
@pytest.mark.windows_only
def test_lsdyna(printer, embedded_app, assets):
    """
    Unit test for LSDyna.

    This test focuses on LSDyna analysis in Mechanical.
    Runs only in Windows environment. This test involves
    a simple geometry with high velocity
    hitting on rigid wall.

    Note - In order for standalone Mechanical to use LS-DYNA,
           the lsdyna license needs to be at the top of the list.
           Use the license preferences in Mechanical to set this up.
    """
    embedded_app.update_globals(globals())
    printer("Setting up test - LSDyna system")
    Model.AddLSDynaAnalysis()
    geometry_file = str(Path(assets) / "Eng157.x_t")
    printer(f"Setting up test - attaching geometry {geometry_file}")
    geometry_import = Model.GeometryImportGroup.AddGeometryImport()
    geometry_import.Import(geometry_file)
    printer("Running test")

    def _innertest():
        analysis = Model.Analyses[0]
        printer("Setup units")
        ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMMton
        ExtAPI.Application.ActiveAngleUnit = AngleUnitType.Radian
        printer("Add Coordinate system")
        cs = Model.CoordinateSystems
        lcs = cs.AddCoordinateSystem()
        lcs.Origin = [0.0, 0.0, -20.0]
        lcs.PrimaryAxis = CoordinateSystemAxisType.PositiveXAxis
        lcs.PrimaryAxisDefineBy = CoordinateSystemAlignmentType.GlobalY
        lcs.OriginDefineBy = CoordinateSystemAlignmentType.Fixed
        printer("Setting solver controls")
        solver = analysis.Solver
        solver.Properties["Step Controls/Endtime"].Value = 3.0e-5
        analysis.Activate()
        printer("Add Rigid Wall")
        rigid_wall = analysis.CreateLoadObject("Rigid Wall", "LSDYNA")
        rigid_wall.Properties["Coordinate System"].Value = lcs.ObjectId
        ExtAPI.DataModel.Tree.Refresh()
        printer("Adding initial velocity")
        ic = ExtAPI.DataModel.GetObjectsByName("Initial Conditions")[0]
        vel = ic.InsertVelocity()
        selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
        selection.Ids = [ExtAPI.DataModel.GeoData.Assemblies[0].Parts[0].Bodies[0].Id]
        vel.Location = selection
        vel.DefineBy = LoadDefineBy.Components
        vel.ZComponent = Quantity(
            -2800000, ExtAPI.DataModel.CurrentUnitFromQuantityName("Velocity")
        )
        printer("Meshing")
        mesh = Model.Mesh
        mesh.ElementOrder = ElementOrder.Linear  # LSDyna supports only Linear
        mesh.ElementSize = Quantity(200, "mm")

        analysis_solution = analysis.Solution
        assert analysis_solution.ObjectState != ObjectState.Solved

        printer("Solve")
        analysis.Solution.Solve()
        assert analysis_solution.ObjectState == ObjectState.Solved, "Solved"

        printer("Add User defined result - EPS")
        eps = analysis.Solution.AddUserDefinedResult()
        eps.Expression = "EPS"
        eps.EvaluateAllResults()
        eps_max = eps.Maximum.Value
        eps_min = eps.Minimum.Value

        printer("Validate Results")
        assert eps_max == pytest.approx(0.2046, abs=0.002)
        assert eps_min == pytest.approx(-0.0101, abs=0.002)

    _innertest()
