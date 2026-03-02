# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Test cases for background app."""

import sys
import time

from ansys.mechanical.core.embedding.background import BackgroundApp


def _print_to_stderr(*args):
    msg = " ".join(map(str, args)) + "\n"
    sys.stderr.write(msg)


def multiple_instances(version):
    """Use multiple instances of BackgroundApp."""
    s = BackgroundApp(version=version)

    def func():
        return s.app.DataModel.Project.Name

    _print_to_stderr(s.post(func), "1")
    time.sleep(0.03)
    _print_to_stderr(s.post(func), "2")

    def new():
        s.app.new()
        s.app.DataModel.Project.Name = "Foo"
        return s.app.DataModel.Project.Name

    _print_to_stderr(s.post(new), "3")

    del s
    s = BackgroundApp(version=version)
    _print_to_stderr(s.post(func), "4")

    s.stop()


def test_background_app_use_stopped(version):
    """Stop background app then try to use it."""
    s = BackgroundApp(version=version)

    def func():
        return s.app.DataModel.Project.Name

    s.post(func)
    s.stop()
    s.post(func)


def test_background_app_initialize_stopped(version):
    """Stop background app then try to use it."""
    s = BackgroundApp(version=version)

    def func():
        return s.app.DataModel.Project.Name

    s.post(func)
    s.stop()
    del s
    s = BackgroundApp(version=version)


if __name__ == "__main__":
    version = sys.argv[1]
    test_name = sys.argv[2]
    tests = {
        "multiple_instances": multiple_instances,
        "test_background_app_use_stopped": test_background_app_use_stopped,
        "test_background_app_initialize_stopped": test_background_app_initialize_stopped,
    }
    tests[test_name](int(version))
    print("@@success@@")
    sys.exit(0)
