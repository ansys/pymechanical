""".. _ref_design_points_run:

Run a set of design points
-------------------------------

In this example, using the support files, resume an archived file and run a set of design points by
varying the bearing load.

"""

###############################################################################
# Example Setup
# -------------
# When you run this workflow, the required file will be downloaded.
#
# Perform required download.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Download the mechanical archive project.

from ansys.mechanical.core import LocalMechanicalPool
from ansys.mechanical.core.examples import download_file

mechpz_path = download_file("example_04_bicycle_crank_231.mechpz", "pymechanical", "00_basic")
print(f"Downloaded the archive project file at : {mechpz_path}")

###############################################################################
# Launch multiple Mechanical sessions in batch.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Launch a pools of two Mechanical instances in batch.

pool = LocalMechanicalPool(2)

###################################################################################
# Create the user-defined function to run on each Mechanical instance in the pool
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This function will be called with the available mechanical instance from the pool.
# Run the script and get the results.


def run_designs(mechanical, run_number, run_val):
    # clear since mechanical session is reused
    mechanical.clear()

    # Make this variable compatible on both windows and linux.
    mechpz_path_modified = mechpz_path.replace("\\", "\\\\")
    mechanical.run_python_script(f"mechpz_path='{mechpz_path_modified}'")

    result = mechanical.run_python_script(
        """
import json

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


###########################################################
# Setup the inputs for this workflow
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Setup the list of tuples for the workflow.

inputs = [("DP1", "500"), ("DP2", "600")]

###########################################################
# Start the workflow
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Pool will trigger run_designs call with available Mechanical
# instance and the input.

results = pool.map(run_designs, inputs, close_when_finished=True, progress_bar=True, wait=True)
print(f"Results after running the workflow:\n{results}")

###########################################################
# Close the pool
# ~~~~~~~~~~~~~~~~
# Close the pool.

pool.exit()
