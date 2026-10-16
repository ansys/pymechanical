# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Test for Command Line Interface (CLI) functionality."""

import json
import os
from pathlib import Path
import subprocess
import sys

import ansys.tools.common.path as atp
from click.testing import CliRunner
import pytest

from ansys.mechanical.core.embedding.initializer import SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS
from ansys.mechanical.core.ide_config import (
    cli as ideconfig_cli,
    get_stubs_location,
    get_stubs_versions,
)
from ansys.mechanical.core.run import _cli_impl, cli

STUBS_LOC = get_stubs_location()
STUBS_REVNS = get_stubs_versions(STUBS_LOC)
MIN_STUBS_REVN = min(STUBS_REVNS)
MAX_STUBS_REVN = max(STUBS_REVNS)


@pytest.mark.cli
def test_cli_default(disable_cli, pytestconfig):
    """Test for default CLI arguments."""
    version = int(pytestconfig.getoption("ansys_version"))
    args, env = _cli_impl(exe="AnsysWBU.exe", version=version, port=11)
    assert os.environ == env
    assert "-AppModeMech" in args
    assert "-b" in args
    assert "-DSApplet" in args
    assert "AnsysWBU.exe" in args


@pytest.mark.cli
def test_cli_debug(disable_cli, pytestconfig):
    """Test for CLI debug argument."""
    version = int(pytestconfig.getoption("ansys_version"))
    _, env = _cli_impl(exe="AnsysWBU.exe", version=version, debug=True, port=11)
    assert "WBDEBUG_STOP" in env


@pytest.mark.cli
def test_cli_graphical(disable_cli, pytestconfig):
    """Test for CLI graphical argument."""
    version = int(pytestconfig.getoption("ansys_version"))
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=version, graphical=True)
    assert "-b" not in args


@pytest.mark.cli
def test_cli_graphical_readonly(disable_cli, pytestconfig):
    """Test for CLI readonly argument in graphical mode."""
    version = int(pytestconfig.getoption("ansys_version"))
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=version, graphical=True, readonly=True)
    assert "-readonly" in args


@pytest.mark.cli
def test_cli_appdata(disable_cli, pytestconfig):
    """Test for CLI private appdata argument."""
    version = int(pytestconfig.getoption("ansys_version"))
    _, env = _cli_impl(exe="AnsysWBU.exe", version=version, private_appdata=True, port=11)
    var_to_compare = "TEMP" if os.name == "nt" else "HOME"
    assert os.environ[var_to_compare] != env[var_to_compare]


@pytest.mark.cli
@pytest.mark.embedding
@pytest.mark.parametrize(
    "options",
    [
        pytest.param(
            {"project_file": "foo.mechdb", "input_script": "foo.py", "graphical": True},
            id="project-with-script",
        ),
        pytest.param({"project_file": "foo.mechdb"}, id="project-in-batch-mode"),
        pytest.param(
            {"project_file": "foo.mechdb", "port": 11, "graphical": True},
            id="project-with-port",
        ),
        pytest.param({"input_script": "foo.py", "port": 11}, id="script-with-port"),
    ],
)
def test_cli_invalid_options(disable_cli, pytestconfig, options):
    """Test incompatible CLI options are rejected independently."""
    version = int(pytestconfig.getoption("ansys_version"))
    with pytest.raises(Exception):
        _cli_impl(exe="AnsysWBU.exe", version=version, **options)


@pytest.mark.cli
def test_cli_appmode(disable_cli, pytestconfig):
    """Test for CLI appmode argument."""
    version = int(pytestconfig.getoption("ansys_version"))
    args, _ = _cli_impl(
        exe="AnsysWBU.exe", version=version, show_welcome_screen=True, graphical=True
    )
    assert "-AppModeMech" not in args


@pytest.mark.cli
def test_cli_port(disable_cli, pytestconfig):
    """Test for CLI port argument."""
    version = int(pytestconfig.getoption("ansys_version"))
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=version, port=11)
    assert "-grpc" in args
    assert "11" in args


@pytest.mark.cli
def test_cli_project(disable_cli, pytestconfig):
    """Test for CLI project argument."""
    version = int(pytestconfig.getoption("ansys_version"))
    args, _ = _cli_impl(
        exe="AnsysWBU.exe", version=version, project_file="foo.mechdb", graphical=True
    )
    assert "-file" in args
    assert "foo.mechdb" in args


@pytest.mark.cli
def test_cli_project_readonly(disable_cli, pytestconfig):
    """Test for CLI readonly argument with project file."""
    version = int(pytestconfig.getoption("ansys_version"))
    args, _ = _cli_impl(
        exe="AnsysWBU.exe",
        version=version,
        project_file="foo.mechdb",
        graphical=True,
        readonly=True,
    )
    assert "-readonly" in args


