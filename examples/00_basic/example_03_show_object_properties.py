""".. _ref_example_03_show_object_properties:

Details View properties of an object
---------------------------------------

In this example, using the support files, you will display the properties that you would see in the
Details View of the object.

- SimpleBoltNew.mechdat
"""

###############################################################################
# Launch Mechanical
# ~~~~~~~~~~~~~~~~~
# Launch a new Mechanical Session in batch.

from ansys.mechanical.core import launch_mechanical

mechanical = launch_mechanical(batch=True)
print(mechanical)

###################################################################################
# Execute the Mechanical script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Execute the Mechanical script to display the properties and their current values

output = mechanical.run_python_script(
    """
import json
mechdb_path = r"C:\\temp\\pymechtest\\example_03_simple_bolt_new.mechdat"

# in case you are using the same instance to test this workflow
# let us start with a empty setup
ExtAPI.DataModel.Project.New()

ExtAPI.DataModel.Project.Open(mechdb_path)

analysisSettings = Model.Analyses[0].AnalysisSettings
props = {}
if hasattr(analysisSettings,'VisibleProperties') != False:
    for prop in analysisSettings.VisibleProperties:
        props[prop.Caption] = prop.StringValue

json.dumps(props, indent=1)
"""
)
print(output)

###################################################################################
# Don't save the project
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# exit without saving the project
mechanical.clear()

###########################################################
# Close Mechanical
# ~~~~~~~~~~~~~~~~
# Close Mechanical

mechanical.exit()
