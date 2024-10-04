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

"""PyMechanical-specific errors."""

from functools import wraps
import signal
import threading

from grpc._channel import _InactiveRpcError, _MultiThreadedRendezvous

from ansys.mechanical.core import LOG as logger

SIGINT_TRACKER = []
"""List of SIGINT keyboard interrupts."""


class VersionError(ValueError):
    """Raises an error when the version of Mechanical is invalid."""

    def __init__(self, msg="Invalid Mechanical version"):
        """Initialize the version error.

        Parameters
        ----------
        msg : str
            Error message to display for an invalid version of Mechanical.
        """
        ValueError.__init__(self, msg)


class MechanicalRuntimeError(RuntimeError):
    """Raises an error when Mechanical passes a runtime error."""

    pass


class MechanicalExitedError(RuntimeError):
    """Raises an error when Mechanical has exited."""

    def __init__(self, msg="Mechanical has exited."):
        """Initialize the MechanicalExitedError.

        Parameters
        ----------
        msg: str
            Error message to display when Mechanical has exited.
        """
        RuntimeError.__init__(self, msg)


# handler for protect_grpc
def handler(sig, frame):  # pragma: no cover
    """Pass signal to custom interrupt handler."""
    logger.info("KeyboardInterrupt received.  Waiting until Mechanical " "execution finishes")
    SIGINT_TRACKER.append(True)


def protect_grpc(func):
    """Capture gRPC exceptions and return a more succinct error message.

    Capture KeyboardInterrupt to avoid segfaulting Mechanical.

    This works some of the time, but not all the time. For some
    reason gRPC still captures SIGINT.

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Capture gRPC exceptions and KeyboardInterrupt."""
        # capture KeyboardInterrupt
        old_handler = None
        if threading.current_thread().__class__.__name__ == "_MainThread":
            if threading.current_thread().is_alive():
                old_handler = signal.signal(signal.SIGINT, handler)

        # Capture gRPC exceptions
        try:
            out = func(*args, **kwargs)
        except (_InactiveRpcError, _MultiThreadedRendezvous) as error:  # pragma: no cover
            # Can't use isinstance here due to circular imports
            try:
                class_name = args[0].__class__.__name__
            except:
                class_name = ""

            mechanical = None

            if class_name == "Mechanical":
                mechanical = args[0]
            elif hasattr(args[0], "_mechanical"):
                mechanical = args[0]._mechanical

            # Must close unfinished processes
            if mechanical is not None:
                mechanical.exit(force=True)

            raise MechanicalExitedError("Mechanical server connection terminated.") from None

        if threading.current_thread().__class__.__name__ == "_MainThread":
            received_interrupt = bool(SIGINT_TRACKER)

            # Always clear and revert to old handler
            SIGINT_TRACKER.clear()
            if old_handler:
                signal.signal(signal.SIGINT, old_handler)

            if received_interrupt:  # pragma: no cover
                raise KeyboardInterrupt("Interrupted during Mechanical execution.")

        return out

    return wrapper
