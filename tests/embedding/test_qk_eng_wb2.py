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

"""Migration from QK_ENG_WB2 tests."""

import os

import pytest


@pytest.mark.embedding
def test_qk_eng_wb2_005(printer, embedded_app, assets):
    """Buckling analysis.

    From STAND_MECH:BATCH/QK_ENG/QK_ENG_005
    """
    embedded_app.update_globals(globals())

    printer("Setting up test - adding linked static structural + buckling analysis system")
    STAT_STRUC = Model.AddStaticStructuralAnalysis()
    STAT_STRUC_SOLN = STAT_STRUC.Solution
    BUCK = Model.AddEigenvalueBucklingAnalysis()
    BUCK_ANA_SETTING = BUCK.AnalysisSettings
    PRE_STRS_ENV = BUCK.Children[0]
    PRE_STRS_ENV.PreStressICEnvironment = STAT_STRUC

    geometry_file = os.path.join(assets, "Eng157.x_t")
    printer(f"Setting up test - attaching geometry {geometry_file}")
    geometry_import = Model.GeometryImportGroup.AddGeometryImport()
    geometry_import.Import(geometry_file)
    printer("Running test")

    def _innertest():
        printer("Setup units")
        ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardBIN

        printer("Create Named Selections")
        FACE1 = Model.AddNamedSelection()
        FACE1.Name = "Face1"
        FACE1.ScopingMethod = GeometryDefineByType.Worksheet
        GEN_CRT = FACE1.GenerationCriteria
        CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
        CRT1.Active = True
        CRT1.Action = SelectionActionType.Add
        CRT1.EntityType = SelectionType.GeoFace
        CRT1.Criterion = SelectionCriterionType.LocationZ
        CRT1.Operator = SelectionOperatorType.Equal
        CRT1.Value = Quantity("0 [in]")
        GEN_CRT.Add(CRT1)
        FACE1.Activate()
        FACE1.Generate()

        FACE2 = Model.AddNamedSelection()
        FACE2.Name = "Face2"
        FACE2.ScopingMethod = GeometryDefineByType.Worksheet
        GEN_CRT = FACE2.GenerationCriteria
        CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
        CRT1.Active = True
        CRT1.Action = SelectionActionType.Add
        CRT1.EntityType = SelectionType.GeoFace
        CRT1.Criterion = SelectionCriterionType.LocationZ
        CRT1.Operator = SelectionOperatorType.Equal
        CRT1.Value = Quantity("100 [in]")
        GEN_CRT.Add(CRT1)
        FACE2.Activate()
        FACE2.Generate()

        printer("Apply loads")
        MODEL = Model
        MODEL.Geometry.ElementControl = ElementControl.Manual

        FIX_SUP = STAT_STRUC.AddFixedSupport()
        FIX_SUP.Location = FACE1

        FRC = STAT_STRUC.AddForce()
        FRC.Location = FACE2
        FRC.DefineBy = LoadDefineBy.Components
        FRC.ZComponent.Output.SetDiscreteValue(0, Quantity("-1 [lbf]"))

        printer("Insert Static Structural results and Solve")
        STAT_STRUC.Solution.AddDirectionalDeformation()
        STAT_STRUC_SOLN.Solve(True)

        printer("Setup Linear Buckling analysis")
        BUCK_ANA_SETTING.MaximumModesToFind = 6
        BUCK_ANA_SETTING.Stress = True
        BUCK_ANA_SETTING.Strain = True

        printer("Add Buckling Results")
        TOT_DEF01_BUCK = BUCK.Solution.AddTotalDeformation()
        TOT_DEF01_BUCK.Mode = 1
        TOT_DEF02_BUCK = BUCK.Solution.AddTotalDeformation()
        TOT_DEF02_BUCK.Mode = 2
        TOT_DEF03_BUCK = BUCK.Solution.AddTotalDeformation()
        TOT_DEF03_BUCK.Mode = 3
        TOT_DEF04_BUCK = BUCK.Solution.AddTotalDeformation()
        TOT_DEF04_BUCK.Mode = 4
        TOT_DEF05_BUCK = BUCK.Solution.AddTotalDeformation()
        TOT_DEF05_BUCK.Mode = 5
        TOT_DEF06_BUCK = BUCK.Solution.AddTotalDeformation()
        TOT_DEF06_BUCK.Mode = 6
        EQV_STRS_BUCK = BUCK.Solution.AddEquivalentStress()
        EQV_STRS_BUCK.Mode = 6

        BUCK.Solution.Solve(True)
        assert BUCK.Solution.ObjectState == ObjectState.Solved

        printer("Clean and Solve")
        embedded_app.DataModel.Project.ClearGeneratedData()
        assert BUCK.Solution.ObjectState != ObjectState.Solved

        MODEL.Solve(True)
        printer("Validate Results")
        TOT_DEF01_BUCK.Activate()
        d1_mode1 = TOT_DEF01_BUCK.TabularData["LoadMultiplier"].get_Item(0)
        assert d1_mode1 == pytest.approx(37.268, rel=0.05), "First Load Multiplier result"
        d1_mode3 = TOT_DEF01_BUCK.TabularData["LoadMultiplier"].get_Item(2)
        assert d1_mode3 == pytest.approx(335.412, rel=0.05), "Third Load Multiplier result"
        d1_mode5 = TOT_DEF01_BUCK.TabularData["LoadMultiplier"].get_Item(4)
        assert d1_mode5 == pytest.approx(931.701, rel=0.05), "Fifth Load Multiplier result"
        EQV_STRS_BUCK.Activate()
        s6_mode6 = EQV_STRS_BUCK.TabularData["LoadMultiplier"].get_Item(5)
        assert s6_mode6 == pytest.approx(43642, rel=1), "Sixth Load Multiplier result"

    _innertest()


