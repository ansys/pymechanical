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
def test_app_poster(embedded_app):
    """The getters of app should be usable after a new().

    The C# objects referred to by ExtAPI, Model, DataModel, and Tree
    are reset on each call to app.new(), so storing them in
    global variables will be broken.

    To resolve this, we have to wrap those objects, and ensure
    that they properly redirect the calls to the appropriate C#
    object after a new()
    """
    version = embedded_app.version
    if os.name != "nt" and version < 242:
        """This test is effectively disabled for versions older than 242 on linux.

        This is because the function coded is distributed with the C# library
        Ansys.Mechanical.CPython.dll. That library only began to be shipping on
        linux in 2024 R2.
        """
        return
    poster = embedded_app.poster

    def change_name_async(poster):
        """Change_name_async will run a background thread

        It will change the name of the project to "foo"
        """

        def change_name():
            embedded_app.DataModel.Project.Name = "foo"

        poster.post(change_name)

    import threading

    change_name_thread = threading.Thread(target=change_name_async, args=(poster,))
    change_name_thread.start()

    # The poster can't do anything unless the main thread is receiving
    # messages. The `sleep` utility puts Mechanical's main thread to
    # idle and only execute actions that have been posted to its main
    # thread, e.g. `change_name` that was posted by the poster.
    utils.sleep(400)
    change_name_thread.join()
    assert embedded_app.DataModel.Project.Name == "foo"


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
        env=test_env.env,
    )

    # Install pythonnet
    subprocess.check_call([test_env.python, "-m", "pip", "install", "pythonnet"], env=test_env.env)

    # Run embedded instance in virtual env with pythonnet installed
    embedded_py = os.path.join(rootdir, "tests", "scripts", "run_embedded_app.py")
    check_warning = subprocess.Popen(
        [test_env.python, embedded_py, pytestconfig.getoption("ansys_version")],
        stderr=subprocess.PIPE,
        env=test_env.env,
    )
    stdout, stderr = check_warning.communicate()

    # If UserWarning & pythonnet are in the stderr output, set warning to True.
    # Otherwise, set warning to False
    warning = True if "UserWarning" and "pythonnet" in stderr.decode() else False

    # Assert warning message appears for embedded app
    assert warning, "UserWarning should appear in the output of the script"


@pytest.mark.embedding
@pytest.mark.python_env
def test_private_appdata(pytestconfig, rootdir):
    """Test embedded instance does not save ShowTriad using a test-scoped Python environment."""

    version = pytestconfig.getoption("ansys_version")
    embedded_py = os.path.join(rootdir, "tests", "scripts", "run_embedded_app.py")

    from ansys.mechanical.core.run import _run
    stdout, stderr = _run([sys.executable, embedded_py, version, "True", "Set"], None)
    stdout, stderr = _run([sys.executable, embedded_py, version, "True", "Run"], None)
    assert "ShowTriad value is True" in stdout.decode()


@pytest.mark.embedding
@pytest.mark.python_env
def test_normal_appdata(pytestconfig, rootdir):
    """Test embedded instance saves ShowTriad value using a test-scoped Python environment."""
    version = pytestconfig.getoption("ansys_version")

    embedded_py = os.path.join(rootdir, "tests", "scripts", "run_embedded_app.py")

    # Set ShowTriad to False
    p1 = subprocess.Popen(
        [sys.executable, embedded_py, version, "False", "Set"], stdout=subprocess.PIPE
    )
    p1.communicate()

    # Check ShowTriad is False for regular embedded session
    p2 = subprocess.Popen(
        [sys.executable, embedded_py, version, "False", "Run"], stdout=subprocess.PIPE
    )
    stdout, stderr = p2.communicate()

    # Set ShowTriad back to True for regular embedded session
    p3 = subprocess.Popen(
        [sys.executable, embedded_py, version, "False", "Reset"], stdout=subprocess.PIPE
    )
    p3.communicate()

    # Assert ShowTriad was set to False for regular embedded session
    assert "ShowTriad value is False" in stdout.decode()


@pytest.mark.embedding
def test_rm_lockfile(embedded_app, tmp_path: pytest.TempPathFactory):
    """Test lock file is removed on close of embedded application."""
    mechdat_path = os.path.join(tmp_path, "test.mechdat")
    embedded_app.save(mechdat_path)
    embedded_app.close()

    lockfile_path = os.path.join(embedded_app.DataModel.Project.ProjectDirectory, ".mech_lock")
    # Assert lock file path does not exist
    assert not os.path.exists(lockfile_path)
