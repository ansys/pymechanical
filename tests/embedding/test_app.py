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

"""Miscellaneous embedding tests"""
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import NamedTemporaryFile
import time

import pytest

from ansys.mechanical.core.embedding.app import is_initialized
from ansys.mechanical.core.embedding.cleanup_gui import cleanup_gui
from ansys.mechanical.core.embedding.ui import _launch_ui
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
    harmonic_acoustic = embedded_app.Model.AddHarmonicAcousticAnalysis()
    with pytest.warns(UserWarning):
        harmonic_acoustic.SystemID
    with pytest.warns(UserWarning):
        harmonic_acoustic.AnalysisSettings.MultipleRPMs = True


@pytest.mark.embedding
def test_app_save_open(embedded_app, tmp_path: pytest.TempPathFactory):
    """Test save and open of the Application class."""
    import System
    import clr  # noqa: F401

    # save without a save_as throws an exception
    with pytest.raises(System.Exception):
        embedded_app.save()

    embedded_app.DataModel.Project.Name = "PROJECT 1"
    project_file = os.path.join(tmp_path, f"{NamedTemporaryFile().name}.mechdat")
    embedded_app.save_as(project_file)

    project_file_directory = os.path.splitext(project_file)[0] + "_Mech_Files"
    assert project_file_directory == os.path.normpath(embedded_app.project_directory)

    with pytest.raises(Exception):
        embedded_app.save_as(project_file)
    embedded_app.save_as(project_file, overwrite=True)
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
def test_app_update_globals_after_open(embedded_app, assets):
    """Test save and open of the Application class."""
    embedded_app.update_globals(globals())
    # unless the global "Model" has been redirected to point to the new model from the project file
    # this will throw an exception
    embedded_app.new()
    embedded_app.open(os.path.join(assets, "cube-hole.mechdb"))
    Model.AddNamedSelection()


@pytest.mark.embedding
def test_explicit_interface(embedded_app):
    """Test save and open of the Application class."""
    embedded_app.update_globals(globals())
    try:
        namedselection = Model.AddNamedSelection()
        ids = list(namedselection.Ids)
        assert len(ids) == 0, f"Expected an empty Ids list, but got {ids}."
    except AttributeError as e:
        pytest.fail(
            f"{str(e)}. This might be related to pythonnet."
            "Uninstall pythonnet and install ansys-pythonnet."
        )


@pytest.mark.embedding
def test_app_version(embedded_app):
    """Test version of the Application class."""
    version = embedded_app.version
    assert type(version) is int
    assert version >= 232


@pytest.mark.embedding
def test_nonblock_sleep(embedded_app):
    """Test non-blocking sleep."""
    t1 = time.time()
    utils.sleep(1000)
    t2 = time.time()
    assert (t2 - t1) >= 1


@pytest.mark.embedding
def test_app_print_tree(embedded_app, capsys, assets):
    """Test printing hierarchical tree of Mechanical ExtAPI object"""
    embedded_app.update_globals(globals())
    geometry_file = os.path.join(assets, "Eng157.x_t")
    geometry_import = Model.GeometryImportGroup.AddGeometryImport()
    geometry_import.Import(geometry_file)
    allbodies = Model.GetChildren(DataModelObjectCategory.Body, True)
    allbodies[0].Suppressed = True
    embedded_app.print_tree()
    captured = capsys.readouterr()
    printed_output = captured.out.strip()
    assert "Project" in printed_output
    assert "Suppressed" in printed_output

    embedded_app.print_tree(max_lines=2)
    captured = capsys.readouterr()
    printed_output = captured.out.strip()
    assert "Model" in printed_output
    assert "truncating after" in printed_output

    with pytest.raises(AttributeError):
        embedded_app.print_tree(DataModel)

    Modal = Model.AddModalAnalysis()
    Modal.Solution.Solve(True)
    embedded_app.print_tree()
    captured = capsys.readouterr()
    printed_output = captured.out.strip()
    assert all(symbol in printed_output for symbol in ["?", "⚡︎", "✕", "✓"])


