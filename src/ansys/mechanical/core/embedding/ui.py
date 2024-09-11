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

"""Run Mechanical UI from Python."""

import atexit
import os
from pathlib import Path
from subprocess import Popen
import sys
import tempfile
import typing


class UILauncher:
    """Launch the GUI using a temporary mechdb file."""

    def save_original(self, app: "ansys.mechanical.core.embedding.App") -> None:
        """Save the active mechdb file.

        Parameters
        ----------
        app: ansys.mechanical.core.embedding.app.App
            A Mechanical embedding application.
        """
        app.save()

    def save_temp_copy(
        self, app: "ansys.mechanical.core.embedding.App"
    ) -> typing.Union[Path, Path]:
        """Save a new mechdb file with a temporary name.

        Parameters
        ----------
        app: ansys.mechanical.core.embedding.app.App
            A Mechanical embedding application.
        """
        # Identify the mechdb of the saved session from save_original()
        project_directory = Path(app.DataModel.Project.ProjectDirectory)
        project_directory_parent = project_directory.parent
        print(project_directory_parent)
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

    def open_original(self, app: "ansys.mechanical.core.embedding.App", mechdb_file: Path) -> None:
        """Open the original mechdb file from save_original().

        Parameters
        ----------
        app: ansys.mechanical.core.embedding.app.App
            A Mechanical embedding application.
        mechdb_file: pathlib.Path
            The full path to the active mechdb file.
        """
        app.open(mechdb_file)

    def graphically_launch_temp(
        self, app: "ansys.mechanical.core.embedding.App", mechdb_file: Path, temp_file: Path
    ) -> Popen:
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
            ],
        )

        return p

    def _cleanup_gui(self, process, temp_mechdb_path):
        cleanup_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cleanup_gui.py")
        Popen([sys.executable, cleanup_script, str(process.pid), temp_mechdb_path])


def _is_saved(app: "ansys.mechanical.core.embedding.App") -> bool:
    """Check if the mechdb file has been saved and raise an exception if not.

    Parameters
    ----------
    app: ansys.mechanical.core.embedding.app.App
        A Mechanical embedding application.
    """
    try:
        app.save()
    except:
        raise Exception("The App must have already been saved before using launch_ui!")
    return True


def _launch_ui(
    app: "ansys.mechanical.core.embedding.App", delete_tmp_on_close: bool, launcher: UILauncher
) -> None:
    """Launch the Mechanical UI if the mechdb file has been saved.

    Parameters
    ----------
    app: ansys.mechanical.core.embedding.app.App
        A Mechanical embedding application.
    delete_tmp_on_close: bool
        Whether to delete the temporary mechdb file when the GUI is closed.
        By default, this is ``True``.
    launcher: UILauncher
        Launch the GUI using a temporary mechdb file.
    """
    if _is_saved(app):
        launcher.save_original(app)
        mechdb_file, temp_file = launcher.save_temp_copy(app)
        launcher.open_original(app, mechdb_file)
        p = launcher.graphically_launch_temp(app, mechdb_file, temp_file)

        # If the user wants the temporary file to be deleted
        if delete_tmp_on_close:
            atexit.register(launcher._cleanup_gui, p, temp_file)
        else:
            # Let the user know that the mechdb started above will not automatically get cleaned up
            print(
                f"""Opened a new mechanical session based on {mechdb_file} named {temp_file}.
PyMechanical will not delete it after use."""
            )


def launch_ui(app: "ansys.mechanical.core.embedding.App", delete_tmp_on_close: bool = True) -> None:
    """Launch the Mechanical UI.

    Precondition: Mechanical has to have already been saved
    Side effect: If Mechanical has ever been saved, it overwrites that save.

    Parameters
    ----------
    app: ansys.mechanical.core.embedding.app.App
        A Mechanical embedding application.
    delete_tmp_on_close: bool
        Whether to delete the temporary mechdb file when the GUI is closed.
        By default, this is ``True``.
    """
    _launch_ui(app, delete_tmp_on_close, UILauncher())
