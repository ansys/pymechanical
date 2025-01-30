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

"""Embedding tests for global variables associated with Mechanical"""
import pytest

from ansys.mechanical.core import global_variables
from ansys.mechanical.core.embedding.transaction import Transaction


@pytest.mark.embedding
def test_global_variables(embedded_app):
    """Test the global variables."""
    attributes = [
        "ExtAPI",
        "DataModel",
        "Model",
        "Tree",
        "Graphics",
        "Quantity",
        "System",
        "Ansys",
        "Transaction",
        "MechanicalEnums",
        "DataModelObjectCategory",
        "Point",
        "SectionPlane",
        "Point2D",
        "Point3D",
        "Vector3D",
    ]
    globals_dict = global_variables(embedded_app, True)
    for attribute in attributes:
        assert attribute in globals_dict


@pytest.mark.embedding
def test_global_variable_transaction(embedded_app):
    embedded_app.update_globals(globals())
    project_name = DataModel.Project.Name
    assert project_name == "Project"
    with Transaction():
        DataModel.Project.Name = "New Project"
    project_name = DataModel.Project.Name
    assert project_name == "New Project"