@pytest.mark.embedding
def test_app_poster(embedded_app, printer):
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

    name = []
    error = []

    def change_name_async(poster):
        """Change_name_async will run a background thread

        It will change the name of the project to "foo"
        """
        printer("change_name_async")

        def get_name():
            return embedded_app.DataModel.Project.Name

        def change_name():
            embedded_app.DataModel.Project.Name = "foo"

        def raise_ex():
            raise Exception("TestException")

        name.append(poster.post(get_name))
        printer("get_name")
        poster.post(change_name)
        printer("change_name")

        try:
            poster.try_post(raise_ex)
        except Exception as e:
            error.append(e)
        printer("raise_ex")

        name.append(poster.try_post(get_name))
        printer("get_name")

    import threading

    change_name_thread = threading.Thread(target=change_name_async, args=(poster,))
    change_name_thread.start()

    # The poster can't do anything unless the main thread is receiving
    # messages. The `sleep` utility puts Mechanical's main thread to
    # idle and only execute actions that have been posted to its main
    # thread, e.g. `change_name` that was posted by the poster.
    while True:
        utils.sleep(40)
        if not change_name_thread.is_alive():
            break
    change_name_thread.join()
    assert len(name) == 2
    assert name[0] == "Project"
    assert name[1] == "foo"
    assert embedded_app.DataModel.Project.Name == "foo"
    assert len(error) == 1
    assert str(error[0]) == "TestException"


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


@pytest.mark.embedding_scripts
@pytest.mark.python_env
def test_warning_message(test_env, pytestconfig, run_subprocess, rootdir):
    """Test Python.NET warning of the embedded instance using a test-scoped Python environment."""

    # set these to None to see output in the terminal
    stdout = subprocess.DEVNULL
    stderr = subprocess.DEVNULL

    # Install pymechanical
    subprocess.check_call(
        [test_env.python, "-m", "pip", "install", "-e", "."],
        cwd=rootdir,
        env=test_env.env,
        stdout=stdout,
        stderr=stderr
    )

    # Install pythonnet
    subprocess.check_call(
        [test_env.python, "-m", "pip", "install", "pythonnet"],
        env=test_env.env,
        stdout = stdout,
        stderr = stderr
    )

    # Initialize with pythonnet
    embedded_pythonnet_py = os.path.join(rootdir, "tests", "scripts", "pythonnet_warning.py")
    process, stdout, stderr = run_subprocess(
        [test_env.python, embedded_pythonnet_py, pytestconfig.getoption("ansys_version")]
    )

    # If UserWarning & pythonnet are in the stderr output, set warning to True.
    # Otherwise, set warning to False
    warning = True if "UserWarning" and "pythonnet" in stderr.decode() else False

    # # Assert warning message appears for embedded app
    assert warning, "UserWarning should appear in the output of the script"


@pytest.mark.embedding_scripts
def test_building_gallery(pytestconfig, run_subprocess, rootdir):
    """Test for building gallery check.

    When building the gallery, each example file creates another instance of the app.
    When the BUILDING_GALLERY flag is enabled, only one instance is kept.
    This is to test the bug fixed in https://github.com/ansys/pymechanical/pull/784
    and will fail on PyMechanical version 0.11.0
    """
    version = pytestconfig.getoption("ansys_version")

    embedded_gallery_py = os.path.join(rootdir, "tests", "scripts", "build_gallery_test.py")

    process, stdout, stderr = run_subprocess(
        [sys.executable, embedded_gallery_py, version, "False"], None, False
    )
    stderr = stderr.decode()

    # Assert Exception
    assert "Cannot have more than one embedded mechanical instance" in stderr

    process, stdout, stderr = run_subprocess([sys.executable, embedded_gallery_py, version, "True"])
    stdout = stdout.decode()

    # Assert stdout after launching multiple instances
    assert "Multiple App launched with building gallery flag on" in stdout


@pytest.mark.embedding
def test_shims_import_material(embedded_app, assets):
    """Test deprecation warning for shims import material."""
    from ansys.mechanical.core.embedding import shims

    embedded_app.update_globals(globals())
    material_file = os.path.join(assets, "eng200_material.xml")
    with pytest.warns(DeprecationWarning):
        shims.import_materials(embedded_app, material_file)


