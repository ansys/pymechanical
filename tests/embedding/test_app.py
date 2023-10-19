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
    check_warning.wait()
    stderr = check_warning.stderr.read().decode()

    # If UserWarning & pythonnet are in the stderr output, set warning to True.
    # Otherwise, set warning to False
    warning = True if "UserWarning" and "pythonnet" in stderr else False

    # Assert warning message appears for embedded app
    assert warning, "UserWarning should appear in the output of the script"


@pytest.mark.embedding
@pytest.mark.python_env
def test_private_appdata(pytestconfig, rootdir):
    """Test embedded instance does not save ShowTriad using a test-scoped Python environment."""

    version = pytestconfig.getoption("ansys_version")
    embedded_py = os.path.join(rootdir, "tests", "scripts", "run_embedded_app.py")

    # Set ShowTriad to False
    p1 = subprocess.Popen(
        [sys.executable, embedded_py, version, "True", "Set"], stdout=subprocess.PIPE
    )
    p1.wait()

    # Check ShowTriad is True for private_appdata embedded sessions
    p2 = subprocess.Popen(
        [sys.executable, embedded_py, version, "True", "Run"], stdout=subprocess.PIPE
    )
    p2.wait()
    stdout = p2.stdout.read().decode()

    assert "ShowTriad value is True" in stdout


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
    p1.wait()

    # Check ShowTriad is False for regular embedded session
    p2 = subprocess.Popen(
        [sys.executable, embedded_py, version, "False", "Run"], stdout=subprocess.PIPE
    )
    p2.wait()
    stdout = p2.stdout.read().decode()

    # Set ShowTriad back to True for regular embedded session
    p3 = subprocess.Popen(
        [sys.executable, embedded_py, version, "False", "Reset"], stdout=subprocess.PIPE
    )
    p3.wait()

    # Assert ShowTriad was set to False for regular embedded session
    assert "ShowTriad value is False" in stdout


@pytest.mark.embedding
def test_rm_lockfile(embedded_app, tmp_path: pytest.TempPathFactory):
    """Test lock file is removed on close of embedded application."""
    mechdat_path = os.path.join(tmp_path, "test.mechdat")
    embedded_app.save(mechdat_path)
    embedded_app.close()

    lockfile_path = os.path.join(embedded_app.DataModel.Project.ProjectDirectory, ".mech_lock")
    # Assert lock file path does not exist
    assert not os.path.exists(lockfile_path)


def mechanical_env_helper(revn, cmd):
    """Helper function for mechanical-env tests."""
    # Get environment before running mechanical-env
    start_env = os.environ

    subproc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subproc.wait()
    stdout = subproc.stdout.read().decode()
    stderr = subproc.stderr.read().decode()

    # Get environment after running mechanical-env
    end_env = os.environ

    # Assert the environment did not change
    assert start_env == end_env

    return stdout, stderr


@pytest.mark.mechanical_env
def test_maintain_env(pytestconfig, rootdir):
    """Ensure the environment does not change when running ``mechanical-env``."""
    # Set version variable and get print_instance.py path
    version = pytestconfig.getoption("ansys_version")
    embedded_py = os.path.join(rootdir, "tests", "scripts", "print_instance.py")
    cmd = ["mechanical-env", "python", embedded_py, version]

    stdout, stderr = mechanical_env_helper(version, cmd)

    # Assert embedded app output was printed
    assert "Ansys Mechanical [Ansys Mechanical Enterprise]" in stdout


@pytest.mark.mechanical_env
def test_nonzero_retcode(rootdir):
    """Non-zero return code is raised in mechanical-env."""
    # Set version variable and get print_instance.py path
    version = "212"
    embedded_py = os.path.join(rootdir, "tests", "scripts", "print_instance.py")
    cmd = ["mechanical-env", "python", embedded_py, version]

    stdout, stderr = mechanical_env_helper(version, cmd)

    # Assert KeyError and ValueError exist
    assert "KeyError: 'AWP_ROOT212'" in stderr


@pytest.mark.mechanical_env
def test_user_revn(pytestconfig, rootdir):
    """Test user selected revision number is used in mechanical-env."""
    # Set version variable and get print_instance.py
    version = "232"
    embedded_py = os.path.join(rootdir, "tests", "scripts", "print_instance.py")
    cmd = ["mechanical-env", f"--revision={version}", "python", embedded_py, version]

    stdout, stderr = mechanical_env_helper(version, cmd)

    if stderr and (version != pytestconfig.getoption("ansys_version")):
        assert f"KeyError: {version}" in stderr
    else:
        assert "Ansys Mechanical [Ansys Mechanical Enterprise]" in stdout
