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

import os.path

import pytest

from ansys.mechanical.core import examples


@pytest.mark.remote_session_connect
def test_download_file():
    # first time download
    filename = examples.download_file("example_01_geometry.agdb", "pymechanical", "00_basic")
    assert os.path.isfile(filename)

    # file already exists in the cache, do not force the download
    filename = examples.download_file("example_01_geometry.agdb", "pymechanical", "00_basic")
    assert os.path.isfile(filename)

    # file already exists in the cache, force it to download again
    filename = examples.download_file(
        "example_01_geometry.agdb", "pymechanical", "00_basic", force=True
    )
    assert os.path.isfile(filename)

    # cleanup downloaded file
    examples.delete_downloads()
    assert not os.path.isfile(filename)
