import json
import math
import os

import grpc
import pytest

from ansys.mechanical.core.misc import is_windows


def test_run_jscript_success(mechanical):
    result = mechanical.run_jscript("2+3")
    assert result == "5"


# # the following test has been commented. on the developer machine,
# # because of the just in time debugging
# # we get a message box, commented for now
# def test_run_jscript_error(mechanical):
#     with pytest.raises(grpc.RpcError) as exc_info:
#         result = mechanical.run_jscript("b=a+1")
#     assert exc_info.value.details() == \
#            'Line:\t0\nChar:\t0\nError:\t\'a\' is undefined\n' \
#            'Code:\t800a1391\nSource:\tMicrosoft JScript runtime error\n'


def test_run_jscript_from_file_success(mechanical):
    current_working_directory = os.getcwd()
    script_path = os.path.join(
        current_working_directory, "tests", "scripts", "run_jscript_success.js"
    )
    print("running jscript : ", script_path)
    result = mechanical.run_jscript_from_file(script_path)
    assert result == "test"


# # the following test has been commented. on the developer machine,
# # because of the just in time debugging
# # we get a message box, commented for now
# def test_run_jscript_from_file_error(mechanical):
#     with pytest.raises(grpc.RpcError) as exc_info:
#         current_working_directory = os.getcwd()
#         script_path = os.path.join(
#             current_working_directory, "tests", "scripts", "run_jscript_error.js"
#         )
#
#         print("running jscript : ", script_path)
#         result = mechanical.run_jscript_from_file(script_path)
#
#     assert exc_info.value.details() == \
#            "Line:\t12\nChar:\t0\nError:\t'a' is undefined\nCode:\t800a1391\n" \
#            "Source:\tMicrosoft JScript runtime error\nScript:\tb = a + 1;"


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


# def test_attach_mesh_solve(mechanical):
#     python_script = r".\scripts\mech_workflow.py"
#     result = mechanical.run_python_script_from_file(python_script)
#     dict = json.loads(result)
#
#     assert dict["Minimum"] == "0 [m]"
#     assert dict["Maximum"] == "9.70153746362981E-06 [m]"
#     assert dict["Average"] == "3.8532601588897765E-06 [m]"

# @pytest.mark.skip(reason="avoid long running")
def test_attach_mesh_solve_use_api(mechanical):
    current_working_directory = os.getcwd()
    python_script = os.path.join(current_working_directory, "tests", "scripts", "api.py")
    print("opening : ", python_script)

    text_file = open(python_script, "r")
    # read whole file to a string
    data = text_file.read()
    # close file
    text_file.close()

    file_path_part = os.path.join(current_working_directory, "tests", "parts", "hsec.x_t")

    file_path_string = "file_path = r'" + file_path_part + "'" + "\n"

    # let us append the scripts to run
    func_to_call = """file_path_modified = file_path.replace('\\\\', '\\\\\\\\')
attach_geometry(file_path_modified)
generate_mesh()
add_static_structural_analysis_bc_results()
solve_model()
return_total_deformation()
"""

    python_script = data + file_path_string + func_to_call

    result = mechanical.run_python_script(python_script, enable_logging=True, log_level="DEBUG")

    dict_result = json.loads(result)

    min_value = float(dict_result["Minimum"].split(" ")[0])
    max_value = float(dict_result["Maximum"].split(" ")[0])
    avg_value = float(dict_result["Average"].split(" ")[0])

    assert math.isclose(min_value, 0)

    if is_windows():
        assert math.isclose(max_value, 0.0001144438029641797)
        assert math.isclose(avg_value, 4.48765448814899e-05)
    else:
        assert math.isclose(max_value, 2.9068725331072863e-06)
        assert math.isclose(avg_value, 1.1398642395560755e-06)


