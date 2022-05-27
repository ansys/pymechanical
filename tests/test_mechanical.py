import json
import os

import grpc
import pytest

from ansys.mechanical.pymechanical.mechanical import Mechanical


def test_run_jscript_success(mechanical):
    result = mechanical.run_jscript("2+3")
    assert result == "5"


# the following test has been commented. on the developer machine,
# because of the just in time debugging
# we get a message box, commented for now
# def test_run_jscript_error(mechanical):
#     with pytest.raises(grpc.RpcError) as exc_info:
#         result = mechanical.run_jscript("b=a+1")
#     assert exc_info.value.args[0].details ==
#     'Line:\t0\nChar:\t0\nError:\t\'a\' is ' \
#     'undefined\nCode:\t800a1391\nSource:\tMicrosoft JScript runtime error\n'


def test_run_jscript_from_file_success(mechanical):
    current_working_directory = os.getcwd()
    script_path = os.path.join(
        current_working_directory, "tests", "scripts", "run_jscript_success.js"
    )
    print("running jscript : ", script_path)
    result = mechanical.run_jscript_from_file(script_path)
    assert result == "test"


# def test_run_jscript_from_file_error(mechanical):
#     with pytest.raises(grpc.RpcError) as exc_info:
#         current_working_directory = os.getcwd()
#         script_path = os.path.join(
#             current_working_directory, "tests", "scripts", "run_jscript_error.js"
#         )
#         print("running jscript : ", script_path)
#
#     assert (
#         exc_info.value.args[0].details == "Line:\t12\nChar:\t0\nError:\t'a' is "
#         "undefined\nCode:\t800a1391\nSource:\tMicrosoft JScript runtime error\n"
#         "Script:\tb = a + 1;"
#     )


def test_run_python_script_success(mechanical):
    result = mechanical.run_python_script("2+3")
    assert result == "5"


def test_run_python_script_error(mechanical):
    with pytest.raises(grpc.RpcError) as exc_info:
        result = mechanical.run_python_script("import test")

    assert exc_info.value.args[0].details == "No module named test"


def test_run_python_from_file_success(mechanical):
    current_working_directory = os.getcwd()
    script_path = os.path.join(
        current_working_directory, "tests", "scripts", "run_python_success.py"
    )
    print("running jscript : ", script_path)
    result = mechanical.run_python_script_from_file(script_path)

    assert result == "test"


def test_run_python_script_from_file_error(mechanical):
    with pytest.raises(grpc.RpcError) as exc_info:
        current_working_directory = os.getcwd()
        script_path = os.path.join(
            current_working_directory, "tests", "scripts", "run_python_error.py"
        )
        print("running jscript : ", script_path)
        result = mechanical.run_python_script_from_file(script_path)

    assert exc_info.value.args[0].details == "name 'get_myname' is not defined"


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

    file_path_string = "file_path = r'" + os.getcwd() + r"/tests/parts/hsec.x_t'" + "\n"

    # let us append the scripts to run
    func_to_call = """file_path_modified = file_path
attach_geometry(file_path_modified)
generate_mesh()
add_static_structural_analysis_bc_results()
solve_model()
return_total_deformation()
"""

    python_script = data + file_path_string + func_to_call

    result = mechanical.run_python_script(python_script)

    dict = json.loads(result)

    assert dict["Minimum"] == "0 [m]"
    assert dict["Maximum"] == "3.2338457742675092E-06 [m]"
    # we need to adjust this comparison on linux
    # assert '1.2844200522847287E-06 [m]' == '1.284420052019201E-06 [m]'
    # assert dict["Average"] == "1.284420052019201E-06 [m]"


def test_call_before_launch_or_connect():
    # we are not checking any valid value passed to each call,
    # we just verify an exception being raised.

    mechanical = Mechanical()
    error = "Don't have a valid connection to mechanical. Use either launch or connect first."

    with pytest.raises(ValueError, match=error):
        mechanical.run_jscript("2+5")

    with pytest.raises(ValueError, match=error):
        mechanical.run_jscript_from_file("test.js")

    with pytest.raises(ValueError, match=error):
        mechanical.run_python_script("2+5")

    with pytest.raises(ValueError, match=error):
        mechanical.run_python_script_from_file("test.py")

    with pytest.raises(ValueError, match=error):
        mechanical.exit()