@pytest.mark.embedding
def test_qk_eng_wb2_007(printer, embedded_app, assets):
    """Fatigue.

    From STAND_MECH:BATCH/QK_ENG/QK_ENG_007
    """
    embedded_app.update_globals(globals())
    printer(embedded_app)
    printer("Set units system to MKS")
    ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardMKS

    geometry_file = os.path.join(assets, "longbar_sat_m.x_t")
    printer(f"Setting up test - attaching geometry {geometry_file}")
    geometry_import = Model.GeometryImportGroup.AddGeometryImport()
    geometry_import.Import(geometry_file)

    printer("Setting up test - adding two static structural systems")
    Model.AddStaticStructuralAnalysis()
    Model.AddStaticStructuralAnalysis()

    material_file = os.path.join(assets, "eng200_material.xml")
    printer(f"Setting up test - import materials {material_file}")
    materials = Model.Materials
    materials.Import(material_file)

    def _innertest():
        printer("Add material file")
        MODEL = Model
        MODEL.RefreshMaterials()
        MODEL.Geometry.Children[0].Material = "eng200_material"

        GEOM = Model.Geometry
        MSH = Model.Mesh

        [
            i
            for i in GEOM.GetChildren[Ansys.ACT.Automation.Mechanical.Body](True)
            if i.Name == "Part 1"
        ][0]

        printer("Create named selection")
        NS1 = ExtAPI.DataModel.Project.Model.AddNamedSelection()
        NS1.Name = "Face1"
        NS1.ScopingMethod = GeometryDefineByType.Worksheet

        GEN_CRT = NS1.GenerationCriteria
        CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
        CRT1.Active = True
        CRT1.Action = SelectionActionType.Add
        CRT1.EntityType = SelectionType.GeoFace
        CRT1.Criterion = SelectionCriterionType.LocationZ
        CRT1.Operator = SelectionOperatorType.Equal
        CRT1.Value = Quantity("0 [m]")
        GEN_CRT.Add(CRT1)

        NS1.Activate()
        NS1.Generate()

        NS2 = ExtAPI.DataModel.Project.Model.AddNamedSelection()
        NS2.Name = "Face2"
        NS2.ScopingMethod = GeometryDefineByType.Worksheet

        GEN_CRT = NS2.GenerationCriteria
        CRT1 = Ansys.ACT.Automation.Mechanical.NamedSelectionCriterion()
        CRT1.Active = True
        CRT1.Action = SelectionActionType.Add
        CRT1.EntityType = SelectionType.GeoFace
        CRT1.Criterion = SelectionCriterionType.LocationZ
        CRT1.Operator = SelectionOperatorType.Equal
        CRT1.Value = Quantity("20 [m]")

        GEN_CRT.Add(CRT1)
        NS2.Activate()
        NS2.Generate()

        printer("Setup Mesh")
        MSH = MODEL.Mesh
        MSH.Resolution = 4

        printer("Apply loads")
        STAT_STRUC1 = MODEL.Analyses[0]
        FIX_SUP = STAT_STRUC1.AddFixedSupport()
        FIX_SUP.Location = NS1

        ExtAPI.SelectionManager.ClearSelection()
        FRC = STAT_STRUC1.AddForce()
        FRC.DefineBy = LoadDefineBy.Components
        FRC.YComponent.Output.DiscreteValues = [Quantity("0 [N]"), Quantity("1000000000 [N]")]
        FRC.Location = NS2

        printer("Add Results and Solve")
        SOLN_STAT_STRUC1 = STAT_STRUC1.Solution
        SHEAR_STRS1_STAT_STRUC1 = SOLN_STAT_STRUC1.AddShearStress()
        SHEAR_STRS1_STAT_STRUC1.ShearOrientation = ShearOrientationType.YZPlane
        SHEAR_STRS2_STAT_STRUC1 = SOLN_STAT_STRUC1.AddShearStress()
        SHEAR_STRS2_STAT_STRUC1.ShearOrientation = ShearOrientationType.XZPlane
        SOLN_STAT_STRUC1.Solve(True)

        printer("Apply loads for Static 2 ")
        STAT_STRUC2 = MODEL.Analyses[1]

        ExtAPI.SelectionManager.ClearSelection()
        FIX_SUP2 = STAT_STRUC2.AddFixedSupport()
        FIX_SUP2.Location = NS1

        ExtAPI.SelectionManager.ClearSelection()
        FRC2 = STAT_STRUC2.AddForce()
        FRC2.DefineBy = LoadDefineBy.Components
        FRC2.XComponent.Output.DiscreteValues = [Quantity("0 [N]"), Quantity("1000000000 [N]")]
        FRC2.Location = NS2

        printer("Add Results and Solve")
        SOLN_STAT_STRUC2 = STAT_STRUC2.Solution

        SHEAR_STRS1_STAT_STRUC2 = SOLN_STAT_STRUC2.AddShearStress()  # YZ stress
        SHEAR_STRS1_STAT_STRUC2.ShearOrientation = ShearOrientationType.YZPlane
        SOLN_STAT_STRUC2.AddShearStress()  # XZ stress
        SHEAR_STRS2_STAT_STRUC1.ShearOrientation = ShearOrientationType.XZPlane

        SOLN_STAT_STRUC2.Solve(True)

        ExtAPI.SelectionManager.ClearSelection()
        printer("Insert Solution Combination 1")
        SOLN_COMB = MODEL.AddSolutionCombination()

        printer("Insert Solution Combination2")
        SOLN_COMB.Definition.AddBaseCase()

        printer("Insert Solution Combination 3")
        SOLN_COMB.Definition.SetCoefficient(0, 0, 1)
        printer("Insert Solution Combination4")
        SOLN_COMB.Definition.SetBaseCaseAnalysis(0, STAT_STRUC1)
        printer("Insert Solution Combination5")
        SOLN_COMB.Definition.SetCoefficient(0, 1, 1)
        printer("Insert Solution Combination6")
        SOLN_COMB.Definition.SetBaseCaseAnalysis(1, STAT_STRUC2)

        printer("Add and Setup Fatigue Tool 1")
        FAT_TOOL1 = SOLN_COMB.AddFatigueTool()
        FAT_TOOL1.LoadingType = FatigueLoadType.NonProportional
        FAT_TOOL1.MeanStressTheory = MeanStressTheoryType.Goodman
        FAT_TOOL1.StressComponent = FatigueStressComponentType.FatigueToolComponent_YZ
        FAT_TOOL1.ScaleFactor = 0.85
        LIFE = FAT_TOOL1.AddLife()
        DAMAGE = FAT_TOOL1.AddDamage()
        DAMAGE.DesignLife = 1000000
        safetyFactor = FAT_TOOL1.AddSafetyFactor()
        safetyFactor.DesignLife = 1000000

        printer("Add and Setup Fatigue Tool 2")
        FAT_TOOL2 = FAT_TOOL1.Duplicate()
        FAT_TOOL2.StressComponent = FatigueStressComponentType.FatigueToolComponent_XZ

        printer("Solve and Validate Fatigue Tool results")
        MODEL.Solve(True)

        FAT_Tool_1_LIFE = LIFE.Minimum.Value
        assert FAT_Tool_1_LIFE == pytest.approx(
            1628.0823, rel=0.08
        ), "Minimum Life For Fatigue Tool 1"

        FAT_TOOL_1_DAMAGE = DAMAGE.Maximum.Value
        assert FAT_TOOL_1_DAMAGE == pytest.approx(
            614.2195, rel=0.08
        ), "Maximum Damage For Fatigue Tool 1"

        FAT_TOOL_1_Safety_Factor = safetyFactor.Minimum.Value
        assert FAT_TOOL_1_Safety_Factor == pytest.approx(
            0.0122, rel=0.08
        ), "Minimum Safety Factor For Fatigue Tool 1"

        FAT_TOOL_2_LIFE = FAT_TOOL2.Children[0].Minimum.Value
        assert FAT_TOOL_2_LIFE == pytest.approx(
            1628.0823, rel=0.08
        ), "Minimum Life For Fatigue Tool 2"

        FAT_TOOL_2_DAMAGE = FAT_TOOL2.Children[1].Maximum.Value
        assert FAT_TOOL_2_DAMAGE == pytest.approx(
            614.2195, rel=0.08
        ), "Maximum Damage For Fatigue Tool 2"

        FAT_TOOL_2_Safety_Factor = FAT_TOOL2.Children[2].Minimum.Value
        assert FAT_TOOL_2_Safety_Factor == pytest.approx(
            0.0122, rel=0.08
        ), "Minimum Safety Factor For Fatigue Tool 2"

    _innertest()
