import json
import os
import pathlib
import re
import subprocess
import sys

import grpc
import pytest

import ansys.mechanical.core as pymechanical
import ansys.mechanical.core.errors as errors
import ansys.mechanical.core.misc as misc
import conftest


@pytest.mark.remote_session_connect
def test_run_python_script_success(mechanical):
    result = mechanical.run_python_script("2+3")
    assert result == "5"


@pytest.mark.remote_session_connect
def test_run_python_script_success_return_empty(mechanical):
    result = mechanical.run_python_script("ExtAPI.DataModel.Project")
    if misc.is_windows():
        assert result == ""
    else:
        assert result == "Ansys.ACT.Automation.Mechanical.Project"


@pytest.mark.remote_session_connect
def test_run_python_script_error(mechanical):
    with pytest.raises(grpc.RpcError) as exc_info:
        mechanical.run_python_script("import test")

    assert exc_info.value.details() == "No module named test"


@pytest.mark.remote_session_connect
def test_run_python_from_file_success(mechanical):
    current_working_directory = os.getcwd()
    script_path = os.path.join(
        current_working_directory, "tests", "scripts", "run_python_success.py"
    )
    print("running python script : ", script_path)
    result = mechanical.run_python_script_from_file(script_path)

    assert result == "test"


# @pytest.mark.remote_session_connect
# def test_run_python_from_file_log_messages(mechanical):
#     current_working_directory = os.getcwd()
#     script_path = os.path.join(current_working_directory, "tests", "scripts", "log_message.py")
#     print("running python script : ", script_path)
#
#     print("logging_not enabled")
#     result = mechanical.run_python_script_from_file(script_path)
#
#     print("logging_enabled")
#     result = mechanical.run_python_script_from_file(
#         script_path, enable_logging=True, log_level="DEBUG", progress_interval=1000
#     )
#
#     result = mechanical.run_python_script_from_file(
#         script_path, enable_logging=True, log_level="INFO", progress_interval=1000
#     )
#
#     result = mechanical.run_python_script_from_file(
#         script_path, enable_logging=True, log_level="WARNING", progress_interval=1000
#     )
#
#     result = mechanical.run_python_script_from_file(
#         script_path, enable_logging=True, log_level="ERROR", progress_interval=1000
#     )
#
#     result = mechanical.run_python_script_from_file(
#         script_path, enable_logging=True, log_level="CRITICAL", progress_interval=1000
#     )
#
#     assert result == "log_test"


@pytest.mark.remote_session_connect
def test_run_python_script_from_file_error(mechanical):
    with pytest.raises(grpc.RpcError) as exc_info:
        current_working_directory = os.getcwd()
        script_path = os.path.join(
            current_working_directory, "tests", "scripts", "run_python_error.py"
        )
        print("running python script : ", script_path)
        mechanical.run_python_script_from_file(script_path)

    assert exc_info.value.details() == "name 'get_myname' is not defined"


@pytest.mark.remote_session_connect
@pytest.mark.parametrize("file_name", [r"hsec.x_t"])
def test_upload(mechanical, file_name):
    mechanical.run_python_script("ExtAPI.DataModel.Project.New()")
    directory = mechanical.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")
    print(directory)

    current_working_directory = os.getcwd()
    file_path = os.path.join(current_working_directory, "tests", "parts", file_name)
    mechanical.upload(
        file_name=file_path, file_location_destination=directory, chunk_size=1024 * 1024
    )

    base_name = os.path.basename(file_path)
    combined_path = os.path.join(directory, base_name)
    file_path_modified = combined_path.replace("\\", "\\\\")
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
def test_upload_with_different_chunk_size(mechanical, chunk_size):
    current_working_directory = os.getcwd()
    file_path = os.path.join(current_working_directory, "tests", "parts", "hsec.x_t")
    mechanical.run_python_script("ExtAPI.DataModel.Project.New()")
    directory = mechanical.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")
    mechanical.upload(
        file_name=file_path, file_location_destination=directory, chunk_size=chunk_size
    )


