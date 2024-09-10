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
from pathlib import Path
from subprocess import Popen
import tempfile
import typing

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
    try:
        app.save()
    except:
        raise Exception("The App must have already been saved before using launch_ui!")
    return True


class UILauncher:
    """Launch the GUI on a temporary mechdb file."""

    def save_original(self, app) -> None:
        """Save the active mechdb file.

        Parameters
        ----------
        app: ansys.mechanical.core.embedding.app.App
            A Mechanical embedding application.
        """
        app.save()

    def save_temp_copy(self, app) -> typing.Union[Path, Path]:
        """Save a new mechdb file with a temporary name.

        Parameters
        ----------
        app: ansys.mechanical.core.embedding.app.App
            A Mechanical embedding application.
        """
        # Identify the mechdb of the saved session from save_original()
        project_directory = Path(app.DataModel.Project.ProjectDirectory)
        project_directory_parent = project_directory.parent
        mechdb_file = os.path.join(
            project_directory_parent, f"{project_directory.parts[-1].split('_')[0]}.mechdb"
        )

        # Get name of NamedTemporaryFile
        temp_file_name = tempfile.NamedTemporaryFile(
            dir=project_directory_parent, suffix=".mechdb", delete=True
        ).name

        # Save app with name of temporary file
        app.save_as(temp_file_name)

        return mechdb_file, temp_file_name

    def open_original(self, app, mechdb_file) -> None:
        """Open the original mechdb file from save_original().

        Parameters
        ----------
        app: ansys.mechanical.core.embedding.app.App
            A Mechanical embedding application.
        mechdb_file: pathlib.Path
            The full path to the active mechdb file.
        """
        app.open(mechdb_file)

    def graphically_launch_temp(self, app, mechdb_file, temp_file) -> Popen:
        """Launch the GUI for the mechdb file with a temporary name from save_temp_copy().

        Parameters
        ----------
        app: ansys.mechanical.core.embedding.app.App
            A Mechanical embedding application.
        mechdb_file: pathlib.Path
            The full path to the active mechdb file.
        temp_file: pathlib.Path
            The full path to the temporary mechdb file.

        Returns
        -------
        subprocess.Popen
            The subprocess that launches the GUI for the temporary mechdb file.
        """
        p = Popen(
            [
                "ansys-mechanical",
                "--project-file",
                temp_file,
                "--graphical",
                "--revision",
                str(app.version),
            ]
            # , env= os.environ.copy() # with some env var for DRY_RUN
        )

        # Problem: the mechdb started above will not automatically get cleaned up
        # option 1 - its the users problem, just tell them with a print
        print(
            f"""Opened a new mechanical session based on ... {mechdb_file}. \
            PyMechanical will not delete after use."""
        )
        # option 2 - try to delete it (maybe this can be an opt-in, an argument to launch_ui??)
        #            by starting a background process that waits until the process exits and
        #            automatically cleans it up like
        #            `Popen(f"python /path/to/cleanup-gui.py {p.pid}")`
        # option 3 - use a canonical name /tmp/some_name/file.mechdb and overwrite it each time
        #            launch_ui is run so that worst case only one extra mechdb is not cleaned up.
        #            The downside is that you can't use launch_ui in parallel but who would even
        #            do that? You can throw an exception if that mechdb file is open by another
        #            process at the beginning of this function...
        print(f"Done launching Ansys Mechanical {str(app.version)}...")

        return p


# class MockLauncher:
#     def __init__(self):
#         self.ops = []

#     def save(self, app):
#         self.ops.append("save")


def _launch_ui(app, launcher):
    # all the implemation below goes here
    if not _is_saved(app):
        raise Exception("The App must have already been saved before using launch_ui!")
    else:
        launcher.save_original(app)
        mechdb_file, temp_file = launcher.save_temp_copy(app)
        launcher.open_original(app, mechdb_file)
        p = launcher.graphically_launch_temp(app, mechdb_file, temp_file)
        return p


def launch_ui(app: "ansys.mechanical.core.embedding.App", testing: bool = False) -> Popen:
    """Launch the Mechanical UI.

    Precondition: Mechanical has to have already been saved
    Side effect: If Mechanical has ever been saved, it overwrites that save.
    """
    if not testing:
        _launch_ui(app, UILauncher())