@pytest.mark.cli
def test_cli_script(disable_cli, pytestconfig):
    """Test for CLI script argument."""
    version = int(pytestconfig.getoption("ansys_version"))
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=version, input_script="foo.py", graphical=True)
    assert "-script" in args
    assert "foo.py" in args


@pytest.mark.cli
def test_cli_scriptargs(disable_cli, pytestconfig):
    """Test for CLI scriptargs argument."""
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
    """Test for CLI scriptargs argument without script."""
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
    """Test for CLI scriptargs argument with single quotes."""
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
    """Test for CLI scriptargs argument with double quotes."""
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
    """Test for CLI features argument."""
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
    """Test for CLI exit argument."""
    version = int(pytestconfig.getoption("ansys_version"))

    args, _ = _cli_impl(exe="AnsysWBU.exe", version=version, exit=True, port=11)
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
    """Test for CLI batch required arguments."""
    # ansys-mechanical -r <version> => exception
    with pytest.raises(Exception):
        _cli_impl(exe="AnsysWBU.exe", version=max(SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS))

    # ansys-mechanical -r <version> -g => no exception
    try:
        _cli_impl(
            exe="AnsysWBU.exe", version=max(SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS), graphical=True
        )
    except Exception as e:
        assert False, f"cli raised an exception: {e}"

    # ansys-mechanical -r <version> -i input.py => no exception
    try:
        _cli_impl(
            exe="AnsysWBU.exe",
            version=max(SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS),
            input_script="input.py",
        )
    except Exception as e:
        assert False, f"cli raised an exception: {e}"

    # ansys-mechanical -r <version> -port 11 => no exception
    try:
        _cli_impl(
            exe="AnsysWBU.exe",
            version=max(SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS),
            port=11,
            transport_mode="insecure",
        )
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
def test_ideconfig_cli_ide_exception(pytestconfig):
    """Test IDE configuration raises an exception for anything but vscode."""
    revision = int(pytestconfig.getoption("ansys_version"))
    unsupported_ide = "pycharm"

    # Set up the runner for click
    runner = CliRunner()
    result = runner.invoke(
        ideconfig_cli, ["--ide", unsupported_ide, "--target", "user", "--revision", str(revision)]
    )

    assert result.exception is not None
    assert f"{unsupported_ide} is not supported at the moment" in result.exception.args[0]


@pytest.mark.cli
@pytest.mark.embedding
@pytest.mark.version_range(MIN_STUBS_REVN, MAX_STUBS_REVN)
@pytest.mark.parametrize("target", ["user", "workspace"])
def test_ideconfig_cli_settings_added(pytestconfig, tmp_path, monkeypatch, target):
    """Test settings are added without overwriting unrelated settings."""
    revision = int(pytestconfig.getoption("ansys_version"))
    stubs_location = get_stubs_location()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("APPDATA", str(tmp_path))
    monkeypatch.setenv("HOME", str(tmp_path))
    settings_json = (
        get_settings_location() if target == "user" else tmp_path / ".vscode" / "settings.json"
    )
    settings_json.parent.mkdir(parents=True, exist_ok=True)
    settings_json.write_text('{"editor.tabSize": 4}', encoding="utf-8")

    result = CliRunner().invoke(
        ideconfig_cli, ["--ide", "vscode", "--target", target, "--revision", str(revision)]
    )
    stdout = result.output.replace("\\\\", "\\")
    settings_data = json.loads(settings_json.read_text(encoding="utf-8"))

    assert result.exit_code == 0
    assert f"Updated {settings_json} with the following information" in stdout
    assert str(stubs_location) in stdout
    if target == "workspace":
        assert "Please ensure the .vscode folder is in the root" in stdout
    assert settings_data == {
        "editor.tabSize": 4,
        "python.autoComplete.extraPaths": [str(stubs_location / f"v{revision}")],
        "python.analysis.extraPaths": [str(stubs_location / f"v{revision}")],
    }


