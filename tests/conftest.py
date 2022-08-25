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

    if not pymechanical.mechanical.get_start_instance():
        # ip needs to be passed or start instance takes precedence
        mechanical = pymechanical.launch_mechanical(clear_on_connect=False, cleanup_on_exit=False)
    else:
        mechanical = pymechanical.launch_mechanical()

    print(mechanical)
    yield mechanical

    assert "Ansys Mechanical" in str(mechanical)

    if not pymechanical.mechanical.get_start_instance():
        mechanical.exit(force=True)
        assert mechanical.exited
        assert "Mechanical exited" in str(mechanical)
        with pytest.raises(MechanicalExitedError):
            mechanical.run_python_script("3+4")