@pytest.mark.embedding
def test_rm_lockfile(embedded_app, tmp_path: pytest.TempPathFactory):
    """Test lock file is removed on close of embedded application."""
    mechdat_path = os.path.join(tmp_path, "test.mechdat")
    embedded_app.save(mechdat_path)
    embedded_app.close()

    lockfile_path = os.path.join(embedded_app.project_directory, ".mech_lock")
    # Assert lock file path does not exist
    assert not os.path.exists(lockfile_path)


@pytest.mark.embedding
def test_app_execute_script(embedded_app):
    """Test execute_script method."""
    embedded_app.update_globals(globals())
    result = embedded_app.execute_script("2+3")
    assert result == 5
    with pytest.raises(Exception):
        # This will throw an exception since no module named test available
        embedded_app.execute_script("import test")


@pytest.mark.embedding
def test_launch_ui(embedded_app, tmp_path: pytest.TempPathFactory):
    """Test the _launch_ui function with a mock launcher."""

    class MockLauncher:
        """Mock Launcher to test launch_gui functionality."""

        def __init__(self):
            """Initialize the MockLauncher class."""
            self.ops = []

        def save_original(self, app):
            """Save the active mechdb file."""
            self.ops.append("save")

        def save_temp_copy(self, app):
            """Save a new mechdb file with a temporary name."""
            # Identify the mechdb of the saved session from save_original()
            self.ops.append("get_saved_session")

            # Get name of NamedTemporaryFile
            self.ops.append("get_name_temp_file")

            # Save app with name of temporary file
            self.ops.append("save_as")

            return "", ""

        def open_original(self, app, mechdb_file):
            """Open the original mechdb file from save_original()."""
            self.ops.append("open_orig_mechdb")

        def graphically_launch_temp(self, app, temp_file):
            """Launch the GUI for the mechdb file with a temporary name from save_temp_copy()."""
            self.ops.append("launch_temp_mechdb")

            return []

    # Create an instance of the MockLauncher object
    m = MockLauncher()

    # Check that _launch_ui raises an Exception when it hasn't been saved yet
    with pytest.raises(Exception):
        _launch_ui(embedded_app, m)

    mechdb_path = os.path.join(tmp_path, "test.mechdb")
    # Save a test.mechdb file
    embedded_app.save(mechdb_path)
    # Launch the UI with the mock class
    _launch_ui(embedded_app, False, m)
    # Close the embedded_app
    embedded_app.close()

    assert m.ops[0] == "save"
    assert m.ops[1] == "get_saved_session"
    assert m.ops[2] == "get_name_temp_file"
    assert m.ops[3] == "save_as"
    assert m.ops[4] == "open_orig_mechdb"
    assert m.ops[5] == "launch_temp_mechdb"


@pytest.mark.embedding
def test_launch_gui(embedded_app, tmp_path: pytest.TempPathFactory, capfd):
    """Test the GUI is launched for an embedded app."""
    mechdb_path = os.path.join(tmp_path, "test.mechdb")
    embedded_app.save(mechdb_path)
    embedded_app.launch_gui(delete_tmp_on_close=False, dry_run=True)
    embedded_app.close()
    out, err = capfd.readouterr()
    assert f"ansys-mechanical --project-file" in out
    assert f"--graphical --revision {str(embedded_app.version)}" in out
    assert f"Opened a new mechanical session based on {mechdb_path}" in out


@pytest.mark.embedding
def test_launch_gui_exception(embedded_app):
    """Test an exception is raised when the embedded_app has not been saved yet."""
    # Assert that an exception is raised
    with pytest.raises(Exception):
        embedded_app.launch_gui(delete_tmp_on_close=False)
    embedded_app.close()


