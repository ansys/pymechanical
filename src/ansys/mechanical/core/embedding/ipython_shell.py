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

"""Interactive IPython shell for embedding."""

import queue
import threading
import time

from ansys.mechanical.core import LOG

try:
    import pythoncom

    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

try:
    from IPython.core.interactiveshell import InteractiveShell

    HAS_IPYTHON = True
except ImportError:
    HAS_IPYTHON = False

CODE_QUEUE = queue.Queue()
RESULT_QUEUE = queue.Queue()
SHUTDOWN_EVENT = threading.Event()
APP_INIT_EVENT = threading.Event()
EXEC_THREAD = None
ORIGINAL_RUN_CELL = None
SHELL_HOOK: callable = None
EXECUTION_THREAD_ID: int = None


def _execution_thread_main():
    global APP_INIT_EVENT
    global CODE_QUEUE
    global EXECUTION_THREAD_ID
    global ORIGINAL_RUN_CELL
    global RESULT_QUEUE
    global SHUTDOWN_EVENT
    global SHELL_HOOK
    pythoncom.CoInitialize()
    shell = InteractiveShell.instance()
    EXECUTION_THREAD_ID = threading.get_ident()
    while not SHUTDOWN_EVENT.is_set():
        try:
            code = CODE_QUEUE.get_nowait()
        except queue.Empty:
            # Spin with short sleep
            if SHELL_HOOK is None:
                time.sleep(0.05)
            else:
                try:
                    SHELL_HOOK()
                except Exception as e:
                    LOG.error(f"shell hook raised {e}. Uninstalling it.")
                    SHELL_HOOK = None
            continue
        if code is None:
            break
        LOG.info(f"execution thread {threading.get_ident()}")
        result = ORIGINAL_RUN_CELL(shell, code, store_history=True)
        RESULT_QUEUE.put(result)


def _run_cell_in_thread(self, raw_cell, store_history=False, silent=False, shell_futures=True):
    global CODE_QUEUE
    global RESULT_QUEUE
    global SHUTDOWN_EVENT
    CODE_QUEUE.put(raw_cell)
    while not SHUTDOWN_EVENT.is_set():
        try:
            return RESULT_QUEUE.get(timeout=0.1)
        except queue.Empty:
            continue
    raise RuntimeError("Execution thread shut down before result was returned.")


def _cleanup():
    global CODE_QUEUE
    global SHUTDOWN_EVENT
    global EXEC_THREAD
    print("Shutting down execution thread")
    SHUTDOWN_EVENT.set()
    CODE_QUEUE.put(None)  # Unblock the thread
    EXEC_THREAD.join(timeout=1)


def _can_post_ipython_blocks():
    if not HAS_WIN32:
        raise Exception("`post_ipython_blocks` requires pywin32")
    if not HAS_IPYTHON:
        raise Exception("`post_ipython_blocks` requires ipython")


def in_ipython():
    if not HAS_IPYTHON:
        return False
    from IPython import get_ipython

    return get_ipython() is not None


# Capture the original run_cell before patching
def post_ipython_blocks():
    _can_post_ipython_blocks()
    global EXEC_THREAD
    global ORIGINAL_RUN_CELL
    LOG.info(f"original main thread {threading.get_ident()}")
    ORIGINAL_RUN_CELL = InteractiveShell.run_cell
    EXEC_THREAD = threading.Thread(target=_execution_thread_main, daemon=True)
    EXEC_THREAD.start()

    import atexit

    atexit.register(_cleanup)
    # Patch IPython to delegate to your thread
    InteractiveShell.run_cell = _run_cell_in_thread.__get__(
        InteractiveShell.instance(), InteractiveShell
    )

    LOG.info("IPython now runs all cells in your dedicated thread.")


def install_shell_hook(hook):
    global SHELL_HOOK
    SHELL_HOOK = hook


def try_post_ipython_blocks():
    if in_ipython():
        post_ipython_blocks()


def is_in_interactive_thread():
    global EXECUTION_THREAD_ID
    if EXECUTION_THREAD_ID is None:
        return False
    return EXECUTION_THREAD_ID == threading.get_ident()
