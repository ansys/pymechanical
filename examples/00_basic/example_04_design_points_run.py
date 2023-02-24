""".. _ref_design_points_run:

Run a set of design points
-------------------------------

In this example, using the support files, resume an archived file and run a set of design points by
varying the bearing load.

# In this example, using the support files, resume an archived file and run a set of design points
by varying the bearing load

- bicycle_crank_231.mechpz
"""

###############################################################################
# Launch multiple sessions in batch
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Launch multiple sessions in batch

from ansys.mechanical.core import LocalMechanicalPool

pool = LocalMechanicalPool(2)

###################################################################################
# Execute the Mechanical script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Execute the Mechanical script to run the python file containing Mechanical scripting
# commands


def run_designs(mechanical, run_number, run_val):
    mechanical.clear()
    result = mechanical.run_python_script(
        """
import json
mechpz_path = r"C:\\temp\\pymechtest\\bicycle_crank_231.mechpz"
ExtAPI.DataModel.Project.Unarchive(mechpz_path)
ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardBIN
bearing_load = DataModel.GetObjectsByName("Bearing Load")[0]
bearing_load.ZComponent.Output.SetDiscreteValue(0, Quantity("""
        + run_val
        + """, "lbf"))
Model.Analyses[0].Solution.Solve(True)
stress = DataModel.GetObjectsByName("Equivalent Stress")[0]
stress_details = {"Eqv Stress (Min)": str(stress.Minimum),"Eqv Stress (Max)": str(stress.Maximum)}
json.dumps(stress_details)
"""
    )

    return run_number, result


inputs = [("DP1", "500"), ("DP2", "600")]
results = pool.map(run_designs, inputs, close_when_finished=True, progress_bar=True, wait=True)

print(results)

###########################################################
# Close the pool
# ~~~~~~~~~~~~~~~~
# Close the pool

pool.exit()
