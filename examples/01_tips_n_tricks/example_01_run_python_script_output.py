""".. _ref_example_01_run_python_script_output:

Different output formats
-------------------------------

In this example, we will call run_python_script and get the output in string,
json and csv formats.

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
# Simple string output
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script to get a simple string output.

output = mechanical.run_python_script(
    """
def return_string():
    return "hello world"

return_string()
"""
)
print(f"string output={output}")

###################################################################################
# String output as json
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script to get the string output as json.

output = mechanical.run_python_script(
    """
def return_json():
    import json
    dict = {"value1": 100, "value2": 200}
    json_text = json.dumps(dict)
    return json_text

return_json()
"""
)
print(f"json output={output}")

my_dict = json.loads(output)
print(f"Parsed json: value1={my_dict['value1']}, value2={my_dict['value2']}")

###################################################################################
# String output as csv
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the script to get the string output as csv.

output = mechanical.run_python_script(
    """
def return_csv():
    return "1,2,3"

return_csv()
"""
)
print(f"csv output={output}")
csv_values = output.split(sep=",")
print(f"Parsed csv: {';'.join(csv_values)}")

###########################################################
# Close Mechanical
# ~~~~~~~~~~~~~~~~
# Close the Mechanical instance.

mechanical.exit()
