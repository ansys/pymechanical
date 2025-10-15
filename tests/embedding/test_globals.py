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

"""Embedding tests for global variables associated with Mechanical."""

from pathlib import Path
import subprocess
import sys

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
    project_name = embedded_app.DataModel.Project.Name
    assert project_name == "Project"
    with Transaction():
        embedded_app.DataModel.Project.Name = "New Project"
    project_name = embedded_app.DataModel.Project.Name
    assert project_name == "New Project"


@pytest.mark.embedding_scripts
def test_global_importer_exception(rootdir):
    """Test an exception is raised in global_importer when the embedded app is not initialized."""
    # Path to global_importer.py
    global_importer = (
        rootdir / "src" / "ansys" / "mechanical" / "core" / "embedding" / "global_importer.py"
    )

    # Run the global_importer.py script without the app being initialized
    stdout, stderr = subprocess.Popen(
        [sys.executable, global_importer], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()

    # Assert the exception is raised
    assert "Globals cannot be imported until the embedded app is initialized." in stderr.decode()


@pytest.mark.embedding_scripts
def test_enum_importer_exception(rootdir):
    """Test an exception is raised in enum_importer when the embedded app is not initialized."""
    # Path to enum_importer.py
    enum_importer = (
        rootdir / "src" / "ansys" / "mechanical" / "core" / "embedding" / "enum_importer.py"
    )

    # Run the enum_importer.py script without the app being initialized
    stdout, stderr = subprocess.Popen(
        [sys.executable, enum_importer], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).communicate()

    # Assert the exception is raised
    assert "Enums cannot be imported until the embedded app is initialized." in stderr.decode()


@pytest.mark.embedding_scripts
def test_globals_kwarg_building_gallery(run_subprocess, pytestconfig, rootdir):
    """Test ViewOrientationType exists and messages are printed when BUILDING_GALLERY is True
    and globals are updated during the app initialization.
    """
    version = pytestconfig.getoption("ansys_version")
    embedded_py = Path(rootdir) / "tests" / "scripts" / "run_embedded_app.py"

    process, stdout, stderr = run_subprocess(
        [
            sys.executable,
            str(embedded_py),
            "--version",
            version,
            "--action",
            "TestGlobals",
        ]
    )
    stdout = stdout.decode()

    assert "ViewOrientationType exists" in stdout
    assert "The app cannot print messages in the building gallery" not in stdout
