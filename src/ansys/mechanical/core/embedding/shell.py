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

import os
import sys
import warnings

import ansys.mechanical.core.embedding.ipython_shell as ipython_shell
import ansys.mechanical.core.embedding.utils as embedding_utils

try:
    import pythoncom

    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

def _install_drain_tracer() -> None:
    """Optional."""
    warnings.warn("""Mechanical UI without blocking python.
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

def _uninstall_drain_tracer() -> None:
    sys.settrace(None)

def _use_drain_tracer():
    return os.environ.get("ANSYS_MECHANICAL_EMBEDDING_UI_DRAIN_TRACER") == "1"

def start_interactive_shell(app):
    if ipython_shell.in_ipython():
        if not HAS_WIN32:
            warnings.warn("""Interactive PyMechanical requires pywin32""")
            return
        ipython_shell.get_shell_hooks().idle_hook = lambda: embedding_utils.sleep(50)
        ipython_shell.get_shell_hooks().end_hook = lambda: app._dispose()
    else:
        if _use_drain_tracer():
            _install_drain_tracer()
        else:
            warnings.warn("""Interactive PyMechanical is used without IPython.
                          The main thread will be held by python, and therefore
                          the mechanical UI will not be responsive""")

def end_interactive_shell():
    if ipython_shell.in_ipython():
        if not HAS_WIN32:
            return
        ipython_shell.get_shell_hooks().idle_hook = None
    else:
        if _use_drain_tracer():
            _uninstall_drain_tracer()

def initialize_ipython_shell():
    if not ipython_shell.in_ipython():
        return
    if not HAS_WIN32:
        return

    ipython_shell.get_shell_hooks().start_hook = lambda: pythoncom.CoInitialize()
    ipython_shell.post_ipython_blocks()
    #ipython_shell.get_shell_hooks().end_hook = lambda: print("DSFKSJDFSFJK")
