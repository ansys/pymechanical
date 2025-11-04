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

"""Embedding tests related to app data."""

import os
from pathlib import Path
import sys
from unittest import mock

import pytest

from ansys.mechanical.core.embedding.appdata import UniqueUserProfile


@pytest.mark.embedding_scripts
@pytest.mark.python_env
def test_private_appdata(pytestconfig, run_subprocess, rootdir):
    """Test embedded instance does not save ShowTriad using a test-scoped Python environment."""
    version = pytestconfig.getoption("ansys_version")
    embedded_py = Path(rootdir) / "tests" / "scripts" / "run_embedded_app.py"

    run_subprocess(
        [
            sys.executable,
            str(embedded_py),
            "--version",
            version,
            "--private_appdata",
            "True",
            "--action",
            "Set",
        ]
    )
    process, stdout, stderr = run_subprocess(
        [
            sys.executable,
            str(embedded_py),
            "--version",
            version,
            "--private_appdata",
            "True",
            "--action",
            "Run",
        ]
    )
    stdout = stdout.decode()
    assert "ShowTriad value is True" in stdout


@pytest.mark.embedding_scripts
@pytest.mark.python_env
def test_normal_appdata(pytestconfig, run_subprocess, rootdir):
    """Test embedded instance saves ShowTriad value using a test-scoped Python environment."""
    version = pytestconfig.getoption("ansys_version")

    embedded_py = Path(rootdir) / "tests" / "scripts" / "run_embedded_app.py"

    run_subprocess(
        [
            sys.executable,
            str(embedded_py),
            "--version",
            version,
            "--private_appdata",
            "False",
            "--action",
            "Set",
        ]
    )
    process, stdout, stderr = run_subprocess(
        [
            sys.executable,
            str(embedded_py),
            "--version",
            version,
            "--private_appdata",
            "False",
            "--action",
            "Run",
        ]
    )
    run_subprocess(
        [
            sys.executable,
            str(embedded_py),
            "--version",
            version,
            "--private_appdata",
            "False",
            "--action",
            "Reset",
        ]
    )

    stdout = stdout.decode()
    # Assert ShowTriad was set to False for regular embedded session
    assert "ShowTriad value is False" in stdout


@pytest.mark.embedding
def test_uniqueprofile_creation():
    """Test profile is copied when copy_profile is ``True`` and is not copied when ``False``."""
    folder_to_check = Path("AppData") / "Local" / "Ansys" if os.name == "nt" else Path(".mw")

    # Create private app data without copying profiles
    private_data2 = UniqueUserProfile(profile_name="test1", copy_profile=False)
    assert not (Path(private_data2.location) / folder_to_check).exists()

    # Check if location is same with same profile name
    private_data1 = UniqueUserProfile(profile_name="test1")
    assert private_data1.location == private_data2.location

    # Check if folder exists after copying profiles
    assert Path(private_data1.location / folder_to_check).exists()

    # Create new profile
    private_data3 = UniqueUserProfile(profile_name="test2")
    assert private_data2.location != private_data3.location


@pytest.mark.embedding
def test_uniqueprofile_env():
    """Test the environment is correctly updated for the profile based on operating system."""
    profile = UniqueUserProfile("test_env")
    env = {}
    platforms = ["win32", "linux"]

    for platform in platforms:
        with mock.patch.object(sys, "platform", platform):
            profile.update_environment(env)

    if platform == "win32":
        env["USERPROFILE"] = str(profile.location)
        env["APPDATA"] = str(Path(profile.location) / "AppData" / "Roaming")
        env["LOCALAPPDATA"] = str(Path(profile.location) / "AppData" / "Local")
        env["TMP"] = str(Path(profile.location) / "AppData" / "Local" / "Temp")
        env["TEMP"] = str(Path(profile.location) / "AppData" / "Local" / "Temp")
    else:
        env["HOME"] = str(profile.location)


@pytest.mark.embedding
def test_uniqueprofile_dryrun():
    """Test the profile is not copied during dry runs."""
    profile = UniqueUserProfile("test_dry_run", dry_run=True)
    assert not Path(profile.location).exists()
