# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.mechanical.core.embedding import App
from pathlib import Path

# Subprocess is needed to launch the GUI and clean up the process on close.
# Excluding bandit check.
from subprocess import Popen  # nosec: B404
import sys
import tempfile
import typing


class UILauncher:
    """Launch the GUI using a temporary mechdb file."""

    def __init__(self, dry_run: bool = False):
        """Initialize UILauncher class."""
        self._dry_run = dry_run

    def save_original(self, app: App) -> None:
        """Save the active mechdb file.

        Parameters
        ----------
        app: ansys.mechanical.core.embedding.app.App
            A Mechanical embedding application.
        """
        app.save()

    def save_temp_copy(self, app: App) -> typing.Union[Path, Path]:
        """Save a new mechdb file with a temporary name.

        Parameters
        ----------
        app: ansys.mechanical.core.embedding.app.App
            A Mechanical embedding application.
        """
        # Identify the mechdb of the saved session from save_original()
        project_directory = Path(app.project_directory)
        project_directory_parent = project_directory.parent
        mechdb_file = (
            project_directory_parent / f"{project_directory.parts[-1].split('_')[0]}.mechdb"
        )

        # Get name of NamedTemporaryFile
        temp_file_name = tempfile.NamedTemporaryFile(
            dir=project_directory_parent, suffix=".mechdb", delete=True
        ).name

        # Save app with name of temporary file
        app.save_as(temp_file_name)

        return mechdb_file, temp_file_name

    def open_original(self, app: App, mechdb_file: str) -> None:
        """Open the original mechdb file from save_original().

        Parameters
        ----------
        app: ansys.mechanical.core.embedding.app.App
            A Mechanical embedding application.
        mechdb_file: str
            The full path to the active mechdb file.
        """
        app.open(mechdb_file)

    def graphically_launch_temp(self, app: App, temp_file: Path) -> typing.Union[Popen, str]:
        """Launch the GUI for the mechdb file with a temporary name from save_temp_copy().

        Parameters
        ----------
        app: ansys.mechanical.core.embedding.app.App
            A Mechanical embedding application.
        temp_file: pathlib.Path
            The full path to the temporary mechdb file.

        Returns
        -------
        subprocess.Popen
            The subprocess that launches the GUI for the temporary mechdb file.
        """
        # The ansys-mechanical command to launch the GUI in a subprocess
        args = [
            "ansys-mechanical",
            "--project-file",
            temp_file,
            "--graphical",
            "--revision",
            str(app.version),
        ]
        if not self._dry_run:
            try:
                # The subprocess that uses ansys-mechanical to launch the GUI of the temporary
                # mechdb file
                process = Popen(args)  # nosec: B603 # pragma: no cover
            except Exception:
                print("Failed to launch Mechanical GUI with args: ", args)
                print("Retrieving the path to the Mechanical executable directly...")
                try:
                    import ansys.tools.common.path as atp
                except ImportError:
                    import ansys.tools.path as atp
                exe = atp.get_mechanical_path(allow_input=False, version=app.version)
                args = [
                    exe,
                    "--project-file",
                    str(temp_file),
                    "--graphical",
                    "--revision",
                    str(app.version),
                ]
                process = Popen(args)  # nosec: B603 # pragma: no cover
            return process
        else:
            # Return a string containing the args
            return " ".join(args)

    def _cleanup_gui(self, process: Popen, temp_mechdb_path: Path) -> None:
        """Remove the temporary mechdb file and folder when the GUI is closed.

        Parameters
        ----------
        process: subprocess.Popen
            The subprocess that launched the GUI of the temporary mechdb file.
        temp_mechdb_path: pathlib.Path
            The full path to the temporary mechdb file.
        """
        # Get the path to the cleanup script
        cleanup_script = Path(__file__).parent / "cleanup_gui.py"  # pragma: no cover

        if not self._dry_run:
            # Open a subprocess to remove the temporary mechdb file and folder when the process ends
            Popen(
                [sys.executable, cleanup_script, str(process.pid), temp_mechdb_path]
            )  # pragma: no cover # nosec: B603


def _is_saved(app: App) -> bool:
    """Check if the mechdb file has been saved and raise an exception if not.

    Parameters
    ----------
    app: ansys.mechanical.core.embedding.app.App
        A Mechanical embedding application.

    Returns
    -------
    bool
        ``True`` when the embedded app has been saved.
        ``False`` when the embedded app has not been saved.
    """
    try:
        app.save()
    except Exception as e:
        raise Exception("The App must have already been saved before using launch_ui!") from e
    return True


def _launch_ui(app: App, delete_tmp_on_close: bool, launcher: UILauncher) -> None:
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
        # Save the active mechdb file.
        launcher.save_original(app)
        # Save a new mechdb file with a temporary name.
        mechdb_file, temp_file = launcher.save_temp_copy(app)
        # Open the original mechdb file from save_original().
        launcher.open_original(app, str(mechdb_file))
        # Launch the GUI for the mechdb file with a temporary name from save_temp_copy().
        process = launcher.graphically_launch_temp(app, temp_file)

        # If it's a dry run and graphically_launch_temp returned a string, print the string
        if isinstance(process, str):
            print(process)

        # If the user wants the temporary file to be deleted and graphically_launch_temp
        # returned a process. By default, this is True
        if delete_tmp_on_close and not isinstance(process, str):
            # Remove the temporary mechdb file and folder when the GUI is closed.
            launcher._cleanup_gui(process, temp_file)  # pragma: no cover
        else:
            # Let the user know that the mechdb started above will not automatically get cleaned up
            print(
                f"""Opened a new mechanical session based on {mechdb_file} named {temp_file}.
PyMechanical will not delete it after use."""
            )


def launch_ui(
    app: App,
    delete_tmp_on_close: bool = True,
    dry_run: bool = False,
) -> None:
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
    dry_run: bool
        Whether or not to launch the GUI. By default, this is ``False``.
    """
    _launch_ui(app, delete_tmp_on_close, UILauncher(dry_run))
