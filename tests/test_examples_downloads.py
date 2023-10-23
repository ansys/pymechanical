# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

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
