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

"""Functions to download sample datasets from the PyAnsys data repository."""

from pathlib import Path
import shutil
from typing import Optional

from ansys.tools.common.example_download import download_manager

import ansys.mechanical.core as pymechanical

__all__ = ["download_file", "delete_downloads"]


def download_file(
    filename: str, *directory: str, destination: Optional[str] = None, force: bool = False
):
    """Download a file from PyAnsys examples Github repo.

    Parameters
    ----------
    filename: str
        Name of the file to download
    directory: tuple[str]
        Path under the PyAnsys Github examples repo
    destination: Optional[str]
        Optional destination to download the directory to
    force: bool
        Flag to force download even if the file exists in cache

    Returns
    -------
    str
        Filepath to the downloaded file

    Examples
    --------
    Download a file from the server

    >>> from ansys.mechanical.core import examples
    >>> filename = examples.download_file("example_01_geometry.agdb", "pymechanical", "00_basic")
    >>> filename
    'C:/Users/user/AppData/Local/ansys_mechanical_core/ansys_mechanical_core/examples/example_01_geometry.agdb'

    Download using the download manager

    >>> filename = examples.download_file("11_blades_mode_1_ND_0.csv", "pymapdl", "cfx_mapping")
    >>> filename
    'C:/Users/user/AppData/Local/ansys_mechanical_core/ansys_mechanical_core/examples/11_blades_mode_1_ND_0.csv'
    """
    # Convert directory tuple to path string
    directory_path = "/".join(directory) if directory else ""

    # Use ansys.tools.example_download
    # If no destination is provided, use the default EXAMPLES_PATH
    if destination is None:
        destination = pymechanical.EXAMPLES_PATH

    local_path = download_manager.download_file(
        filename, directory_path, destination=destination, force=force
    )
    return local_path


def delete_downloads() -> bool:
    """Delete all downloaded examples to free space or update the files.

    Returns
    -------
    bool
        ``True`` if delete_downlaods succeeds, ``False`` otherwise.

    Examples
    --------
    Delete all downloaded examples

    >>> from ansys.mechanical.core import examples
    >>> return_value = examples.delete_downloads()
    >>> return_value
    'True'

    """
    examples_path = Path(pymechanical.EXAMPLES_PATH)
    if examples_path.exists():
        shutil.rmtree(examples_path)
    examples_path.mkdir(parents=True, exist_ok=True)
    return True
