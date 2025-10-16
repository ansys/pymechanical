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
"""Test for Mechanical Module."""
import json
from pathlib import Path
import re

import ansys.tools.path
import conftest
import pytest

import ansys.mechanical.core as pymechanical
import ansys.mechanical.core.errors as errors
import ansys.mechanical.core.misc as misc


def new_python_script_api(mechanical):
    """Check if the new python script API is available."""
    api_version = mechanical._get_python_script_api_version()
    return api_version > 0


@pytest.mark.remote_session_connect
def test_run_python_script_success(mechanical):
    """Test for running a python script successfully."""
    result = str(mechanical.run_python_script("2+3"))
    assert result == "5"


@pytest.mark.remote_session_connect
def test_run_python_script_success_return_empty(mechanical):
    """Test for running a python script that returns empty."""
    result = str(mechanical.run_python_script("ExtAPI.DataModel.Project"))
    if misc.is_windows() and not new_python_script_api(mechanical):
        assert result == ""
    else:
        assert result == "Ansys.ACT.Automation.Mechanical.Project"


@pytest.mark.remote_session_connect
def test_run_python_script_error(mechanical):
    """Test for running a python script that raises an error."""
    with pytest.raises(mechanical._error_type) as exc_info:
        mechanical.run_python_script("import test")

    # TODO : we can do custom error with currying poster
    if not new_python_script_api(mechanical):
        assert exc_info.value.details() == "No module named test"
    else:
        assert "No module named test" in str(exc_info.value)


@pytest.mark.remote_session_connect
def test_run_python_from_file_success(mechanical):
    """Test for running a python script from a file successfully."""
    current_working_directory = Path.cwd()
    script_path = current_working_directory / "tests" / "scripts" / "run_python_success.py"
    print("running python script : ", script_path)
    result = mechanical.run_python_script_from_file(str(script_path))

    assert result == "test"


@pytest.mark.remote_session_connect
def test_run_python_script_from_file_error(mechanical):
    """Test for running a python script from a file that raises an error."""
    with pytest.raises(mechanical._error_type) as exc_info:
        current_working_directory = Path.cwd()
        script_path = current_working_directory / "tests" / "scripts" / "run_python_error.py"
        print("running python script : ", script_path)
        mechanical.run_python_script_from_file(str(script_path))
    if not new_python_script_api(mechanical):
        assert exc_info.value.details() == "name 'get_myname' is not defined"
    else:
        assert "name 'get_myname' is not defined" in str(exc_info.value)


@pytest.mark.remote_session_connect
@pytest.mark.parametrize("file_name", [r"hsec.x_t"])
def test_upload(mechanical, file_name, assets):
    """Test for uploading a file."""
    directory = mechanical.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")
    print(directory)

    file_path = Path(assets) / file_name
    mechanical.upload(
        file_name=str(file_path), file_location_destination=directory, chunk_size=1024 * 1024
    )

    base_name = file_path.name
    combined_path = Path(directory) / base_name
    file_path_modified = str(combined_path).replace("\\", "\\\\")
    # we are working with iron python 2.7 on mechanical side
    # use python 2.7 style formatting
    # path = '%s' % file_path_modified
    script = 'import os\nos.path.exists("%s")' % file_path_modified
    print(script)
    result = mechanical.run_python_script(script)
    assert bool(result)


@pytest.mark.remote_session_connect
# we are using only a small test file
# change the chunk_size for that
# ideally this will be 64*1024, 1024*1024, etc.
@pytest.mark.parametrize("chunk_size", [10, 50, 100])
def test_upload_with_different_chunk_size(mechanical, chunk_size, assets):
    """Test for uploading a file with different chunk sizes."""
    file_path = Path(assets) / "hsec.x_t"
    directory = mechanical.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")
    mechanical.upload(
        file_name=str(file_path), file_location_destination=directory, chunk_size=chunk_size
    )


def get_solve_out_path(mechanical):
    """Get the path to the solve.out file."""
    solve_out_path = ""
    for file_path in mechanical.list_files():
        if file_path.find("solve.out") != -1:
            solve_out_path = file_path
            break

    return solve_out_path


def write_file_contents_to_console(path):
    """Write the contents of a file to the console."""
    path = Path(path)
    with path.open("rt") as file:
        for line in file:
            print(line, end="")