def get_solve_out_path(mechanical):
    solve_out_path = ""
    for file_path in mechanical.list_files():
        if file_path.find("solve.out") != -1:
            solve_out_path = file_path
            break

    return solve_out_path


def write_file_contents_to_console(path):
    with open(path, "rt") as file:
        for line in file:
            print(line, end="")


def disable_distributed_solve(mechanical):
    script = (
        'ExtAPI.Application.SolveConfigurations["My Computer"].'
        "SolveProcessSettings.DistributeSolution = False"
    )
    mechanical.run_python_script(script)


def enable_distributed_solve(mechanical):
    script = (
        'ExtAPI.Application.SolveConfigurations["My Computer"].'
        "SolveProcessSettings.DistributeSolution = True"
    )
    mechanical.run_python_script(script)


def solve_and_return_results(mechanical):
    current_working_directory = os.getcwd()
    file_path = os.path.join(current_working_directory, "tests", "parts", "hsec.x_t")

    mechanical.clear()
    directory = mechanical.project_directory
    mechanical.upload(
        file_name=file_path, file_location_destination=directory, chunk_size=1024 * 1024
    )

    python_script = os.path.join(current_working_directory, "tests", "scripts", "api.py")

    text_file = open(python_script, "r")
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
            solve_out_path, target_dir=current_working_directory
        )
        solve_out_local_path = solve_out_local_path_list[0]
        print(solve_out_local_path)

        write_file_contents_to_console(solve_out_local_path)

        # done with solve.out - remove it
        os.remove(solve_out_local_path)

    return result


def verify_project_download(mechanical, tmpdir):
    files = mechanical.list_files()
    number_of_files = len(files)

    print("files available: ")
    for file in files:
        print(file)
    assert number_of_files > 0

    # download the project
    project_directory = mechanical.project_directory
    print(f"project directory: {project_directory}")

    target_dir = os.path.join(tmpdir, "mechanical_project")
    # add a trailing path separator
    target_dir = os.path.join(target_dir, "")
    print(f"creating target directory {target_dir}")
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    out_files = mechanical.download_project(target_dir=target_dir)
    print("downloaded files:")
    for file in out_files:
        print(file)
        assert os.path.exists(file) and os.path.getsize(file) > 0

    files = mechanical.list_files()
    assert len(files) == len(out_files)

    target_dir = os.path.join(tmpdir, "mechanical_project2")
    # add a trailing path separator
    target_dir = os.path.join(target_dir, "")
    print(f"creating target directory {target_dir}")
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    # project not saved.
    # no mechdb available.
    extensions = ["mechdb"]
    with pytest.raises(ValueError):
        mechanical.download_project(extensions=extensions, target_dir=target_dir)

    extensions = ["xml", "rst"]
    out_files = mechanical.download_project(extensions=extensions, target_dir=target_dir)
    print(f"downloaded files for extensions: {extensions}")
    for file in out_files:
        print(file)
        assert os.path.exists(file) and os.path.getsize(file) > 0
        extension = pathlib.Path(file).suffix
        extension_without_dot = extension[1:]
        assert extension_without_dot in extensions


@pytest.mark.remote_session_connect
# @pytest.mark.wip
# @pytest.mark.skip(reason="avoid long running")
def test_upload_attach_mesh_solve_use_api_non_distributed_solve(mechanical, tmpdir):
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
    assert "5" == result.lower()

    verify_project_download(mechanical, tmpdir)


@pytest.mark.remote_session_connect
def test_upload_attach_mesh_solve_use_api_distributed_solve(mechanical, tmpdir):
    # default is distributed solve

    result = solve_and_return_results(mechanical)

    dict_result = json.loads(result)

    min_value = float(dict_result["Minimum"].split(" ")[0])
    max_value = float(dict_result["Maximum"].split(" ")[0])
    avg_value = float(dict_result["Average"].split(" ")[0])

    print(f"min_value = {min_value} max_value = {max_value} avg_value = {avg_value}")

    result = mechanical.run_python_script("ExtAPI.DataModel.Project.Model.Analyses[0].ObjectState")
    assert "5" == result.lower()

    verify_project_download(mechanical, tmpdir)


