import os

import pytest

from ansys.mechanical.pymechanical.mechanical import Mechanical


@pytest.fixture(scope="session")
def mechanical():
    print("current working directory: ", os.getcwd())
    mechanical_obj = Mechanical()
    # mechanical_exe_path = \
    #     r"C:\ANSYSDev\Program Files\ANSYS Inc\v222\aisol\bin\winx64\AnsysWBU.exe"
    # additional_environment_variables = { "WBDEBUG_TRACE_MESSAGE":"1",
    #                                      "WBDEBUG_STDOUT_MESSAGE":"1",
    # mechanical_obj.launch(
    #     batch=True,
    #     wait_time=60,
    #     exe_path=mechanical_exe_path,
    #     use_loopback_address=True,
    #     port=10000,
    # )
    # mechanical_obj.launch(batch=True, port=10000,
    #                       wait_time=60, version="222",
    #                       use_loopback_address=True)
    mechanical_obj.launch(batch=True, wait_time=60, version="222", use_loopback_address=True)
    # mechanical_obj.launch(exe_path=mechanical_exe_path, batch=True, port=10000, wait_time=60)
    yield mechanical_obj

    mechanical_obj.exit()
