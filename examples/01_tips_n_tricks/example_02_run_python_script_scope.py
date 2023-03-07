""".. _ref_example_02_run_python_script_scope:

Test variable and function scope
-------------------------------------

In this example, we will call run_python_script and check the variable and
function scope between calls

"""

###############################################################################
# Example Setup
# -------------
# This workflow doesn't use any sample files
#
# Launch Mechanical
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Launch a new Mechanical Session in batch. 'cleanup_on_exit' set to False,
# you need to call mechanical.exit to close Mechanical.

import json
from ansys.mechanical.core import launch_mechanical
mechanical = launch_mechanical(batch=True, cleanup_on_exit=False)
print(mechanical)

###################################################################################
# Set variable
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script to set a value to a variable.

output = mechanical.run_python_script(
    """
x = 10
x
"""
)
print(f"x = {output}")

###################################################################################
# Access the variable in the next call
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script to change the variable value in the next call

output = mechanical.run_python_script(
    """
x = x * 2
x    
"""
)
print(f"x = {output}")

###################################################################################
# Define function
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script to define a function and access the variable defined in the
# previous call

output = mechanical.run_python_script(
    """
def multiply_by_10():
    return x*10
    
multiply_by_10()  
"""
)
print(f"output = {output}")

###################################################################################
# Access the function
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script to access the function defined in the previous call

output = mechanical.run_python_script(
    """
multiply_by_10() * 2   
"""
)
print(f"output = {output}")


###########################################################
# Close Mechanical
# ~~~~~~~~~~~~~~~~
# Close the Mechanical instance.

mechanical.exit()
