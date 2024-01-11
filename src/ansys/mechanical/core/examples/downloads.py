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

"""Functions to download sample datasets from the PyAnsys data repository."""

import os
import shutil
from typing import Optional
from urllib.parse import urljoin
import urllib.request

import ansys.mechanical.core as pymechanical

# __all__ = ['download_file']


def _joinurl(base, *paths):
    for path in paths:
        if base[-1] != "/":
            base += "/"
        base = urljoin(base, path)
    return base


def _get_default_server_and_joiner():
    return "https://github.com/ansys/example-data/raw/master", _joinurl


def _get_filepath_on_default_server(filename: str, *directory: str):
    server, joiner = _get_default_server_and_joiner()
    if directory:
        return joiner(server, *directory, filename)
    else:
        return joiner(server, filename)


def _retrieve_url(url, dest):
    saved_file, _ = urllib.request.urlretrieve(url, filename=dest)
    return saved_file


def _retrieve_data(url: str, filename: str, dest: str = None, force: bool = False):
    if dest is None:
        dest = pymechanical.EXAMPLES_PATH
    local_path = os.path.join(dest, os.path.basename(filename))
    if not force and os.path.isfile(local_path):
        return local_path
    local_path = _retrieve_url(url, local_path)
    return local_path


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
    Tuple[str, str]
        Tuple containing filepath to be used and the local filepath of the downloaded directory
        The two are different in case of containers.

    Examples
    --------
    Download a file from the server

    >>> from ansys.mechanical.core import examples
    >>> filename = examples.download_file('example_01_geometry.agdb', 'pymechanical', '00_basic')
    >>> filename
    'C:/Users/user/AppData/Local/ansys_mechanical_core/ansys_mechanical_core/examples/example_01_geometry.agdb'
    """
    url = _get_filepath_on_default_server(filename, *directory)
    local_path = _retrieve_data(url, filename, dest=destination, force=force)
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
    shutil.rmtree(pymechanical.EXAMPLES_PATH)
    os.makedirs(pymechanical.EXAMPLES_PATH)
    return True
