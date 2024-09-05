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

"""Run Mechanical UI from python."""

import os
from subprocess import Popen
import tempfile

"""
If Mechanical has ever been saved, then we are allowed to use `app.save()`,
otherwise, we have to use `app.save_as()` and pass a temp file path which
will have to be cleaned up later...

Mechanical can be in one of three states:
1. not-saved
2. saved|dirty
3. saved|not-dirty

#1
Example:
    app = App()
    ...
    app.launch_gui()

A save_as() to save1.mechdb
B save_as() to save2.mechdb
C open() the mechdb from A
D run ansys-mechanical -g on save2.mechdb

** side-effect: not-saved => saved|not-dirty

#2
Example:
    app.save_as("/path/to/file.mechdb")
    app.project_file =>
        "/path/to/file.mechdb"
    ...
    app.launch_gui()
    app.project_file =>
        "/path/to/save2.mechdb"

A save()
B identify the mechdb of the saved session
C save_as() to a save.mechdb
D open() the mechdb from A
E run ansys-mechanical -g on save.mechdb from C

** side-effect: saved|dirty => saved|not-dirty

#3
Example:
    app.save_as("/path/to/some/file.mechdb")
    app.launch_gui()


A save()
B identify the mechdb of the saved session
C save_as() into a save.mechdb
D open() the mechdb saved session (from A)
E run ansys-mechanical -g on that temp path (B)
** side-effect: no side effect

side-effect of all:
    If we are either in a dirty state or have never been saved, we went to a save|not-dirty state

side-effect/bug:
    There is now a mechdb in the temp folder that is leaked.

"""


def _is_saved(app: "ansys.mechanical.core.embedding.App"):
    return True


def launch_ui(app: "ansys.mechanical.core.embedding.App"):
    """Launch the Mechanical UI.

    Precondition: Mechanical has to have already been saved
    Side effect: If Mechanical has ever been saved, it overwrites that save.
    """

    if not _is_saved(app):
        raise Exception("The App must have already been saved before using launch_ui!")

    """
    A save()
    B identify the mechdb of the saved session
    C save_as() to a save.mechdb
    D open() the mechdb from A
    E run ansys-mechanical -g on save.mechdb from C
    """

    # Get the project directory
    project_directory = app.DataModel.Project.ProjectDirectory
    # Create a temporary file
    named_temp_file = tempfile.NamedTemporaryFile()
    # Create the entire mechdb file path
    temp_mechdb = os.path.join(project_directory, f"{named_temp_file.name}.mechdb")
    # Call SaveAs - SaveAs copies the entire directory
    app.DataModel.Project.SaveAs(os.path.join(project_directory, f"{named_temp_file.name}.mechdb"))
    # Launch the temporary mechdb file in GUI mode
    Popen(
        [
            "ansys-mechanical",
            "--project-file",
            temp_mechdb,
            "--graphical",
            "--revision",
            str(app.version),
        ]
    )
    print(f"Done launching Ansys Mechanical {str(app.version)}...")
