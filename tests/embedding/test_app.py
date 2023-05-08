"""Miscellaneous embedding tests"""
import os
import shutil
import subprocess
import sys
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
def test_warning_message():
    """Test pythonnet warning of the embedded instance."""
    venv_name = "pythonnetvenv"
    base = os.getcwd()

    if "win" in sys.platform:
        exe_dir = "Scripts"
    else:
        exe_dir = "bin"

    venv_bin = os.path.join(base, "." + venv_name, exe_dir)

    # Set up path to use the virtual environment
    original_path = os.environ["PATH"]
    os.environ["PATH"] = venv_bin + os.pathsep + os.environ.get("PATH", "")

    # Create virtual environment
    subprocess.run([sys.executable, "-m", "venv", "." + venv_name])

    # Upgrade pip
    print("Upgrading pip")
    upgrade_pip = subprocess.Popen(
        [os.path.join(venv_bin, "python"), "-m", "pip", "install", "-U", "pip"]
    )
    upgrade_pip.wait()

    # Install tests
    print("Installing tests")
    install_tests = subprocess.Popen([os.path.join(venv_bin, "pip"), "install", "-e", ".[tests]"])
    install_tests.wait()

    # Install pythonnet
    print("Installing pythonnet")
    install_pythonnet = subprocess.Popen([os.path.join(venv_bin, "pip"), "install", "pythonnet"])
    install_pythonnet.wait()

    # Run embedded instance in virtual env with pythonnet installed
    print("Running the embedded instance in a virtual environment")
    embedded_py = os.path.join(base, "tests", "scripts", "run_embedded_app.py")
    check_warning = subprocess.Popen(
        [os.path.join(venv_bin, "python"), embedded_py], stderr=subprocess.PIPE
    )
    check_warning.wait()
    stderr_output = check_warning.stderr.read().decode()

    # If UserWarning & pythonnet are in the stderr output, set warning to True.
    # Otherwise, set warning to False
    warning = True if "UserWarning" and "pythonnet" in stderr_output else False

    # Assert warning message appears for embedded app
    assert 1 == warning

    # Remove virtual environment
    venv_dir = os.path.join(base, "." + venv_name)
    shutil.rmtree(venv_dir)

    # Set PATH back to what it was originally
    os.environ["PATH"] = original_path
