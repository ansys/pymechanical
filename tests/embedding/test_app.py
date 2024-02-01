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

"""Miscellaneous embedding tests"""
# import datetime
import os
import subprocess
import sys
from tempfile import NamedTemporaryFile
import time

import pytest

import ansys.mechanical.core.embedding.utils as utils


@pytest.mark.embedding
def test_app_repr(embedded_app):
    """Test repr of the Application class."""
    app_repr_lines = repr(embedded_app).splitlines()
    assert app_repr_lines[0].startswith("Ansys Mechanical")
    assert app_repr_lines[1].startswith("Product Version")
    assert app_repr_lines[2].startswith("Software build date:")


@pytest.mark.embedding
@pytest.mark.minimum_version(241)
def test_deprecation_warning(embedded_app):
    struct = embedded_app.Model.AddStaticStructuralAnalysis()
    with pytest.warns(UserWarning):
        struct.SystemID


@pytest.mark.embedding
def test_app_save_open(embedded_app, tmp_path: pytest.TempPathFactory):
    """Test save and open of the Application class."""
    import System
    import clr  # noqa: F401

    # save without a save_as throws an exception
    with pytest.raises(System.Exception):
        embedded_app.save()

    embedded_app.DataModel.Project.Name = "PROJECT 1"
    tmpfile = NamedTemporaryFile()
    tmpname = tmpfile.name
    project_file = os.path.join(tmp_path, f"{tmpname}.mechdat")
    embedded_app.save_as(project_file)
    embedded_app.new()
    embedded_app.open(project_file)
    assert embedded_app.DataModel.Project.Name == "PROJECT 1"
    embedded_app.DataModel.Project.Name = "PROJECT 2"
    embedded_app.save()
    embedded_app.new()
    embedded_app.open(project_file)
    assert embedded_app.DataModel.Project.Name == "PROJECT 2"
    embedded_app.new()


@pytest.mark.embedding
def test_app_version(embedded_app):
    """Test version of the Application class."""
    version = embedded_app.version
    assert type(version) is int
    assert version >= 231


@pytest.mark.embedding
def test_nonblock_sleep(embedded_app):
    """Test non-blocking sleep."""
    t1 = time.time()
    utils.sleep(2000)
    t2 = time.time()
    assert (t2 - t1) >= 2


@pytest.mark.embedding
def test_app_getters_notstale(embedded_app):
    """The getters of app should be usable after a new().

    The C# objects referred to by ExtAPI, Model, DataModel, and Tree
    are reset on each call to app.new(), so storing them in
    global variables will be broken.

    To resolve this, we have to wrap those objects, and ensure
    that they properly redirect the calls to the appropriate C#
    object after a new()
    """
    data_model = embedded_app.DataModel
    data_model.Project.Name = "a"
    model = embedded_app.Model
    model.Name = "b"
    embedded_app.new()
    assert data_model.Project.Name != "a"
    assert model.Name != "b"


@pytest.mark.embedding
@pytest.mark.python_env
def test_warning_message(test_env, pytestconfig, rootdir):
    """Test Python.NET warning of the embedded instance using a test-scoped Python environment."""

    # Install pymechanical
    subprocess.check_call(
        [test_env.python, "-m", "pip", "install", "-e", "."],
        cwd=rootdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=test_env.env,
        close_fds=True,
    )

    # Install pythonnet
    install_pythonnet = subprocess.Popen(
        [test_env.python, "-m", "pip", "install", "pythonnet"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=test_env.env,
        close_fds=True,
    )
    install_pythonnet.communicate()

    # Run embedded instance in virtual env with pythonnet installed
    embedded_py = os.path.join(rootdir, "tests", "scripts", "run_embedded_app.py")
    check_warning = subprocess.Popen(
        [test_env.python, embedded_py, pytestconfig.getoption("ansys_version")],
        stderr=subprocess.PIPE,
        env=test_env.env,
        close_fds=True,
    )
    stdout, stderr = check_warning.communicate()

    # If UserWarning & pythonnet are in the stderr output, set warning to True.
    # Otherwise, set warning to False
    warning = True if "UserWarning" and "pythonnet" in stderr.decode() else False

    # Assert warning message appears for embedded app
    assert warning, "UserWarning should appear in the output of the script"


# def print_stderr(process):
#     while True:
#         line = process.stderr.readline()
#         if not line:
#             break
#         print(line.rstrip().decode())
#     # time.sleep(0.001)


@pytest.mark.embedding
@pytest.mark.python_env
def test_private_appdata(pytestconfig, rootdir):
    """Test embedded instance does not save ShowTriad using a test-scoped Python environment."""
    version = pytestconfig.getoption("ansys_version")
    embedded_py = os.path.join(rootdir, "tests", "scripts", "run_embedded_app.py")

    # Set ShowTriad to False
    p1 = subprocess.Popen(
        [sys.executable, embedded_py, version, "True", "Set"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
    )
    # print_stderr(p1)
    p1.communicate()

    # Check ShowTriad is True for private_appdata embedded sessions
    p2 = subprocess.Popen(
        [sys.executable, embedded_py, version, "True", "Run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
    )
    # print_stderr(p2)
    stdout, stderr = p2.communicate()

    assert "ShowTriad value is True" in stdout.decode()


# @pytest.mark.embedding
# @pytest.mark.python_env
# def test_normal_appdata(pytestconfig, rootdir):
#     """Test embedded instance saves ShowTriad value using a test-scoped Python environment."""
#     version = pytestconfig.getoption("ansys_version")
#     embedded_py = os.path.join(rootdir, "tests", "scripts", "run_embedded_app.py")

#     # Set ShowTriad to False
#     p1 = subprocess.Popen(
#         [sys.executable, embedded_py, version, "False", "Set"],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         close_fds=True,
#     )
#     print_stderr(p1)
#     p1.communicate()

#     # Check ShowTriad is False for regular embedded session
#     p2 = subprocess.Popen(
#         [sys.executable, embedded_py, version, "False", "Run"],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         close_fds=True,
#     )
#     print_stderr(p2)
#     stdout, stderr = p2.communicate()

#     # Set ShowTriad back to True for regular embedded session
#     p3 = subprocess.Popen(
#         [sys.executable, embedded_py, version, "False", "Reset"],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         close_fds=True,
#     )
#     print_stderr(p3)
#     p3.communicate()

#     # Assert ShowTriad was set to False for regular embedded session
#     assert "ShowTriad value is False" in stdout.decode()


@pytest.mark.embedding
def test_rm_lockfile(embedded_app, tmp_path: pytest.TempPathFactory):
    """Test lock file is removed on close of embedded application."""
    mechdat_path = os.path.join(tmp_path, "test.mechdat")
    embedded_app.save(mechdat_path)
    embedded_app.close()

    lockfile_path = os.path.join(embedded_app.DataModel.Project.ProjectDirectory, ".mech_lock")
    # Assert lock file path does not exist
    assert not os.path.exists(lockfile_path)
