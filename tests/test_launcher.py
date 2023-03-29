import pytest

import ansys.mechanical.core.launcher as launcher
from ansys.mechanical.core.misc import is_windows


@pytest.mark.remote_session_launch
def test_verify_path_exists():
    if is_windows():
        windows_path = (
            "C:\\does_not_exist\\Program Files\\ANSYS Inc\\v111\\aisol\\bin\\winx64\\AnsysWBU.exe"
        )
        with pytest.raises(FileNotFoundError):
            launcher.MechanicalLauncher.verify_path_exists(windows_path)
    else:
        linux_path = "/usr/does_not_exist/ansys_inc/v111/aisol/.workbench"
        with pytest.raises(FileNotFoundError):
            launcher.MechanicalLauncher.verify_path_exists(linux_path)


@pytest.mark.remote_session_launch
def test_verify_mode_exists():
    additional_args = None
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMech")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMesh")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeRest")

    additional_args = []
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMech")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMesh")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeRest")

    additional_args = ["-AppModeMech"]
    assert launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMech")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMesh")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeRest")

    additional_args = ["-AppModeMesh"]
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMech")
    assert launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMesh")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeRest")

    additional_args = ["-AppModeRest"]
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMech")
    assert not launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeMesh")
    assert launcher.MechanicalLauncher._mode_exists(additional_args, "-AppModeRest")