# @pytest.mark.skip(reason="avoid long running")
@pytest.mark.parametrize("file_name", [r"hsec.x_t"])
def test_upload_file(mechanical, file_name):
    mechanical.run_python_script("ExtAPI.DataModel.Project.New()")
    directory = mechanical.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")
    print(directory)

    current_working_directory = os.getcwd()
    file_path = os.path.join(current_working_directory, "tests", "parts", file_name)
    mechanical.upload_file(file_path, directory, 1024 * 1024)

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
def test_upload_file_with_different_chunk_size(mechanical, chunk_size):
    current_working_directory = os.getcwd()
    file_path = os.path.join(current_working_directory, "tests", "parts", "hsec.x_t")
    mechanical.run_python_script("ExtAPI.DataModel.Project.New()")
    directory = mechanical.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")
    mechanical.upload_file(file_path, directory, chunk_size=chunk_size)


# @pytest.mark.skip(reason="avoid long running")
def test_upload_attach_mesh_solve_use_api(mechanical):
    current_working_directory = os.getcwd()
    file_path = os.path.join(current_working_directory, "tests", "parts", "hsec.x_t")

    mechanical.run_python_script("ExtAPI.DataModel.Project.New()")
    directory = mechanical.run_python_script("ExtAPI.DataModel.Project.ProjectDirectory")
    mechanical.upload_file(file_path, directory, 1024 * 1024)

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

    dict_result = json.loads(result)

    min_value = float(dict_result["Minimum"].split(" ")[0])
    max_value = float(dict_result["Maximum"].split(" ")[0])
    avg_value = float(dict_result["Average"].split(" ")[0])

    assert math.isclose(min_value, 0)

    if is_windows():
        assert math.isclose(max_value, 0.0001144438029641797)
        assert math.isclose(avg_value, 4.48765448814899e-05)
    else:
        assert math.isclose(max_value, 2.9068725331072863e-06)
        assert math.isclose(avg_value, 1.1398642395560755e-06)


@pytest.mark.parametrize("file_name", ["hsec.x_t"])
def test_download_file(mechanical, tmpdir, file_name):
    print(f"using the temporary directory: {tmpdir}")
    current_working_directory = os.getcwd()
    file_path = os.path.join(current_working_directory, "tests", "parts", file_name)
    local_directory = tmpdir.strpath

    mechanical.download_file(file_path, local_directory, 1024 * 1024)

    base_name = os.path.basename(file_path)
    local_path = os.path.join(local_directory, base_name)

    assert os.path.exists(local_path) and os.path.getsize(local_path) > 0


# we are using only a small test file
# change the chunk_size for that
# ideally this will be 64*1024, 1024*1024, etc.
@pytest.mark.parametrize("chunk_size", [10, 50, 100])
def test_download_file_different_chunk_size1(mechanical, tmpdir, chunk_size):
    print(f"using the temporary directory: {tmpdir}")
    current_working_directory = os.getcwd()
    file_path = os.path.join(current_working_directory, "tests", "parts", "hsec.x_t")
    local_directory = tmpdir.strpath

    mechanical.download_file(file_path, local_directory, chunk_size=chunk_size)

    base_name = os.path.basename(file_path)
    local_path = os.path.join(local_directory, base_name)

    assert os.path.exists(local_path) and os.path.getsize(local_path) > 0


# def test_call_before_launch_or_connect():
#     # we are not checking any valid value passed to each call,
#     # we just verify an exception being raised.
#
#     mechanical = pymechanical.Mechanical()
#
#     error = "Don't have a valid connection to mechanical. Use either launch or connect first."
#
#     with pytest.raises(ValueError, match=error):
#         mechanical.run_jscript("2+5")
#
#     with pytest.raises(ValueError, match=error):
#         mechanical.run_jscript_from_file("test.js")
#
#     with pytest.raises(ValueError, match=error):
#         mechanical.run_python_script("2+5")
#
#     with pytest.raises(ValueError, match=error):
#         mechanical.run_python_script_from_file("test.py")
#
#     with pytest.raises(ValueError, match=error):
#         mechanical.exit(force_exit=True)
#
#     with pytest.raises(ValueError, match=error):
#         mechanical.upload_file("test.x_t", "some_destination", 1024)
#
#     with pytest.raises(ValueError, match=error):
#         mechanical.download_file("test.x_t", "some_local_directory", 1024)