@pytest.mark.cli
@pytest.mark.embedding
@pytest.mark.parametrize("target", ["user", "workspace"])
def test_ideconfig_cli_settings_already_added(tmp_path, monkeypatch, target):
    """Test repeated configuration reports existing settings without rewriting them."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("APPDATA", str(tmp_path))
    monkeypatch.setenv("HOME", str(tmp_path))
    settings_json = (
        get_settings_location() if target == "user" else tmp_path / ".vscode" / "settings.json"
    )
    runner = CliRunner()
    arguments = ["--target", target, "--revision", str(MAX_STUBS_REVN)]
    first_result = runner.invoke(ideconfig_cli, arguments)
    assert first_result.exit_code == 0
    original_text = settings_json.read_text(encoding="utf-8") + "\n"
    settings_json.write_text(original_text, encoding="utf-8")

    result = runner.invoke(ideconfig_cli, arguments)

    assert result.exit_code == 0
    assert "settings have already been added" in result.output
    assert "Updated" not in result.output
    assert settings_json.read_text(encoding="utf-8") == original_text


@pytest.mark.cli
@pytest.mark.embedding
@pytest.mark.parametrize(
    "existing_key", ["python.autoComplete.extraPaths", "python.analysis.extraPaths"]
)
@pytest.mark.parametrize("existing_is_list", [False, True])
@pytest.mark.parametrize("existing_has_path", [False, True])
def test_ideconfig_cli_settings_partially_added(
    tmp_path, monkeypatch, existing_key, existing_is_list, existing_has_path
):
    """Test incomplete settings gain missing paths without duplicating existing paths."""
    monkeypatch.chdir(tmp_path)
    settings_json = tmp_path / ".vscode" / "settings.json"
    settings_json.parent.mkdir()
    stubs_path = str(STUBS_LOC / f"v{MAX_STUBS_REVN}")
    other_path = str(tmp_path / "other-stubs")
    existing_paths = [other_path, stubs_path] if existing_has_path else [other_path]
    existing_value = existing_paths if existing_is_list else existing_paths[-1]
    settings_json.write_text(
        json.dumps({"editor.tabSize": 4, existing_key: existing_value}), encoding="utf-8"
    )

    result = CliRunner().invoke(
        ideconfig_cli, ["--target", "workspace", "--revision", str(MAX_STUBS_REVN)]
    )
    settings_data = json.loads(settings_json.read_text(encoding="utf-8"))

    assert result.exit_code == 0
    assert "Updated" in result.output
    assert "settings have already been added" not in result.output
    expected_data = {
        "editor.tabSize": 4,
        "python.autoComplete.extraPaths": [stubs_path],
        "python.analysis.extraPaths": [stubs_path],
    }
    expected_data[existing_key] = (
        [other_path, stubs_path] if existing_is_list or not existing_has_path else [stubs_path]
    )
    assert settings_data == expected_data


@pytest.mark.cli
@pytest.mark.embedding
@pytest.mark.parametrize("target", ["user", "workspace"])
@pytest.mark.parametrize("existing_kind", ["string", "list", "multiple", "current_first"])
def test_ideconfig_cli_settings_version_changed(tmp_path, monkeypatch, target, existing_kind):
    """Test revision changes replace existing stubs paths and report the requested version."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("APPDATA", str(tmp_path))
    monkeypatch.setenv("HOME", str(tmp_path))
    settings_json = (
        get_settings_location() if target == "user" else tmp_path / ".vscode" / "settings.json"
    )
    settings_json.parent.mkdir(parents=True, exist_ok=True)
    old_revision = MIN_STUBS_REVN if MIN_STUBS_REVN != MAX_STUBS_REVN else MAX_STUBS_REVN - 1
    old_path = str(STUBS_LOC / f"v{old_revision}")
    requested_path = str(STUBS_LOC / f"v{MAX_STUBS_REVN}")
    unrelated_path = str(tmp_path / "other-stubs")
    other_installation = str(tmp_path / "other-env" / "ansys" / "mechanical" / "stubs" / "v252")
    existing_values = {
        "string": old_path,
        "list": [unrelated_path, old_path, other_installation],
        "multiple": [unrelated_path, old_path, requested_path, old_path, other_installation],
        "current_first": [unrelated_path, requested_path, old_path, other_installation],
    }
    settings_json.write_text(
        json.dumps(
            {
                "editor.tabSize": 4,
                "python.autoComplete.extraPaths": existing_values[existing_kind],
                "python.analysis.extraPaths": existing_values[existing_kind],
            }
        ),
        encoding="utf-8",
    )
    runner = CliRunner()
    arguments = ["--target", target, "--revision", str(MAX_STUBS_REVN)]

    result = runner.invoke(ideconfig_cli, arguments)
    settings_data = json.loads(settings_json.read_text(encoding="utf-8"))

    expected_paths = (
        [requested_path]
        if existing_kind == "string"
        else [unrelated_path, requested_path, other_installation]
    )
    assert result.exit_code == 0
    assert f"Updated the autocomplete path to version {MAX_STUBS_REVN}" in result.output
    assert settings_data == {
        "editor.tabSize": 4,
        "python.autoComplete.extraPaths": expected_paths,
        "python.analysis.extraPaths": expected_paths,
    }


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

    # Get the version from the Mechanical executable
    exe = atp.get_mechanical_path(allow_input=False, version=revision)
    if exe:
        exe_version = atp.version_from_path("mechanical", exe)
        assert str(exe_version) in stdout

    assert str(settings_json_fragment) in stdout
    assert venv_loc in stdout


