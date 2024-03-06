# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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

"""Additional imports for embedded Mechanical."""
import typing


def global_variables(app: "ansys.mechanical.core.App", enums: bool = False) -> typing.Dict:
    """Return the Mechanical scripting global variables as a dict.

    It can be used to add all of these as global variables in python
    with this command:
        `globals().update(global_variables(embedded_app))`

    To also import all the enums, set the parameter enums to true.
    """
    vars = {}
    vars["ExtAPI"] = app.ExtAPI
    vars["DataModel"] = app.DataModel
    vars["Model"] = app.DataModel.Project.Model
    vars["Tree"] = app.DataModel.Tree
    import clr  # isort: skip

    clr.AddReference("System.Collections")
    clr.AddReference("Ansys.ACT.WB1")
    clr.AddReference("Ansys.Mechanical.DataModel")
    # from Ansys.ACT.Mechanical import Transaction
    # When ansys-pythonnet issue #14 is fixed, uncomment above
    from Ansys.Core.Units import Quantity
    from Ansys.Mechanical.DataModel import MechanicalEnums

    import System  # isort: skip
    import Ansys  # isort: skip

    vars["Quantity"] = Quantity
    vars["System"] = System
    vars["Ansys"] = Ansys
    vars["Transaction"] = Transaction
    vars["MechanicalEnums"] = MechanicalEnums

    if enums:
        vars.update(get_all_enums())

    return vars


def get_all_enums() -> typing.Dict[str, typing.Any]:
    """Get all the enums as a dictionary."""
    import ansys.mechanical.core.embedding.enum_importer as enum_importer

    enums = {}
    for attr in dir(enum_importer):
        if not hasattr(enum_importer, attr):
            continue
        the_enum = getattr(enum_importer, attr)
        if type(the_enum).__name__ == "CLRMetatype":
            enums[attr] = the_enum
    return enums


class Transaction:  # When ansys-pythonnet issue #14 is fixed, this class will be removed
    """
    A class to speed up bulk user interactions using Ansys ACT Mechanical Transaction.

    Example
    -------
    >>> with Transaction() as transaction:
    ...     pass   # Perform bulk user interactions here
    ...
    """

    def __init__(self):
        """Initialize the Transaction class."""
        import clr

        clr.AddReference("Ansys.ACT.WB1")
        import Ansys

        self._transaction = Ansys.ACT.Mechanical.Transaction()

    def __enter__(self):
        """Enter the context of the transaction."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context of the transaction and disposes of resources."""
        self._transaction.Dispose()
