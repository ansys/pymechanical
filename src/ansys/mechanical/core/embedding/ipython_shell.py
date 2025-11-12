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
    from IPython import get_ipython
    from IPython.core.interactiveshell import InteractiveShell

    FROM_IPYTHON = get_ipython() is not None
    HAS_IPYTHON = True
except ImportError:
    FROM_IPYTHON = False
    HAS_IPYTHON = False

CODE_QUEUE = queue.Queue()
RESULT_QUEUE = queue.Queue()
SHUTDOWN_EVENT = threading.Event()
EXEC_THREAD = None
ORIGINAL_RUN_CELL = None
EXECUTION_THREAD_ID: int = None


def _idle_sleep():
    time.sleep(0.01)


DEFAULT_IDLE_HOOK = _idle_sleep


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
        """Signal handler when the shell starts."""
        if self.start_hook is not None:
            self._start_hook()
            self._start_hook = None

    def idle(self):
        """Signal handler when the shell is idle."""
        if self.idle_hook is not None:
            self._idle_hook()

    def end(self):
        """Signal handler when the shell ends."""
        if self.end_hook is not None:
            self._end_hook()
            self._end_hook = None


SHELL_HOOKS = ShellHooks()


def _exec_from_queue(shell) -> bool:
    """Worker function for ipython execution.

    Return whether to break out of loop
    """
    try:
        code = CODE_QUEUE.get_nowait()
    except queue.Empty:
        # call the idle hook
        try:
            SHELL_HOOKS.idle()
        except Exception as e:
            LOG.error(f"shell hook raised {e}. Uninstalling it.")
            SHELL_HOOKS.idle_hook = DEFAULT_IDLE_HOOK
        return False
    if code is None:
        return True
    LOG.info(f"execution thread {threading.get_ident()}")
    result = ORIGINAL_RUN_CELL(shell, code, store_history=True)
    RESULT_QUEUE.put(result)
    return False


def _execution_thread_main():
    global EXECUTION_THREAD_ID

    SHELL_HOOKS.start()
    shell = InteractiveShell.instance()
    EXECUTION_THREAD_ID = threading.get_ident()
    while not SHUTDOWN_EVENT.is_set():
        if _exec_from_queue(shell):
            break

    # one more execution in case the shutdown event was set and the exit code was not processed?
    if SHELL_HOOKS.end_hook is not None:
        _exec_from_queue(shell)


def _run_cell_in_thread(self, raw_cell, store_history=False, silent=False, shell_futures=True):
    CODE_QUEUE.put(raw_cell)
    while not SHUTDOWN_EVENT.is_set():
        try:
            return RESULT_QUEUE.get(timeout=0.1)
        except queue.Empty:
            continue
    raise RuntimeError("Execution thread shut down before result was returned.")


def cleanup():
    """Cleanup the ipython shell.

    Must be called before the application exits.
    May be called from an atexit handler.
    """
    LOG.info("Shutting down execution thread")
    CODE_QUEUE.put(None)  # Unblock the thread
    SHUTDOWN_EVENT.set()
    EXEC_THREAD.join(timeout=1)


def _can_post_ipython_blocks():
    if not HAS_IPYTHON:
        raise Exception("`post_ipython_blocks` requires ipython")


def in_ipython():
    """Return whether Python is running from IPython."""
    return FROM_IPYTHON


# Capture the original run_cell before patching
def post_ipython_blocks():
    """Initiate the IPython worker thread for block execution."""
    _can_post_ipython_blocks()
    global EXEC_THREAD
    global ORIGINAL_RUN_CELL
    LOG.info(f"original main thread {threading.get_ident()}")
    ORIGINAL_RUN_CELL = InteractiveShell.run_cell
    EXEC_THREAD = threading.Thread(target=_execution_thread_main, daemon=True)
    EXEC_THREAD.start()

    # Patch IPython to delegate to your thread
    InteractiveShell.run_cell = _run_cell_in_thread.__get__(
        InteractiveShell.instance(), InteractiveShell
    )
    LOG.info("IPython now runs all cells in your dedicated thread.")


def get_shell_hooks():
    """Get the shell hooks object."""
    return SHELL_HOOKS
