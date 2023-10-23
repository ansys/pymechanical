# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.

import pytest

import ansys.mechanical.core.misc as misc


@pytest.mark.remote_session_launch
def test_valid_start_instance():
    assert misc.check_valid_start_instance("true")

    assert False == misc.check_valid_start_instance("false")

    assert misc.check_valid_start_instance("True")

    assert False == misc.check_valid_start_instance("False")

    with pytest.raises(ValueError):
        misc.check_valid_start_instance([])

    with pytest.raises(ValueError):
        misc.check_valid_start_instance("hello")


@pytest.mark.remote_session_launch
def test_is_float():
    assert misc.is_float("1.3")

    assert False == misc.is_float("hello")
