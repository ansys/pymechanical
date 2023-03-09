"""Quick Mechanical embedding tests."""
import os
import pathlib

import pytest

try:
    from ansys.mechanical.core import global_variables
except:
    # No embedding - this import breaks test collection
    global_variables = {}

ROOT_FOLDER = pathlib.Path(__file__).parent


def get_assets_folder():
    """Return the test assets folder.

    TODO - share this with the mechanical remote tests.
    """
    return ROOT_FOLDER / "assets"


@pytest.mark.embedding
def test_cause_failure():
    assert 3 == 4


@pytest.mark.embedding
def test_qk_eng_wb2_005(printer, selection, embedded_app):
    """Buckling analysis.

    From Mechanical/QK_ENG_WB2/QK_ENG_WB2_005
    """
    globals().update(global_variables(embedded_app))
    printer("Setting up test - adding linked static structural + buckling analysis system")
    Model.AddStaticStructuralAnalysis()
    Model.AddEigenvalueBucklingAnalysis()
    Model.Analyses[1].InitialConditions[0].PreStressICEnvironment = Model.Analyses[0]
    geometry_file = os.path.join(get_assets_folder(), "Eng157.x_t")
    printer(f"Setting up test - attaching geometry {geometry_file}")
    geometry_import = Model.GeometryImportGroup.AddGeometryImport()
    geometry_import.Import(geometry_file)
    printer("Running test")

    def _innertest():
        printer("Setup units")
        ExtAPI.Application.ActiveUnitSystem = (
            Ansys.ACT.Interfaces.Common.MechanicalUnitSystem.StandardBIN
        )
        MODEL = Model
        MODEL.Geometry.ElementControl = Ansys.Mechanical.DataModel.Enums.ElementControl.Manual
        STAT_STRUC = MODEL.Analyses[0]
        printer("Apply loads")
        selection.UpdateSelection(
            ExtAPI, [26], Ansys.ACT.Interfaces.Common.SelectionTypeEnum.GeometryEntities
        )
        FIX_SUP = STAT_STRUC.AddFixedSupport()
        selection.UpdateSelection(
            ExtAPI, [25], Ansys.ACT.Interfaces.Common.SelectionTypeEnum.GeometryEntities
        )
        FRC = STAT_STRUC.AddForce()
        FRC.DefineBy = Ansys.Mechanical.DataModel.Enums.LoadDefineBy.Components
        FRC.ZComponent.Output.SetDiscreteValue(0, Quantity("-1 [lbf]"))
        ExtAPI.SelectionManager.ClearSelection()
        printer("Insert Static Structural results and Solve")
        DIR_DEF01_STAT_STRUC = STAT_STRUC.Solution.AddDirectionalDeformation()
        STAT_STRUC.Solution.Solve(True)
        assert (
            STAT_STRUC.Solution.ObjectState == Ansys.Mechanical.DataModel.Enums.ObjectState.Solved
        )

        printer("Setup Linear Buckling analysis")
        BUCK = MODEL.Analyses[1]
        BUCK.AnalysisSettings.MaximumModesToFind = 6
        BUCK.AnalysisSettings.Stress = True
        BUCK.AnalysisSettings.Strain = True
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
        assert BUCK.Solution.ObjectState == Ansys.Mechanical.DataModel.Enums.ObjectState.Solved

        printer("Clean and Solve")
        embedded_app.execute_script("ExtAPI.DataModel.Project.Model.ClearGeneratedData()")
        assert BUCK.Solution.ObjectState != Ansys.Mechanical.DataModel.Enums.ObjectState.Solved
        # embedded_app.DataModel.Project.ClearGeneratedData()
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
def test_qk_eng_wb2_007(printer, selection, embedded_app):
    """Fatigue.

    From Mechanical/QK_ENG_WB2/QK_ENG_WB2_007
    """
    globals().update(global_variables(embedded_app))
    printer("Setting up test - adding two static structural systems")
    Model.AddStaticStructuralAnalysis()
    Model.AddStaticStructuralAnalysis()
    geometry_file = os.path.join(get_assets_folder(), "longbar.sat")
    printer(f"Setting up test - attaching geometry {geometry_file}")
    geometry_import = Model.GeometryImportGroup.AddGeometryImport()
    geometry_import.Import(geometry_file)
    material_file = os.path.join(get_assets_folder(), "eng200_material.xml")
    printer(f"Setting up test - import materials {material_file}")
    embedded_app.import_materials(material_file)

    def _innertest():
        printer("Add material file")
        MODEL = Model
        MODEL.RefreshMaterials()
        MODEL.Geometry.Children[0].Assignment = "eng200_material"

        printer("Setup Mesh")
        MSH = MODEL.Mesh
        MSH.Resolution = 4

        printer("Apply loads")
        STAT_STRUC1 = MODEL.Analyses[0]

        selection.UpdateSelection(
            ExtAPI, [29], Ansys.ACT.Interfaces.Common.SelectionTypeEnum.GeometryEntities
        )
        FIX_SUP = STAT_STRUC1.AddFixedSupport()

        ExtAPI.SelectionManager.ClearSelection()
        selection.UpdateSelection(
            ExtAPI, [28], Ansys.ACT.Interfaces.Common.SelectionTypeEnum.GeometryEntities
        )
        FRC = STAT_STRUC1.AddForce()
        FRC.DefineBy = Ansys.Mechanical.DataModel.Enums.LoadDefineBy.Components
        values = System.Collections.Generic.List[Quantity]()
        values.Add(Quantity("0 [N]"))
        values.Add(Quantity("1000000000 [N]"))
        FRC.YComponent.Output.DiscreteValues = values

        printer("Add Results and Solve")
        SOLN_STAT_STRUC1 = STAT_STRUC1.Solution
        SHEAR_STRS1_STAT_STRUC1 = SOLN_STAT_STRUC1.AddShearStress()
        SHEAR_STRS1_STAT_STRUC1.ShearOrientation = (
            Ansys.Mechanical.DataModel.Enums.ShearOrientationType.YZPlane
        )
        SHEAR_STRS2_STAT_STRUC1 = SOLN_STAT_STRUC1.AddShearStress()
        SHEAR_STRS2_STAT_STRUC1.ShearOrientation = (
            Ansys.Mechanical.DataModel.Enums.ShearOrientationType.XZPlane
        )
        SOLN_STAT_STRUC1.Solve(True)

        printer("Apply loads for Static 2 ")
        STAT_STRUC2 = MODEL.Analyses[1]

        ExtAPI.SelectionManager.ClearSelection()
        selection.UpdateSelection(
            ExtAPI, [29], Ansys.ACT.Interfaces.Common.SelectionTypeEnum.GeometryEntities
        )
        FIX_SUP2 = STAT_STRUC2.AddFixedSupport()

        ExtAPI.SelectionManager.ClearSelection()
        selection.UpdateSelection(
            ExtAPI, [28], Ansys.ACT.Interfaces.Common.SelectionTypeEnum.GeometryEntities
        )
        FRC2 = STAT_STRUC2.AddForce()
        FRC2.DefineBy = Ansys.Mechanical.DataModel.Enums.LoadDefineBy.Components
        values = System.Collections.Generic.List[Quantity]()
        values.Add(Quantity("0 [N]"))
        values.Add(Quantity("1000000000 [N]"))
        FRC2.XComponent.Output.DiscreteValues = values

        printer("Add Results and Solve")
        SOLN_STAT_STRUC2 = STAT_STRUC2.Solution

        SHEAR_STRS1_STAT_STRUC2 = SOLN_STAT_STRUC2.AddShearStress()  # YZ stress
        SHEAR_STRS1_STAT_STRUC2.ShearOrientation = (
            Ansys.Mechanical.DataModel.Enums.ShearOrientationType.YZPlane
        )

        SHEAR_STRS2_STAT_STRUC2 = SOLN_STAT_STRUC2.AddShearStress()  # XZ stress
        SHEAR_STRS2_STAT_STRUC1.ShearOrientation = (
            Ansys.Mechanical.DataModel.Enums.ShearOrientationType.XZPlane
        )

        SOLN_STAT_STRUC2.Solve(True)

        ExtAPI.SelectionManager.ClearSelection()
        printer("Insert Solution Combination 1")
        SOLN_COMB = MODEL.AddSolutionCombination()
        SOLN_COMB.Activate()

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
        FAT_TOOL1.LoadingType = Ansys.Mechanical.DataModel.Enums.FatigueLoadType.NonProportional
        FAT_TOOL1.MeanStressTheory = Ansys.Mechanical.DataModel.Enums.MeanStressTheoryType.Goodman
        FAT_TOOL1.StressComponent = (
            Ansys.Mechanical.DataModel.Enums.FatigueStressComponentType.FatigueToolComponent_YZ
        )
        FAT_TOOL1.ScaleFactor = 0.85
        LIFE = FAT_TOOL1.AddLife()
        DAMAGE = FAT_TOOL1.AddDamage()
        DAMAGE.DesignLife = 1000000
        safetyFactor = FAT_TOOL1.AddSafetyFactor()
        safetyFactor.DesignLife = 1000000

        printer("Add and Setup Fatigue Tool 2")
        FAT_TOOL2 = FAT_TOOL1.Duplicate()
        FAT_TOOL2.StressComponent = (
            Ansys.Mechanical.DataModel.Enums.FatigueStressComponentType.FatigueToolComponent_XZ
        )

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
