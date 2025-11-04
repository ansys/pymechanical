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

"""Module for scheduling background work in IPython shells.

Interactive Python, or IPython, offers an enhanced Python shell. This module
schedules all the work of the IPython shell on a background thread, allowing
the Main thread to be used exclusively for the shell frontend. As a result,
user-defined functions can be executed during idle time between blocks.
"""

import queue
import threading
import time

from ansys.mechanical.core import LOG

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
EXECUTION_THREAD_ID: int = None

DEFAULT_IDLE_HOOK = lambda: time.sleep(0.05)

class ShellHooks:
    """IPython shell lifetime hooks."""

    def __init__(self):
        self._idle_hook: callable = DEFAULT_IDLE_HOOK
        self._start_hook: callable = None
        self._end_hook: callable = None

    @property
    def idle_hook(self) -> callable:
        """Function to call between IPython block executions."""
        return self._idle_hook

    @idle_hook.setter
    def idle_hook(self, value: callable) -> None:
        self._idle_hook = value

    @property
    def start_hook(self) -> callable:
        """Function to call at the start of the block thread."""
        return self._start_hook

    @start_hook.setter
    def start_hook(self, value: callable) -> None:
        self._start_hook = value

    @property
    def end_hook(self) -> callable:
        """Function to call when the shell is exited."""
        return self._end_hook

    @end_hook.setter
    def end_hook(self, value: callable) -> None:
        self._end_hook = value

    def start(self):
        if self.start_hook is not None:
            self._start_hook()

    def idle(self):
        if self.idle_hook is not None:
            self._idle_hook()

    def end(self):
        if self.end_hook is not None:
            self._end_hook()

SHELL_HOOKS = ShellHooks()

def _execution_thread_main():
    global APP_INIT_EVENT
    global CODE_QUEUE
    global EXECUTION_THREAD_ID
    global ORIGINAL_RUN_CELL
    global RESULT_QUEUE
    global SHUTDOWN_EVENT
    global SHELL_HOOKS

    SHELL_HOOKS.start()
    shell = InteractiveShell.instance()
    EXECUTION_THREAD_ID = threading.get_ident()
    while not SHUTDOWN_EVENT.is_set():
        try:
            code = CODE_QUEUE.get_nowait()
        except queue.Empty:
            # call the idle hook
            try:
                SHELL_HOOKS.idle()
            except Exception as e:
                LOG.error(f"shell hook raised {e}. Uninstalling it.")
                SHELL_HOOKS.idle_hook = DEFAULT_IDLE_HOOK
            continue
        if code is None:
            SHELL_HOOKS.end()
            break
        LOG.info(f"execution thread {threading.get_ident()}")
        result = ORIGINAL_RUN_CELL(shell, code, store_history=True)
        RESULT_QUEUE.put(result)
        SHELL_HOOKS.end()


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
    LOG.info("Shutting down execution thread")
    SHUTDOWN_EVENT.set()
    CODE_QUEUE.put(None)  # Unblock the thread
    EXEC_THREAD.join(timeout=1)


def _can_post_ipython_blocks():
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


def get_shell_hooks():
    global SHELL_HOOKS
    return SHELL_HOOKS