def disable_distributed_solve(mechanical):
    """Disable distributed solve."""
    script = (
        'ExtAPI.Application.SolveConfigurations["My Computer"].'
        "SolveProcessSettings.DistributeSolution = False"
    )
    mechanical.run_python_script(script)


def enable_distributed_solve(mechanical):
    """Enable distributed solve."""
    script = (
        'ExtAPI.Application.SolveConfigurations["My Computer"].'
        "SolveProcessSettings.DistributeSolution = True"
    )
    mechanical.run_python_script(script)


def solve_and_return_results(mechanical):
    """Solve the model and return the results."""
    current_working_directory = Path.cwd()
    file_path = current_working_directory / "tests" / "assets" / "hsec.x_t"

    mechanical.clear()
    directory = mechanical.project_directory
    mechanical.upload(
        file_name=str(file_path), file_location_destination=directory, chunk_size=1024 * 1024
    )

    python_script = current_working_directory / "tests" / "scripts" / "api.py"

    text_file = python_script.open("r")
    # read whole file to a string
    data = text_file.read()
    # close file
    text_file.close()

    file_path_string = "\n"

    # let us append the scripts to run
    func_to_call = """
import os
directory = ExtAPI.DataModel.Project.ProjectDirectory
file_path_modified=os.path.join(directory,'hsec.x_t')
attach_geometry(file_path_modified)
generate_mesh()
add_static_structural_analysis_bc_results()
solve_model()
return_total_deformation()
    """
    python_script = data + file_path_string + func_to_call

    result = mechanical.run_python_script(
        python_script, enable_logging=True, log_level="INFO", progress_interval=1000
    )

    # if solve fails, solve.out contains enough information
    solve_out_path = get_solve_out_path(mechanical)

    if solve_out_path != "":
        print(f"downloading {solve_out_path} from server")
        print(f"downloading to {current_working_directory}")
        solve_out_local_path_list = mechanical.download(
            solve_out_path, target_dir=str(current_working_directory)
        )
        solve_out_local_path = solve_out_local_path_list[0]
        print(solve_out_local_path)

        write_file_contents_to_console(solve_out_local_path)

        # done with solve.out - remove it
        Path(solve_out_local_path).unlink()

    return result


def verify_project_download(mechanical, tmpdir):
    """Verify that the project can be downloaded."""
    files = mechanical.list_files()
    number_of_files = len(files)

    print("files available: ")
    for file in files:
        print(file)
    assert number_of_files > 0

    # download the project
    project_directory = mechanical.project_directory
    print(f"project directory: {project_directory}")

    target_dir = Path(tmpdir) / "mechanical_project"
    # add a trailing path separator
    target_dir = target_dir / ""
    print(f"creating target directory {target_dir}")
    target_dir.mkdir(exist_ok=True)

    out_files = mechanical.download_project(target_dir=str(target_dir))
    print("downloaded files:")
    for file in out_files:
        print(file)
        file_path = Path(file)
        assert file_path.exists() and file_path.stat().st_size > 0

    files = mechanical.list_files()
    assert len(files) == len(out_files)

    target_dir = Path(tmpdir) / "mechanical_project2"
    # add a trailing path separator
    target_dir = target_dir / ""
    print(f"creating target directory {target_dir}")
    target_dir.mkdir(exist_ok=True)

    # project not saved.
    # no mechdb available.
    extensions = ["mechdb"]
    with pytest.raises(ValueError):
        mechanical.download_project(extensions=extensions, target_dir=str(target_dir))

    extensions = ["xml", "rst"]
    out_files = mechanical.download_project(extensions=extensions, target_dir=str(target_dir))
    print(f"downloaded files for extensions: {extensions}")
    for file in out_files:
        print(file)
        file_path = Path(file)
        assert file_path.exists() and file_path.stat().st_size > 0
        extension = file_path.suffix
        extension_without_dot = extension[1:]
        assert extension_without_dot in extensions