@pytest.mark.embedding_scripts
def test_tempfile_cleanup(tmp_path: pytest.TempPathFactory):
    """Test cleanup function to remove the temporary mechdb file and folder."""
    assert os.path.isdir(tmp_path)
    temp_file = tmp_path / "tempfiletest.mechdb"
    temp_folder = tmp_path / "tempfiletest_Mech_Files"

    # Make temporary file
    temp_file.touch()
    # Make temporary folder
    temp_folder.mkdir()

    # Assert the file and folder exist
    assert temp_file.exists()
    assert temp_folder.exists()

    # Run process
    if os.name == "nt":
        process = subprocess.Popen(["ping", "127.0.0.1", "-n", "2"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    else:
        process = subprocess.check_call(["sleep", "3"])

    pid = process.pid
    assert process.wait() == 0

    # Remove the temporary file and folder
    cleanup_gui(pid, temp_file)

    # Assert the file and folder do not exist
    assert not temp_file.exists()
    assert not temp_folder.exists()


@pytest.mark.embedding_scripts
def test_attribute_error(tmp_path: pytest.TempPathFactory, pytestconfig, rootdir):
    """Test cleanup function to remove the temporary mechdb file and folder."""
    # Change directory to tmp_path
    os.chdir(tmp_path)

    # Get the version
    version = pytestconfig.getoption("ansys_version")

    # Create the Ansys folder in tmp_path and assert it exists
    temp_folder = tmp_path / "Ansys"
    temp_folder.mkdir()
    assert temp_folder.exists()

    # Copy the run_embedded_app.py script to tmp_path
    embedded_py = os.path.join(rootdir, "tests", "scripts", "run_embedded_app.py")
    tmp_file_script = tmp_path / "run_embedded_app.py"
    shutil.copyfile(embedded_py, tmp_file_script)

    # Run the script and assert the AttributeError is raised
    stdout, stderr = subprocess.Popen(
        [sys.executable, tmp_file_script, "--version", version],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).communicate()

    # Assert the AttributeError is raised
    assert "Unable to resolve Mechanical assemblies." in stderr.decode()

    os.chdir(rootdir)


@pytest.mark.embedding
def test_app_execute_script_from_file(embedded_app, rootdir, printer):
    """Test execute_script_from_file method."""
    embedded_app.update_globals(globals())

    printer("Running run_python_error.py")
    error_script_path = os.path.join(rootdir, "tests", "scripts", "run_python_error.py")
    with pytest.raises(Exception) as exc_info:
        # This will throw an exception since no module named test available
        embedded_app.execute_script_from_file(error_script_path)
    assert "name 'get_myname' is not defined" in str(exc_info.value)

    printer("Running run_python_success.py")
    succes_script_path = os.path.join(rootdir, "tests", "scripts", "run_python_success.py")
    result = embedded_app.execute_script_from_file(succes_script_path)
    assert result == "test"


@pytest.mark.embedding
def test_app_lock_file_open(embedded_app, tmp_path: pytest.TempPathFactory):
    """Test the lock file is removed on open if remove_lock=True."""
    embedded_app.DataModel.Project.Name = "PROJECT 1"
    project_file = os.path.join(tmp_path, f"{NamedTemporaryFile().name}.mechdat")
    embedded_app.save_as(project_file)
    with pytest.raises(Exception):
        embedded_app.save_as(project_file)
    embedded_app.save_as(project_file, overwrite=True)

    lock_file = Path(embedded_app.project_directory) / ".mech_lock"

    # Assert the lock file exists after saving it
    assert lock_file.exists()

    # Assert a warning is emitted if the lock file is going to be removed
    with pytest.warns(UserWarning):
        embedded_app.open(project_file, remove_lock=True)


@pytest.mark.embedding
def test_app_initialized(embedded_app):
    """Test the app is initialized."""
    assert is_initialized()


@pytest.mark.embedding
def test_app_not_initialized(run_subprocess, pytestconfig, rootdir):
    """Test the app is not initialized."""
    version = pytestconfig.getoption("ansys_version")
    embedded_py = os.path.join(rootdir, "tests", "scripts", "run_embedded_app.py")

    process, stdout, stderr = run_subprocess(
        [
            sys.executable,
            embedded_py,
            "--version",
            version,
            "--test_not_initialized",
        ]
    )
    stdout = stdout.decode()

    assert "The app is not initialized" in stdout
