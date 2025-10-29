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

"""Shell interaction for PyMechanical embedding."""

import sys
import warnings


def _start_nonblocking_ui_no_ipython(app) -> None:
    warnings.warn("""Starting the UI without blocking.
                  The UI will be stuck while python is executing, except during
                  non-blocking sleeps. To use a non-blocking sleep, run
                  `import ansys.mechanical.core.embedding.utils`
                  `ansys.mechanical.core.embedding.utils.sleep(ms)`
                  or, use app.wait_with_dialog() to open a dialog box that
                  will block the python interpreter but keep the UI
                  responsive.""")

    def tracer(frame, event, arg):
        if event == "line":
            from ansys.mechanical.core.embedding.utils import drain

            drain()
        return tracer

    sys.settrace(tracer)
    app.ExtAPI.Application.StartUI(False)


def _start_nonblocking_ui_ipython(app) -> None:
    """"""
    from ansys.mechanical.core.embedding.ipython_shell import install_shell_hook
    from ansys.mechanical.core.embedding.utils import sleep

    install_shell_hook(lambda: sleep(50))
    app.ExtAPI.Application.StartUI(False)


def start_nonblocking_ui(app) -> None:
    """Start the ui without blocking"""
    from ansys.mechanical.core.embedding.ipython_shell import in_ipython, is_in_interactive_thread

    if not in_ipython():
        _start_nonblocking_ui_no_ipython(app)
        return
    if not is_in_interactive_thread():
        raise Exception("Cannot start nonblocking UI from IPython when not in interactive thread.")
    _start_nonblocking_ui_ipython(app)
