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
"""Clean up temporary mechdb files after GUI is closed."""

from pathlib import Path
import shutil
import sys
import time

import psutil


def cleanup_gui(pid, temp_mechdb) -> None:
    """Remove the temporary mechdb file after it is closed.

    Parameters
    ----------
    pid: int
        The process ID of the open temporary mechdb file.
    temp_mechdb: Path
        The path of the temporary mechdb file.
    """
    # While the pid exists, sleep
    while psutil.pid_exists(pid):
        time.sleep(1)

    # Delete the temporary mechdb file once the GUI is closed
    temp_mechdb.unlink()

    # Delete the temporary mechdb Mech_Files folder
    temp_folder_path = temp_mechdb.parent / f"{temp_mechdb.name.split('.')[0]}_Mech_Files"
    shutil.rmtree(temp_folder_path)


if __name__ == "__main__":  # pragma: no cover
    """Get the process ID and temporary file path to monitor and delete files after use."""
    # Convert the process id (pid) argument into an integer
    pid = int(sys.argv[1])
    # Convert the temporary mechdb path into a Path
    temp_mechdb_path = Path(sys.argv[2])
    # Remove the temporary mechdb file when the GUI is closed
    cleanup_gui(pid, temp_mechdb_path)
