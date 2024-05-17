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

import pytest

from ansys.mechanical.core.run import _cli_impl


@pytest.mark.cli
def test_cli_default(disable_cli):
    args, env = _cli_impl(exe="AnsysWBU.exe", version=241)
    assert os.environ == env
    assert "-AppModeMech" in args
    assert "-b" in args
    assert "-DSApplet" in args
    assert "AnsysWBU.exe" in args


@pytest.mark.cli
def test_cli_debug(disable_cli):
    _, env = _cli_impl(exe="AnsysWBU.exe", version=241, debug=True)
    assert "WBDEBUG_STOP" in env


@pytest.mark.cli
def test_cli_graphical(disable_cli):
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, graphical=True)
    assert "-b" not in args


@pytest.mark.cli
def test_cli_appdata(disable_cli):
    _, env = _cli_impl(exe="AnsysWBU.exe", version=241, private_appdata=True)
    assert os.environ["TEMP"] != env["TEMP"]


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
def test_cli_232(disable_cli):
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=231)
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
def test_cli_features(disable_cli):
    with pytest.warns(UserWarning):
        args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, features="a;b;c")
        assert "-featureflags" in args
        assert "a;b;c" in args
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, features="MultistageHarmonic")
    assert "Mechanical.MultistageHarmonic" in args


@pytest.mark.cli
def test_cli_exit(disable_cli):

    # Regardless of version, `exit` does nothing on its own
    args, _ = _cli_impl(exe="AnsysWBU.exe", version=232, exit=True)
    assert "-x" not in args

    args, _ = _cli_impl(exe="AnsysWBU.exe", version=241, exit=True)
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