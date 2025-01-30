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

import os
from pathlib import Path
import subprocess
import sys

import pytest

from ansys.mechanical.core.ide_config import _cli_impl as ideconfig_cli_impl
from ansys.mechanical.core.ide_config import get_stubs_location, get_stubs_versions
from ansys.mechanical.core.run import _cli_impl

STUBS_LOC = get_stubs_location()
STUBS_REVNS = get_stubs_versions(STUBS_LOC)
MIN_STUBS_REVN = min(STUBS_REVNS)
MAX_STUBS_REVN = max(STUBS_REVNS)


@pytest.mark.cli
def test_cli_default(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    args, env = _cli_impl(exe="AnsysWBU.exe", version=version, port=11)
    assert os.environ == env
    assert "-AppModeMech" in args
    assert "-b" in args
    assert "-DSApplet" in args
    assert "AnsysWBU.exe" in args


@pytest.mark.cli
def test_cli_debug(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    _, env = _cli_impl(exe="AnsysWBU.exe", version=version, debug=True, port=11)
    assert "WBDEBUG_STOP" in env


@pytest.mark.cli
def test_cli_graphical(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=version, graphical=True)
    assert "-b" not in args


@pytest.mark.cli
def test_cli_appdata(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    _, env = _cli_impl(exe="AnsysWBU.exe", version=version, private_appdata=True, port=11)
    var_to_compare = "TEMP" if os.name == "nt" else "HOME"
    assert os.environ[var_to_compare] != env[var_to_compare]


@pytest.mark.cli
def test_cli_errors(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    # can't mix project file and input script
    with pytest.raises(Exception):
        _cli_impl(
            exe="AnsysWBU.exe",
            version=version,
            project_file="foo.mechdb",
            input_script="foo.py",
            graphical=True,
        )
    # project file only works in graphical mode
    with pytest.raises(Exception):
        _cli_impl(exe="AnsysWBU.exe", version=version, project_file="foo.mechdb")
    # can't mix port and project file
    with pytest.raises(Exception):
        _cli_impl(exe="AnsysWBU.exe", version=version, project_file="foo.mechdb", port=11)
    # can't mix port and input script
    with pytest.raises(Exception):
        _cli_impl(exe="AnsysWBU.exe", version=version, input_script="foo.py", port=11)


@pytest.mark.cli
def test_cli_appmode(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    args, _ = _cli_impl(
        exe="AnsysWBU.exe", version=version, show_welcome_screen=True, graphical=True
    )
    assert "-AppModeMech" not in args


@pytest.mark.cli
def test_cli_231(disable_cli):
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=231, port=11)
    assert "-nosplash" in args
    assert "-notabctrl" in args


@pytest.mark.cli
def test_cli_port(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=version, port=11)
    assert "-grpc" in args
    assert "11" in args


@pytest.mark.cli
def test_cli_project(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    args, _ = _cli_impl(
        exe="AnsysWBU.exe", version=version, project_file="foo.mechdb", graphical=True
    )
    assert "-file" in args
    assert "foo.mechdb" in args


@pytest.mark.cli
def test_cli_script(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=version, input_script="foo.py", graphical=True)
    assert "-script" in args
    assert "foo.py" in args


@pytest.mark.cli
def test_cli_scriptargs(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    args, _ = _cli_impl(
        exe="AnsysWBU.exe",
        version=version,
        input_script="foo.py",
        script_args="arg1,arg2,arg3",
        graphical=True,
    )
    assert "-ScriptArgs" in args
    assert '"arg1,arg2,arg3"' in args
    assert "-script" in args
    assert "foo.py" in args


@pytest.mark.cli
def test_cli_scriptargs_no_script(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    with pytest.raises(Exception):
        _cli_impl(
            exe="AnsysWBU.exe",
            version=version,
            script_args="arg1,arg2,arg3",
            graphical=True,
        )


@pytest.mark.cli
def test_cli_scriptargs_singlequote(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    args, _ = _cli_impl(
        exe="AnsysWBU.exe",
        version=version,
        input_script="foo.py",
        script_args="arg1,arg2,'arg3'",
        graphical=True,
    )
    assert "-ScriptArgs" in args
    assert "\"arg1,arg2,'arg3'\"" in args
    assert "-script" in args
    assert "foo.py" in args


@pytest.mark.cli
def test_cli_scriptargs_doublequote(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    with pytest.raises(Exception):
        _cli_impl(
            exe="AnsysWBU.exe",
            version=version,
            input_script="foo.py",
            script_args='arg1,"arg2",arg3',
            graphical=True,
        )


@pytest.mark.cli
def test_cli_features(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    with pytest.warns(UserWarning):
        args, _ = _cli_impl(exe="AnsysWBU.exe", version=version, features="a;b;c", port=11)
        assert "-featureflags" in args
        assert "a;b;c" in args
    args, _ = _cli_impl(
        exe="AnsysWBU.exe",
        version=version,
        features="ThermalShells;MultistageHarmonic;CPython",
        port=11,
    )
    args = [arg for arg in args if arg.startswith("Mechanical")][0]
    assert "Mechanical.ThermalShells" in args
    assert "Mechanical.MultistageHarmonic" in args
    assert "Mechanical.CPython.Capability" in args


@pytest.mark.cli
def test_cli_exit(disable_cli, pytestconfig):
    version = int(pytestconfig.getoption("ansys_version"))
    # Regardless of version, `exit` does nothing on its own
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=232, exit=True, port=11)
    assert "-x" not in args

    args, _ = _cli_impl(exe="AnsysWBU.exe", version=version, exit=True, port=11)
    assert "-x" not in args

    # On versions earlier than 2024R1, `exit` throws a warning but does nothing
    with pytest.warns(UserWarning):
        args, _ = _cli_impl(exe="AnsysWBU.exe", version=232, exit=True, input_script="foo.py")
        assert "-x" not in args

    # In UI mode, exit must be manually specified
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=version, input_script="foo.py", graphical=True)
    assert "-x" not in args

    # In batch mode, exit is implied
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=version, input_script="foo.py")
    assert "-x" in args

    # In batch mode, exit can be explicitly passed
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=version, exit=True, input_script="foo.py")
    assert "-x" in args

    # In batch mode, exit can not be disabled
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=version, exit=False, input_script="foo.py")
    assert "-x" in args


@pytest.mark.cli
def test_cli_batch_required_args(disable_cli):
    # ansys-mechanical -r 241 => exception
    with pytest.raises(Exception):
        _cli_impl(exe="AnsysWBU.exe", version=241)

    # ansys-mechanical -r 241 -g => no exception
    try:
        _cli_impl(exe="AnsysWBU.exe", version=241, graphical=True)
    except Exception as e:
        assert False, f"cli raised an exception: {e}"

    # ansys-mechanical -r 241 -i input.py => no exception
    try:
        _cli_impl(exe="AnsysWBU.exe", version=241, input_script="input.py")
    except Exception as e:
        assert False, f"cli raised an exception: {e}"

    # ansys-mechanical -r 241 -port 11 => no exception
    try:
        _cli_impl(exe="AnsysWBU.exe", version=241, port=11)
    except Exception as e:
        assert False, f"cli raised an exception: {e}"


def get_settings_location() -> str:
    """Get the location of settings.json for user settings.

    Returns
    -------
    str
        The path to the settings.json file for users on Windows and Linux.
    """
    if "win" in sys.platform:
        settings_json = Path(os.environ.get("APPDATA")) / "Code" / "User" / "settings.json"
    elif "lin" in sys.platform:
        settings_json = Path(os.environ.get("HOME")) / ".config" / "Code" / "User" / "settings.json"

    return settings_json


@pytest.mark.cli
def test_ideconfig_cli_ide_exception(capfd, pytestconfig):
    """Test IDE configuration raises an exception for anything but vscode."""
    revision = int(pytestconfig.getoption("ansys_version"))
    with pytest.raises(Exception):
        ideconfig_cli_impl(
            ide="pycharm",
            target="user",
            revision=revision,
        )


def test_ideconfig_cli_version_exception(pytestconfig):
    """Test the IDE configuration raises an exception when the version is out of bounds."""
    revision = int(pytestconfig.getoption("ansys_version"))
    stubs_location = get_stubs_location()
    stubs_revns = get_stubs_versions(stubs_location)

    # If revision number is greater than the maximum stubs revision number
    # assert an exception is raised
    if revision > max(stubs_revns):
        with pytest.raises(Exception):
            ideconfig_cli_impl(
                ide="vscode",
                target="user",
                revision=revision,
            )


@pytest.mark.cli
@pytest.mark.version_range(MIN_STUBS_REVN, MAX_STUBS_REVN)
def test_ideconfig_cli_user_settings(capfd, pytestconfig):
    """Test the IDE configuration prints correct information for user settings."""
    # Get the revision number
    revision = int(pytestconfig.getoption("ansys_version"))
    stubs_location = get_stubs_location()

    # Run the IDE configuration command for the user settings type
    ideconfig_cli_impl(
        ide="vscode",
        target="user",
        revision=revision,
    )

    # Get output of the IDE configuration command
    out, err = capfd.readouterr()
    out = out.replace("\\\\", "\\")

    # Get the path to the settings.json file based on operating system env vars
    settings_json = get_settings_location()

    assert f"Update {settings_json} with the following information" in out
    assert str(stubs_location) in out


@pytest.mark.cli
@pytest.mark.version_range(MIN_STUBS_REVN, MAX_STUBS_REVN)
def test_ideconfig_cli_workspace_settings(capfd, pytestconfig):
    """Test the IDE configuration prints correct information for workplace settings."""
    # Set the revision number
    revision = int(pytestconfig.getoption("ansys_version"))
    stubs_location = get_stubs_location()

    # Run the IDE configuration command
    ideconfig_cli_impl(
        ide="vscode",
        target="workspace",
        revision=revision,
    )

    # Get output of the IDE configuration command
    out, err = capfd.readouterr()
    out = out.replace("\\\\", "\\")

    # Get the path to the settings.json file based on the current directory & .vscode folder
    settings_json = Path.cwd() / ".vscode" / "settings.json"

    # Assert the correct settings.json file and stubs location is in the output
    assert f"Update {settings_json} with the following information" in out
    assert str(stubs_location) in out
    assert "Please ensure the .vscode folder is in the root of your project or repository" in out


@pytest.mark.cli
@pytest.mark.python_env
@pytest.mark.version_range(MIN_STUBS_REVN, MAX_STUBS_REVN)
def test_ideconfig_cli_venv(test_env, run_subprocess, rootdir, pytestconfig):
    """Test the IDE configuration location when a virtual environment is active."""
    # Set the revision number
    revision = pytestconfig.getoption("ansys_version")

    # Install pymechanical
    subprocess.check_call(
        [test_env.python, "-m", "pip", "install", "-e", "."],
        cwd=rootdir,
        env=test_env.env,
    )

    # Get the virtual environment location
    subprocess_output = run_subprocess(
        [test_env.python, "-c", "'import sys; print(sys.prefix)'"],
        env=test_env.env,
    )
    # Decode stdout and fix extra backslashes in paths
    venv_loc = subprocess_output[1].decode().replace("\\\\", "\\")

    # Run ansys-mechanical-ideconfig in the test virtual environment
    subprocess_output_ideconfig = run_subprocess(
        [
            "ansys-mechanical-ideconfig",
            "--ide",
            "vscode",
            "--target",
            "user",
            "--revision",
            str(revision),
        ],
        env=test_env.env,
    )
    # Decode stdout and fix extra backslashes in paths
    stdout = subprocess_output_ideconfig[1].decode().replace("\\\\", "\\")

    # Assert virtual environment is in the stdout
    assert venv_loc in stdout


@pytest.mark.cli
@pytest.mark.python_env
@pytest.mark.version_range(MIN_STUBS_REVN, MAX_STUBS_REVN)
def test_ideconfig_cli_default(test_env, run_subprocess, rootdir, pytestconfig):
    """Test the IDE configuration location when no arguments are supplied."""
    # Get the revision number
    revision = pytestconfig.getoption("ansys_version")
    # Set part of the settings.json path
    settings_json_fragment = Path("Code") / "User" / "settings.json"

    # Install pymechanical
    subprocess.check_call(
        [test_env.python, "-m", "pip", "install", "-e", "."],
        cwd=rootdir,
        env=test_env.env,
    )

    # Get the virtual environment location
    subprocess_output = run_subprocess(
        [test_env.python, "-c", "'import sys; print(sys.prefix)'"],
        env=test_env.env,
    )
    # Decode stdout and fix extra backslashes in paths
    venv_loc = subprocess_output[1].decode().replace("\\\\", "\\")

    # Run ansys-mechanical-ideconfig in the test virtual environment
    subprocess_output_ideconfig = run_subprocess(
        ["ansys-mechanical-ideconfig"],
        env=test_env.env,
    )
    # Decode stdout and fix extra backslashes in paths
    stdout = subprocess_output_ideconfig[1].decode().replace("\\\\", "\\")

    assert revision in stdout
    assert str(settings_json_fragment) in stdout
    assert venv_loc in stdout