@pytest.mark.remote_session_connect
# @pytest.mark.wip
# @pytest.mark.skip(reason="avoid long running")
def test_upload_attach_mesh_solve_use_api_non_distributed_solve(mechanical, tmpdir):
    """Test for uploading, attaching mesh, solving using API with non-distributed solve."""
    # default is distributed solve
    # let's disable the distributed solve and then solve
    # enable the distributed solve back

    # this test could run under a container with 1 cpu
    # let us disable distributed solve
    disable_distributed_solve(mechanical)

    result = solve_and_return_results(mechanical)

    # revert back to distributed solve
    enable_distributed_solve(mechanical)

    dict_result = json.loads(result)

    min_value = float(dict_result["Minimum"].split(" ")[0])
    max_value = float(dict_result["Maximum"].split(" ")[0])
    avg_value = float(dict_result["Average"].split(" ")[0])

    print(f"min_value = {min_value} max_value = {max_value} avg_value = {avg_value}")

    result = mechanical.run_python_script("ExtAPI.DataModel.Project.Model.Analyses[0].ObjectState")
    if not new_python_script_api(mechanical):
        assert "5" == result
    else:
        assert "Solved" == str(result)

    verify_project_download(mechanical, tmpdir)


@pytest.mark.remote_session_connect
def test_upload_attach_mesh_solve_use_api_distributed_solve(mechanical, tmpdir):
    """Test for uploading, attaching mesh, solving using API with distributed solve."""
    result = solve_and_return_results(mechanical)

    dict_result = json.loads(result)

    min_value = float(dict_result["Minimum"].split(" ")[0])
    max_value = float(dict_result["Maximum"].split(" ")[0])
    avg_value = float(dict_result["Average"].split(" ")[0])

    print(f"min_value = {min_value} max_value = {max_value} avg_value = {avg_value}")

    result = mechanical.run_python_script("ExtAPI.DataModel.Project.Model.Analyses[0].ObjectState")
    if not new_python_script_api(mechanical):
        assert "5" == result
    else:
        assert "Solved" == str(result)

    verify_project_download(mechanical, tmpdir)


def verify_download(mechanical, tmpdir, file_name, chunk_size):
    """Verify downloading a file with different chunk sizes."""
    directory = mechanical.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")
    print(directory)

    current_working_directory = Path.cwd()
    file_path = current_working_directory / "tests" / "assets" / file_name
    mechanical.upload(
        file_name=str(file_path), file_location_destination=directory, chunk_size=1024 * 1024
    )

    print(f"using the temporary directory: {tmpdir}")
    file_path = Path(directory) / file_name
    local_directory = tmpdir.strpath

    # test with different download chunk_size
    local_path_list = mechanical.download(
        files=str(file_path), target_dir=local_directory, chunk_size=chunk_size
    )
    print("downloaded files:")
    for local_path in local_path_list:
        print(f" downloaded file: {local_path}")
        local_file = Path(local_path)
        assert local_file.exists() and local_file.stat().st_size > 0


@pytest.mark.remote_session_connect
@pytest.mark.parametrize("file_name", ["hsec.x_t"])
def test_download_file(mechanical, tmpdir, file_name):
    """Test for downloading a file."""
    verify_download(mechanical, tmpdir, file_name, 1024 * 1024)


@pytest.mark.remote_session_connect
# we are using only a small test file
# change the chunk_size for that
# ideally this will be 64*1024, 1024*1024, etc.
@pytest.mark.parametrize("chunk_size", [10, 50, 100])
def test_download_file_different_chunk_size1(mechanical, tmpdir, chunk_size):
    """Test for downloading a file with different chunk sizes."""
    file_name = "hsec.x_t"

    verify_download(mechanical, tmpdir, file_name, chunk_size)


@pytest.mark.remote_session_launch
def test_launch_meshing_mode(mechanical_meshing):
    """Test for launching in meshing mode."""
    result = mechanical_meshing.run_python_script("2+3")
    assert result == "5"


@pytest.mark.remote_session_launch
def test_launch_result_mode(mechanical_result):
    """Test for launching in result mode."""
    result = mechanical_result.run_python_script("2+3")
    assert result == "5"


@pytest.mark.remote_session_launch
def test_close_all_local_instances(tmpdir):
    """Test for closing all local instances."""
    list_ports = []
    mechanical = conftest.launch_mechanical_instance(cleanup_on_exit=False)
    print(mechanical.name)
    list_ports.append(mechanical._port)

    # connect to the launched instance
    mechanical2 = conftest.connect_to_mechanical_instance(mechanical._port, clear_on_connect=True)
    print(mechanical2.name)

    test_upload_attach_mesh_solve_use_api_non_distributed_solve(mechanical2, tmpdir)

    # use the settings and launch another Mechanical instance
    mechanical.launch(cleanup_on_exit=False)
    print(mechanical.name)
    list_ports.append(mechanical._port)

    pymechanical.close_all_local_instances(list_ports, use_thread=False)
    for value in list_ports:
        assert value not in pymechanical.LOCAL_PORTS


