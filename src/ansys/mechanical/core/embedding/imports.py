import clr


def global_variables(app):
    vars = {}
    vars["ExtAPI"] = app.ExtAPI
    vars["DataModel"] = app.DataModel
    vars["Model"] = app.DataModel.Project.Model
    vars["Tree"] = app.DataModel.Tree
    import clr

    clr.AddReference("System.Collections")
    import Ansys
    import System
    from Ansys.Core.Units import Quantity

    vars["Quantity"] = Quantity
    vars["System"] = System
    vars["Ansys"] = Ansys
    return vars