def verify_download(mechanical, tmpdir, file_name, chunk_size):
    directory = mechanical.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")
    print(directory)

    current_working_directory = os.getcwd()
    file_path = os.path.join(current_working_directory, "tests", "parts", file_name)
    mechanical.upload(
        file_name=file_path, file_location_destination=directory, chunk_size=1024 * 1024
    )

    print(f"using the temporary directory: {tmpdir}")
    file_path = os.path.join(directory, file_name)
    local_directory = tmpdir.strpath

    # test with different download chunk_size
    local_path_list = mechanical.download(
        files=file_path, target_dir=local_directory, chunk_size=chunk_size
    )
    print("downloaded files:")
    for local_path in local_path_list:
        print(f" downloaded file: {local_path}")
        assert os.path.exists(local_path) and os.path.getsize(local_path) > 0


@pytest.mark.remote_session_connect
# @pytest.mark.wip
@pytest.mark.parametrize("file_name", ["hsec.x_t"])
def test_download_file(mechanical, tmpdir, file_name):
    verify_download(mechanical, tmpdir, file_name, 1024 * 1024)


@pytest.mark.remote_session_connect
# we are using only a small test file
# change the chunk_size for that
# ideally this will be 64*1024, 1024*1024, etc.
@pytest.mark.parametrize("chunk_size", [10, 50, 100])
def test_download_file_different_chunk_size1(mechanical, tmpdir, chunk_size):
    file_name = "hsec.x_t"

    verify_download(mechanical, tmpdir, file_name, chunk_size)


@pytest.mark.remote_session_launch
def test_launch_meshing_mode(mechanical_meshing):
    result = mechanical_meshing.run_python_script("2+3")
    assert result == "5"


@pytest.mark.remote_session_launch
def test_launch_result_mode(mechanical_result):
    result = mechanical_result.run_python_script("2+3")
    assert result == "5"


@pytest.mark.remote_session_launch
def test_close_all_Local_instances(tmpdir):
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
def test_launch_result_mode(mechanical_result):
    result = mechanical_result.run_python_script("2+3")
    assert result == "5"


@pytest.mark.remote_session_launch
def test_find_mechanical_path():
    if pymechanical.mechanical.get_start_instance():
        path, version = pymechanical.find_mechanical()

        if misc.is_windows():
            assert "AnsysWBU.exe" in path
        else:
            assert ".workbench" in path

        assert re.match(r"\d\d\.\d", str(version))


@pytest.mark.remote_session_launch
def test_change_default_mechanical_path():
    if pymechanical.mechanical.get_start_instance():
        path, version = pymechanical.find_mechanical()

        pymechanical.change_default_mechanical_path(path)

        path_new, version_new = pymechanical.find_mechanical()

        assert path_new == path
        assert version_new == version


@pytest.mark.remote_session_launch
def test_version_from_path():
    windows_path = "C:\\Program Files\\ANSYS Inc\\v231\\aisol\\bin\\winx64\\AnsysWBU.exe"
    version = pymechanical.mechanical._version_from_path(windows_path)
    assert version == 231

    linux_path = "/usr/ansys_inc/v231/aisol/.workbench"
    version = pymechanical.mechanical._version_from_path(linux_path)
    assert version == 231

    with pytest.raises(RuntimeError):
        # doesn't contain version
        path = "C:\\Program Files\\ANSYS Inc\\aisol\\bin\\winx64\\AnsysWBU.exe"
        pymechanical.mechanical._version_from_path(path)


@pytest.mark.remote_session_launch
def test_valid_port():
    # no error thrown when everything is ok.
    pymechanical.mechanical.check_valid_port(10000, 1000, 60000)

    with pytest.raises(ValueError):
        pymechanical.mechanical.check_valid_port("10000")

    with pytest.raises(ValueError):
        pymechanical.mechanical.check_valid_port(100, 1000, 60000)