@pytest.mark.remote_session_launch
def test_find_mechanical_path():
    """Test for finding the Mechanical executable path."""
    if pymechanical.mechanical.get_start_instance():
        path = ansys.tools.path.get_mechanical_path()
        version = ansys.tools.path.version_from_path("mechanical", path)

        if misc.is_windows():
            assert "AnsysWBU.exe" in path
        else:
            assert ".workbench" in path

        assert re.match(r"\d{3}", str(version)) and version >= 241


@pytest.mark.remote_session_launch
def test_change_default_mechanical_path():
    """Test for changing the default Mechanical executable path."""
    if pymechanical.mechanical.get_start_instance():
        path = ansys.tools.path.get_mechanical_path()
        version = ansys.tools.path.version_from_path("mechanical", path)

        pymechanical.change_default_mechanical_path(path)

        path_new = ansys.tools.path.get_mechanical_path()
        version_new = ansys.tools.path.version_from_path("mechanical", path)

        assert path_new == path
        assert version_new == version


@pytest.mark.remote_session_launch
def test_version_from_path():
    """Test for getting version from path."""
    windows_path = "C:\\Program Files\\ANSYS Inc\\v251\\aisol\\bin\\winx64\\AnsysWBU.exe"
    version = ansys.tools.path.version_from_path("mechanical", windows_path)
    assert version == 251

    linux_path = "/usr/ansys_inc/v251/aisol/.workbench"
    version = ansys.tools.path.version_from_path("mechanical", linux_path)
    assert version == 251

    with pytest.raises(RuntimeError):
        # doesn't contain version
        path = "C:\\Program Files\\ANSYS Inc\\aisol\\bin\\winx64\\AnsysWBU.exe"
        ansys.tools.path.version_from_path("mechanical", path)


@pytest.mark.remote_session_launch
def test_valid_port():
    """Test for valid port."""
    # no error thrown when everything is ok.
    pymechanical.mechanical.check_valid_port(10000, 1000, 60000)

    with pytest.raises(ValueError):
        pymechanical.mechanical.check_valid_port("10000")

    with pytest.raises(ValueError):
        pymechanical.mechanical.check_valid_port(100, 1000, 60000)


@pytest.mark.remote_session_launch
def test_server_log_level():
    """Test for server log level conversion."""
    server_log_level = pymechanical.mechanical.Mechanical.convert_to_server_log_level("DEBUG")
    assert 1 == server_log_level

    server_log_level = pymechanical.mechanical.Mechanical.convert_to_server_log_level("INFO")
    assert 2 == server_log_level

    server_log_level = pymechanical.mechanical.Mechanical.convert_to_server_log_level("WARNING")
    assert 3 == server_log_level

    server_log_level = pymechanical.mechanical.Mechanical.convert_to_server_log_level("ERROR")
    assert 4 == server_log_level

    server_log_level = pymechanical.mechanical.Mechanical.convert_to_server_log_level("CRITICAL")
    assert 5 == server_log_level

    with pytest.raises(ValueError):
        pymechanical.mechanical.Mechanical.convert_to_server_log_level("NON_EXITING_LEVEL")


@pytest.mark.remote_session_launch
def test_launch_mechanical_non_existent_path():
    """Test for launching Mechanical with a non-existent path."""
    cwd = Path.cwd()

    if misc.is_windows():
        exec_file = cwd / "test" / "AnsysWBU.exe"
    else:
        exec_file = cwd / "test" / ".workbench"

    with pytest.raises(FileNotFoundError):
        pymechanical.launch_mechanical(exec_file=str(exec_file))


@pytest.mark.remote_session_launch
def test_launch_grpc_not_supported_version():
    """Test for launching grpc with not supported version."""
    cwd = Path.cwd()

    if misc.is_windows():
        exec_file = cwd / "ANSYS Inc" / "v230" / "aisol" / "bin" / "win64" / "AnsysWBU.exe"
    else:
        exec_file = cwd / "ansys_inc" / "v230" / "aisol" / ".workbench"

    with pytest.raises(errors.VersionError):
        pymechanical.mechanical.launch_grpc(exec_file=str(exec_file))
