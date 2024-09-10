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

import glob
import os
import pathlib
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
    try:
        app.save()
    except:
        raise Exception("The App must have already been saved before using launch_ui!")
    return True


class UILauncher():
    def save(self, app):
        app.save()



def _launch_ui(app, launcher):
    # all the implemation below goes here
    pass

def test_launch_ui(app):
    # there are also python frameworks for fake/mock objects...
    # if its one test it can go in the test, if its multiple it can be defined in the test_---.py file
    # or in a fixture in conftest
    class MockLauncher():
        def __init__(self):
            self.ops = []

        def save(self, app):
            self.ops.append("save")
    m = MockLauncher()
    _launch_ui(app, m)
    assert m.ops[0] == "save"

def launch_ui(app: "ansys.mechanical.core.embedding.App", testing: bool = False) -> Popen:
    """Launch the Mechanical UI.

    Precondition: Mechanical has to have already been saved
    Side effect: If Mechanical has ever been saved, it overwrites that save.
    """
    # not testing
    _launch_ui(UILauncher())

    if not _is_saved(app):
        raise Exception("The App must have already been saved before using launch_ui!")
    else:
        # Save the app
        app.save()

        # Identify the mechdb of the saved session
        project_directory = app.DataModel.Project.ProjectDirectory
        # print(project_directory)

        # list all files / find mechdb file in project_directory
        # find a command that lists active mechdb file
        level_above_projdir = pathlib.Path(project_directory).parent
        print(level_above_projdir)
        mechdb_list = glob.glob(f"{level_above_projdir}/*.mechdb")
        if len(mechdb_list) > 1:
            print("multiple mechdb files found")

        mechdb_file = mechdb_list[0]
        # print(f"mechdb file: {mechdb_file}")

        # Get the directory the mechdb_file is in and the name of the file
        dirname, basename = os.path.split(mechdb_file)
        # Create a named temporary file
        # temp_file = tempfile.NamedTemporaryFile()
        # # Get the name of the temporary file
        # temp_file_basename = os.path.basename(temp_file.name)
        # # print(f"temp_file name: {temp_file_basename}")
        # # Use the name of the temporary file to create a mechdb file
        # temp_file_name = os.path.join(dirname, f"{temp_file_basename}.mechdb")

        temp_file_name = tempfile.NamedTemporaryFile(
            dir=dirname, suffix=".mechdb", delete=True
        ).name

        # Save app with name of temporary file
        # file a bug about adding an option overwrite=True to `save_as`
        app.save_as(temp_file_name)

        # Open the mechdb of the saved session
        app.open(mechdb_file)

        # another option for testing:
        # if testing:
            # don't put --graphical in the args
            # return the process object
            # the test code can wait for the process to exit...
            # maybe work around the command line parsing of ansys-mechanical
        # Run ansys-mechanical on the save.mechdb in the temporary location
        p = Popen(
            [
                "ansys-mechanical",
                "--project-file",
                temp_file_name,
                "--graphical",
                "--revision",
                str(app.version),
            ]
            , env= os.environ.copy() # with some env var for DRY_RUN
        )

        # Problem: the mechdb started above will not automatically get cleaned up
        # option 1 - its the users problem, just tell them with a print
        print("Opened a new mechanical session based on ... {mechdb_file}. PyMechanical will not delete after use.")
        # option 2 - try to delete it (maybe this can be an opt-in, an argument to launch_ui??)
        #            by starting a background process that waits until the process exits and automatically cleans it up.
        #            like `Popen(f"python /path/to/cleanup-gui.py {p.pid}")`
        # option 3 - use a canonical name /tmp/some_name/file.mechdb and overwrite it each time launch_ui is run
        #            so that worst case only one extra mechdb is not cleaned up. The downside is that you can't use launch_ui
        #            in parallel but who would even do that? You can throw an exception if that mechdb file is open by another
        #            process at the beginning of this function...
        print(f"Done launching Ansys Mechanical {str(app.version)}...")
        return p