@pytest.mark.remote_session_launch
def test_server_log_level():
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
    cwd = os.getcwd()

    if misc.is_windows():
        exec_file = os.path.join(cwd, "test", "AnsysWBU.exe")
    else:
        exec_file = os.path.join(cwd, "test", ".workbench")

    with pytest.raises(FileNotFoundError):
        pymechanical.launch_mechanical(exec_file=exec_file)


@pytest.mark.remote_session_launch
def test_launch_grpc_not_supported_version():
    cwd = os.getcwd()

    if misc.is_windows():
        exec_file = os.path.join(cwd, "ANSYS Inc", "v230", "aisol", "bin", "win64", "AnsysWBU.exe")
    else:
        exec_file = os.path.join(cwd, "ansys_inc", "v230", "aisol", ".workbench")

    with pytest.raises(errors.VersionError):
        pymechanical.mechanical.launch_grpc(exec_file=exec_file)


@pytest.mark.remote_session_launch
@pytest.mark.python_env
def test_warning_message_pythonnet(test_env):
    """Test pythonnet warning of the remote session in virtual env."""

    # Install pymechanical
    subprocess.check_call(
        [test_env.python, "-m", "pip", "install", "-e", "."],
        cwd=test_env.pymechanical_root,
        env=test_env.env,
    )

    # Install pythonnet
    subprocess.check_call([test_env.python, "-m", "pip", "install", "pythonnet"], env=test_env.env)

    # Run remote session in virtual env with pythonnet installed
    remote_py = os.path.join(
        test_env.pymechanical_root, "tests", "scripts", "run_remote_session.py"
    )
    check_warning = subprocess.Popen(
        [test_env.python, remote_py],
        stderr=subprocess.PIPE,
        env=test_env.env,
    )
    check_warning.wait()
    stderr = check_warning.stderr.read().decode()

    # If UserWarning & pythonnet are in the stderr output, set warning to True.
    # Otherwise, set warning to False
    warning = True if "UserWarning" and "pythonnet" in stderr else False

    # Assert the warning message did not appear for the remote session
    assert not warning


@pytest.mark.remote_session_launch
def test_warning_message_default():
    """Test pythonnet warning of the remote session in default env."""
    base = os.getcwd()

    # Run remote session
    remote_py = os.path.join(base, "tests", "scripts", "run_remote_session.py")
    check_warning = subprocess.Popen([sys.executable, remote_py], stderr=subprocess.PIPE)
    check_warning.wait()
    stderr_output = check_warning.stderr.read().decode()

    # If UserWarning & pythonnet are in the stderr output, set warning to True.
    # Otherwise, set warning to False
    warning = True if "UserWarning" and "pythonnet" in stderr_output else False

    # Assert the warning message did not appear for the remote session
    assert not warning


# def test_call_before_launch_or_connect():
#     import ansys.mechanical.core as pymechanical
#     from ansys.mechanical.core.errors import MechanicalExitedError
#
#     # we are not checking any valid value passed to each call,
#     # we just verify an exception being raised.
#
#     mechanical1 = pymechanical.launch_mechanical(start_instance=True)
#     mechanical1.exit()
#
#     error = "Mechanical has already exited."
#
#     with pytest.raises(MechanicalExitedError, match=error):
#         mechanical1.run_python_script("2+5")
#
#     with pytest.raises(MechanicalExitedError, match=error):
#         mechanical1.run_python_script_from_file("test.py")
#
#     # currently we exit silently
#     # with pytest.raises(ValueError, match=error):
#     #     mechanical.exit(force_exit=True)
#
#     with pytest.raises(MechanicalExitedError, match=error):
#         mechanical1.upload(file_name="test.x_t", file_location_destination="some_destination",
#                           chunk_size=1024)
#
#     with pytest.raises(MechanicalExitedError, match=error):
#         mechanical1.download(files="test.x_t", target_dir="some_local_directory", chunk_size=1024)
