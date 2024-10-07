# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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
import sysconfig

import git
import pytest

from ansys.mechanical.core.autocomplete import _cli_impl as autocomplete_cli_impl
from ansys.mechanical.core.run import _cli_impl

git_repo = git.Repo(os.getcwd(), search_parent_directories=True)
REPO_PATH = Path(git_repo.git.rev_parse("--show-toplevel"))


@pytest.mark.cli
def test_cli_default(disable_cli):
    args, env = _cli_impl(exe="AnsysWBU.exe", version=241, port=11)
    assert os.environ == env
    assert "-AppModeMech" in args
    assert "-b" in args
    assert "-DSApplet" in args
    assert "AnsysWBU.exe" in args


@pytest.mark.cli
def test_cli_debug(disable_cli):
    _, env = _cli_impl(exe="AnsysWBU.exe", version=241, debug=True, port=11)
    assert "WBDEBUG_STOP" in env


@pytest.mark.cli
def test_cli_graphical(disable_cli):
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, graphical=True)
    assert "-b" not in args


@pytest.mark.cli
def test_cli_appdata(disable_cli):
    _, env = _cli_impl(exe="AnsysWBU.exe", version=241, private_appdata=True, port=11)
    var_to_compare = "TEMP" if os.name == "nt" else "HOME"
    assert os.environ[var_to_compare] != env[var_to_compare]


@pytest.mark.cli
def test_cli_errors(disable_cli):
    # can't mix project file and input script
    with pytest.raises(Exception):
        _cli_impl(
            exe="AnsysWBU.exe",
            version=241,
            project_file="foo.mechdb",
            input_script="foo.py",
            graphical=True,
        )
    # project file only works in graphical mode
    with pytest.raises(Exception):
        _cli_impl(exe="AnsysWBU.exe", version=241, project_file="foo.mechdb")
    # can't mix port and project file
    with pytest.raises(Exception):
        _cli_impl(exe="AnsysWBU.exe", version=241, project_file="foo.mechdb", port=11)
    # can't mix port and input script
    with pytest.raises(Exception):
        _cli_impl(exe="AnsysWBU.exe", version=241, input_script="foo.py", port=11)


@pytest.mark.cli
def test_cli_appmode(disable_cli):
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, show_welcome_screen=True, graphical=True)
    assert "-AppModeMech" not in args


@pytest.mark.cli
def test_cli_231(disable_cli):
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=231, port=11)
    assert "-nosplash" in args
    assert "-notabctrl" in args


@pytest.mark.cli
def test_cli_port(disable_cli):
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, port=11)
    assert "-grpc" in args
    assert "11" in args


@pytest.mark.cli
def test_cli_project(disable_cli):
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, project_file="foo.mechdb", graphical=True)
    assert "-file" in args
    assert "foo.mechdb" in args


@pytest.mark.cli
def test_cli_script(disable_cli):
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, input_script="foo.py", graphical=True)
    assert "-script" in args
    assert "foo.py" in args


@pytest.mark.cli
def test_cli_scriptargs(disable_cli):
    args, _ = _cli_impl(
        exe="AnsysWBU.exe",
        version=241,
        input_script="foo.py",
        script_args="arg1,arg2,arg3",
        graphical=True,
    )
    assert "-ScriptArgs" in args
    assert '"arg1,arg2,arg3"' in args
    assert "-script" in args
    assert "foo.py" in args


@pytest.mark.cli
def test_cli_scriptargs_no_script(disable_cli):
    with pytest.raises(Exception):
        _cli_impl(
            exe="AnsysWBU.exe",
            version=241,
            script_args="arg1,arg2,arg3",
            graphical=True,
        )


@pytest.mark.cli
def test_cli_scriptargs_singlequote(disable_cli):
    args, _ = _cli_impl(
        exe="AnsysWBU.exe",
        version=241,
        input_script="foo.py",
        script_args="arg1,arg2,'arg3'",
        graphical=True,
    )
    assert "-ScriptArgs" in args
    assert "\"arg1,arg2,'arg3'\"" in args
    assert "-script" in args
    assert "foo.py" in args


@pytest.mark.cli
def test_cli_scriptargs_doublequote(disable_cli):
    with pytest.raises(Exception):
        _cli_impl(
            exe="AnsysWBU.exe",
            version=241,
            input_script="foo.py",
            script_args='arg1,"arg2",arg3',
            graphical=True,
        )


@pytest.mark.cli
def test_cli_features(disable_cli):
    with pytest.warns(UserWarning):
        args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, features="a;b;c", port=11)
        assert "-featureflags" in args
        assert "a;b;c" in args
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, features="MultistageHarmonic", port=11)
    assert "Mechanical.MultistageHarmonic" in args


