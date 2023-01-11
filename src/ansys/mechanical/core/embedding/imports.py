"""Additional imports for embedded Mechanical."""
import typing


def global_variables(app: "ansys.mechanical.core.App") -> typing.Dict:
    """Return the Mechanical scripting global variables as a dict.

    It can be used to add all of these as global variables in python
    with this command:
        `globals().update(global_variables(embedded_app))`
    """
    vars = {}
    vars["ExtAPI"] = app.ExtAPI
    vars["DataModel"] = app.DataModel
    vars["Model"] = app.DataModel.Project.Model
    vars["Tree"] = app.DataModel.Tree
    import clr  # isort: skip

    clr.AddReference("System.Collections")
    from Ansys.Core.Units import Quantity

    import System  # isort: skip
    import Ansys  # isort: skip

    vars["Quantity"] = Quantity
    vars["System"] = System
    vars["Ansys"] = Ansys
    return vars