@pytest.mark.cli
def test_ideconfig_revision_max_min(tmp_path, monkeypatch):
    """Test the IDE configuration location when no arguments are supplied."""
    monkeypatch.setenv("APPDATA", str(tmp_path))
    monkeypatch.setenv("HOME", str(tmp_path))
    # Set the revision number to be greater than the maximum stubs revision number
    stubs_location = get_stubs_location()
    # Get the path to the settings.json file based on operating system env vars
    settings_json = get_settings_location()

    # Set the revision number to be greater than the maximum stubs revision number
    gt_max_revision = MAX_STUBS_REVN + 10
    # Set the revision number to be less than the minimum stubs revision number
    lt_min_revision = MIN_STUBS_REVN - 10

    # Set up the runner for click
    runner = CliRunner()

    # Assert a warning is raised when the revision is greater than the maximum version in the stubs
    with pytest.warns(UserWarning):
        result = runner.invoke(
            ideconfig_cli,
            ["--ide", "vscode", "--target", "user", "--revision", str(gt_max_revision)],
        )
        stdout = result.output.replace("\\\\", "\\")

        assert result.exit_code == 0
        assert f"Updated {settings_json} with the following information" in stdout
        assert str(stubs_location) in stdout
        assert str(MAX_STUBS_REVN) in stdout

    # Assert an exception is raised when the revision is less than the minimum version in the stubs
    result = runner.invoke(
        ideconfig_cli, ["--ide", "vscode", "--target", "user", "--revision", str(lt_min_revision)]
    )
    assert result.exception is not None
    assert f"PyMechanical Stubs are not available for {lt_min_revision}" in result.exception.args[0]


@pytest.mark.cli
def test_ideconfig_no_revision(tmp_path, monkeypatch):
    """Test the IDE configuration when no revision is supplied."""
    monkeypatch.setenv("APPDATA", str(tmp_path))
    monkeypatch.setenv("HOME", str(tmp_path))
    # Set the revision number to be greater than the maximum stubs revision number
    stubs_location = get_stubs_location()
    # Get the path to the settings.json file based on operating system env vars
    settings_json = get_settings_location()

    # Set the runner for click
    runner = CliRunner()
    result = runner.invoke(ideconfig_cli, ["--ide", "vscode", "--target", "user"])
    stdout = result.output.replace("\\\\", "\\")

    assert result.exit_code == 0
    assert f"Updated {settings_json} with the following information" in stdout
    assert str(stubs_location) in stdout


@pytest.mark.cli
def test_cli_engine_type_args(disable_cli, pytestconfig):
    """Test engine type selection arguments."""
    # Must specify version and transport_mode when using port to avoid SP04 check errors
    args, _ = _cli_impl(exe="AnsysWBU.exe", port=11, version=261, transport_mode="insecure")
    assert "-engineType" not in args

    # Select ironpython engine type
    args, _ = _cli_impl(exe="AnsysWBU.exe", enginetype="ironpython", input_script="foo.py")
    assert "-engineType" in args
    assert "ironpython" in args

    # Select cpython engine type
    args, _ = _cli_impl(exe="AnsysWBU.exe", enginetype="cpython", input_script="foo.py")
    assert "-engineType" in args
    assert "cpython" in args


@pytest.mark.cli
@pytest.mark.embedding
@pytest.mark.parametrize(
    ("options", "expected_error"),
    [
        pytest.param(
            {"enginetype": "invalid_engine", "input_script": "foo.py"},
            "Invalid engine type",
            id="invalid-engine",
        ),
        pytest.param(
            {"enginetype": "cpython"},
            "Cannot specify engine type without an input script",
            id="engine-without-script",
        ),
    ],
)
def test_cli_engine_type_invalid_options(disable_cli, pytestconfig, options, expected_error):
    """Test invalid engine options produce the appropriate validation error."""
    version = int(pytestconfig.getoption("ansys_version"))
    with pytest.raises(Exception, match=expected_error):
        _cli_impl(exe="AnsysWBU.exe", version=version, **options)


@pytest.mark.cli
@pytest.mark.embedding
def test_cli_enginetype_unsupported_version(disable_cli, monkeypatch):
    """Test CPython engine selection is rejected before version 261."""
    version = max(version for version in SUPPORTED_MECHANICAL_EMBEDDING_VERSIONS if version < 261)
    monkeypatch.setattr(atp, "get_mechanical_path", lambda **kwargs: "AnsysWBU.exe")
    monkeypatch.setattr(atp, "version_from_path", lambda product, path: version)

    result = CliRunner().invoke(
        cli,
        ["--revision", str(version), "--input-script", "foo.py", "--enginetype", "cpython"],
    )

    assert result.exit_code != 0
    assert (
        "--enginetype option for cpython is only applicable for version 261 or later."
        in result.output
    )
