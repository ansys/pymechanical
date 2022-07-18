import os

import pytest

import ansys.mechanical.core as pymechanical
from ansys.mechanical.core.errors import MechanicalExitedError

# connect to an existing instance
# @pytest.fixture(scope="session")
# def mechanical():
#     from ansys.mechanical import core as pymechanical
#     mechanical = pymechanical.Mechanical()
#     yield mechanical
#
#     mechanical.exit(force=True)
#     assert mechanical.exited
#     assert "Mechanical exited" in str(mechanical)
#     with pytest.raises(MechanicalExitedError):
#         mechanical.run_python_script("3+4")


@pytest.fixture(scope="session")
def mechanical():
    print("current working directory: ", os.getcwd())
    mechanical = pymechanical.launch_mechanical()
    print(mechanical)
    yield mechanical

    assert "Ansys Mechanical" in str(mechanical)

    mechanical.exit(force=True)
    assert mechanical.exited
    assert "Mechanical exited" in str(mechanical)
    with pytest.raises(MechanicalExitedError):
        mechanical.run_python_script("3+4")
