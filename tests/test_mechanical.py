import json
import os

import grpc
import pytest


def validate_real(value, expected, tol):
    low = 1 - tol
    high = 1 + tol

    if expected * low <= value <= expected * high:
        return True

    return False


def test_run_python_script_success(mechanical):
    result = mechanical.run_python_script("2+3")
    assert result == "5"


def test_run_python_script_error(mechanical):
    with pytest.raises(grpc.RpcError) as exc_info:
        mechanical.run_python_script("import test")

    assert exc_info.value.details() == "No module named test"


def test_run_python_from_file_success(mechanical):
    current_working_directory = os.getcwd()
    script_path = os.path.join(
        current_working_directory, "tests", "scripts", "run_python_success.py"
    )
    print("running python script : ", script_path)
    result = mechanical.run_python_script_from_file(script_path)

    assert result == "test"


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


def test_run_python_script_from_file_error(mechanical):
    with pytest.raises(grpc.RpcError) as exc_info:
        current_working_directory = os.getcwd()
        script_path = os.path.join(
            current_working_directory, "tests", "scripts", "run_python_error.py"
        )
        print("running python script : ", script_path)
        mechanical.run_python_script_from_file(script_path)

    assert exc_info.value.details() == "name 'get_myname' is not defined"


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
directory = ExtAPI.DataModel.Project.ProjectDirectory
file_path_modified=os.path.join(directory,'hsec.x_t')
attach_geometry(file_path_modified)
generate_mesh()
add_static_structural_analysis_bc_results()
solve_model()
return_total_deformation()
    """
    python_script = data + file_path_string + func_to_call

    result = mechanical.run_python_script(python_script)

    # if the solve fails, solve.out contains enough information
    solve_out_path = get_solve_out_path(mechanical)

    if solve_out_path != "":
        print(f"downloading {solve_out_path} from server")
        print(f"downloading to {current_working_directory}")
        mechanical.download(solve_out_path, target_dir=current_working_directory)
        solve_out_local_path = os.path.join(current_working_directory, "solve.out")

        write_file_contents_to_console(solve_out_local_path)

        # done with solve.out - remove it
        os.remove(solve_out_local_path)

    return result


# @pytest.mark.skip(reason="avoid long running")
def test_upload_attach_mesh_solve_use_api_non_distributed_solve(mechanical):
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

    assert validate_real(min_value, 0, 0.1)
    assert validate_real(max_value, 2.9068725331072863e-06, 0.1)
    assert validate_real(avg_value, 1.1398642395560755e-06, 0.1)


def test_upload_attach_mesh_solve_use_api_distributed_solve(mechanical):
    # default is distributed solve

    result = solve_and_return_results(mechanical)

    dict_result = json.loads(result)

    min_value = float(dict_result["Minimum"].split(" ")[0])
    max_value = float(dict_result["Maximum"].split(" ")[0])
    avg_value = float(dict_result["Average"].split(" ")[0])

    assert validate_real(min_value, 0, 0.1)
    assert validate_real(max_value, 2.9068725331072863e-06, 0.1)
    assert validate_real(avg_value, 1.1398642395560755e-06, 0.1)


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
    mechanical.download(files=file_path, target_dir=local_directory, chunk_size=chunk_size)

    base_name = os.path.basename(file_path)
    local_path = os.path.join(local_directory, base_name)

    assert os.path.exists(local_path) and os.path.getsize(local_path) > 0


@pytest.mark.parametrize("file_name", ["hsec.x_t"])
def test_download_file(mechanical, tmpdir, file_name):
    verify_download(mechanical, tmpdir, file_name, 1024 * 1024)


# we are using only a small test file
# change the chunk_size for that
# ideally this will be 64*1024, 1024*1024, etc.
@pytest.mark.parametrize("chunk_size", [10, 50, 100])
def test_download_file_different_chunk_size1(mechanical, tmpdir, chunk_size):
    file_name = "hsec.x_t"
    verify_download(mechanical, tmpdir, file_name, chunk_size)


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
