"""Miscellaneous embedding tests"""
import os
import shutil
import subprocess
import tempfile

import pytest


@pytest.mark.embedding
def test_app_repr(embedded_app):
    """Test repr of the Application class."""
    app_repr_lines = repr(embedded_app).splitlines()
    assert app_repr_lines[0].startswith("Ansys Mechanical")
    assert app_repr_lines[1].startswith("Product Version")
    assert app_repr_lines[2].startswith("Software build date:")


@pytest.mark.embedding
def test_app_save_open(embedded_app):
    """Test save and open of the Application class."""
    import System
    import clr  # noqa: F401

    # save without a save_as throws an exception
    with pytest.raises(System.Exception):
        embedded_app.save()

    embedded_app.DataModel.Project.Name = "PROJECT 1"
    tmpname = tempfile.mktemp()
    project_file = f"{tmpname}.mechdat"
    project_files = f"{tmpname}_Mech_Files"
    embedded_app.save_as(project_file)
    try:
        embedded_app.new()
        embedded_app.open(project_file)
        assert embedded_app.DataModel.Project.Name == "PROJECT 1"
        embedded_app.DataModel.Project.Name = "PROJECT 2"
        embedded_app.save()
        embedded_app.new()
        embedded_app.open(project_file)
        assert embedded_app.DataModel.Project.Name == "PROJECT 2"
        embedded_app.new()
    except:
        # clean up the project files
        shutil.rmtree(project_files)
        os.remove(project_file)


@pytest.mark.embedding
def test_app_version(embedded_app):
    """Test version of the Application class."""
    version = embedded_app.version
    assert type(version) is int
    assert version >= 231


@pytest.mark.embedding
@pytest.mark.python_env
def test_warning_message(test_env, rootdir):
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
        [test_env.python, embedded_py],
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
def test_private_appdata(test_env, rootdir):
    """Test embedded instance does not save ShowTriad using a test-scoped Python environment."""

    # Install pymechanical
    subprocess.check_call(
        [test_env.python, "-m", "pip", "install", "-e", "."],
        cwd=rootdir,
        env=test_env.env,
    )

    embedded_py = os.path.join(rootdir, "tests", "scripts", "run_embedded_app.py")

    # Set ShowTriad to False
    set_showtriad = subprocess.Popen(
        [test_env.python, embedded_py, "True", "Set"],
        stdout=subprocess.PIPE,
        env=test_env.env,
    )
    set_showtriad.wait()

    # Check ShowTriad is True for private_appdata embedded sessions
    launch_private_app = subprocess.Popen(
        [test_env.python, embedded_py, "True", "Run"],
        stdout=subprocess.PIPE,
        env=test_env.env,
    )
    launch_private_app.wait()
    stdout = launch_private_app.stdout.read().decode().strip("\n").strip("\r")

    assert stdout == "True"


@pytest.mark.embedding
@pytest.mark.python_env
def test_normal_appdata(test_env, rootdir):
    """Test embedded instance saves ShowTriad value using a test-scoped Python environment."""

    # Install pymechanical
    subprocess.check_call(
        [test_env.python, "-m", "pip", "install", "-e", "."],
        cwd=rootdir,
        env=test_env.env,
    )

    embedded_py = os.path.join(rootdir, "tests", "scripts", "run_embedded_app.py")

    # Set ShowTriad to False
    set_showtriad = subprocess.Popen(
        [test_env.python, embedded_py, "False", "Set"],
        stdout=subprocess.PIPE,
        env=test_env.env,
    )
    set_showtriad.wait()

    # Check ShowTriad is False for regular embedded session
    launch_app = subprocess.Popen(
        [test_env.python, embedded_py, "False", "Run"],
        stdout=subprocess.PIPE,
        env=test_env.env,
    )
    launch_app.wait()
    stdout = launch_app.stdout.read().decode().strip("\n").strip("\r")

    # Set ShowTriad back to True for regular embedded session
    reset_showtriad = subprocess.Popen(
        [test_env.python, embedded_py, "False", "Reset"],
        stdout=subprocess.PIPE,
        env=test_env.env,
    )
    reset_showtriad.wait()

    # Assert ShowTriad was set to False for regular embedded session
    assert stdout == "False"