@pytest.mark.cli
def test_cli_exit(disable_cli):
    # Regardless of version, `exit` does nothing on its own
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=232, exit=True, port=11)
    assert "-x" not in args

    args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, exit=True, port=11)
    assert "-x" not in args

    # On versions earlier than 2024R1, `exit` throws a warning but does nothing
    with pytest.warns(UserWarning):
        args, _ = _cli_impl(exe="AnsysWBU.exe", version=232, exit=True, input_script="foo.py")
        assert "-x" not in args

    # In UI mode, exit must be manually specified
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, input_script="foo.py", graphical=True)
    assert "-x" not in args

    # In batch mode, exit is implied
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, input_script="foo.py")
    assert "-x" in args

    # In batch mode, exit can be explicitly passed
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, exit=True, input_script="foo.py")
    assert "-x" in args

    # In batch mode, exit can not be disabled
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, exit=False, input_script="foo.py")
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


def init_repo(tmp_path: pytest.TempPathFactory) -> git.Repo:
    """Set up a git repository given a temporary path.

    Parameters
    ----------
    tmp_path: pytest.TempPathFactory
        A temporary folder created by pytest.

    Returns
    -------
    git.Repo
        The git repository at the temporary path.
    """
    git.Repo.init(tmp_path)
    repo = git.Repo(tmp_path)
    repo.index.commit("initialized git repo for tmp_path")

    return repo


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


def get_stubs_location(revision: int) -> Path:
    """Get the ansys-mechanical-stubs location with specified revision.

    Parameters
    ----------
    revision: int
        The Mechanical revision number. For example, "242".

    Returns
    -------
    pathlib.Path
        The path to the ansys-mechanical-stubs installation.
    """
    return (
        Path(sysconfig.get_paths()["purelib"]) / "ansys" / "mechanical" / "stubs" / f"v{revision}"
    )


@pytest.mark.cli
def test_autocomplete_cli_ide_exception(capfd):
    """Test autocomplete raises an exception for anything but vscode."""
    with pytest.raises(Exception):
        autocomplete_cli_impl(
            ide="pycharm",
            settings_type="user",
            revision=242,
        )


@pytest.mark.cli
def test_autocomplete_cli_user_settings(capfd):
    """Test autocomplete prints correct information for user settings."""
    # Set the revision number
    revision = 242

    # Run the autocomplete settings command for the user settings type
    autocomplete_cli_impl(
        ide="vscode",
        settings_type="user",
        revision=revision,
    )

    # Get output of autocomplete settings command
    out, err = capfd.readouterr()
    out = out.replace("\\\\", "\\")

    # Get the path to the settings.json file based on the git root & .vscode folder
    settings_json = get_settings_location()
    stubs_location = get_stubs_location(revision)

    assert f"Update {settings_json} with the following information" in out
    assert str(stubs_location) in out


@pytest.mark.cli
def test_autocomplete_cli_workspace_settings(capfd):
    """Test autocomplete prints correct information for workplace settings."""
    # Set the revision number
    revision = 241

    # Run the autocomplete settings command
    autocomplete_cli_impl(
        ide="vscode",
        settings_type="workspace",
        revision=revision,
    )

    # Get output of autocomplete settings command
    out, err = capfd.readouterr()
    out = out.replace("\\\\", "\\")

    # Get the path to the settings.json file based on the git root & .vscode folder
    settings_json = REPO_PATH / ".vscode" / "settings.json"
    stubs_location = get_stubs_location(revision)

    # Assert the correct settings.json file and stubs location is in the output
    assert f"Update {settings_json} with the following information" in out
    assert str(stubs_location) in out


@pytest.mark.cli
@pytest.mark.python_env
def test_autocomplete_venv(test_env, run_subprocess, rootdir):
    """Test autocomplete settings location when a virtual environment is active."""
    # Set the revision number
    revision = 242

    # Install pymechanical
    subprocess.check_call(
        [test_env.python, "-m", "pip", "install", "-e", "."],
        cwd=rootdir,
        env=test_env.env,
    )

    # Run ansys-mechanical-autocomplete in the test virtual environment
    process, stdout, stderr = run_subprocess(
        [
            "ansys-mechanical-autocomplete",
            "--ide",
            "vscode",
            "--settings_type",
            "user",
            "--revision",
            str(revision),
        ],
        env=test_env.env,
    )
    # Decode stdout and fix extra backslashes in paths
    stdout = stdout.decode().replace("\\\\", "\\")

    # Assert virtual environment is in the stdout
    assert ".venv" in stdout
