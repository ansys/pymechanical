"""pymechanical specific errors."""

from functools import wraps
import signal
import threading

from grpc._channel import _InactiveRpcError, _MultiThreadedRendezvous

from ansys.mechanical.core import LOG as logger

SIGINT_TRACKER = []


class VersionError(ValueError):
    """Raise when Mechanical is the wrong version."""

    def __init__(self, msg="Invalid Mechanical version"):
        """Initialize the VersionError.

        Parameters
        ----------
        msg : str
            Use the message describe about the invalid Mechanical version
        """
        ValueError.__init__(self, msg)


class MechanicalRuntimeError(RuntimeError):
    """Raise when Mechanical passes an error."""

    pass


class MechanicalExitedError(RuntimeError):
    """Raise when Mechanical has exited."""

    def __init__(self, msg="Mechanical has exited"):
        """Initialize the MechanicalExitedError.

        Parameters
        ----------
        msg: str
            use the message to describe about the Mechanical exited error.
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

    This works some of the time, but not all the time.  For some
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
        except (_InactiveRpcError, _MultiThreadedRendezvous) as error:
            # can't use isinstance here due to circular imports
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
                # TODO: compare this with MAPDL
                # mechanical._close_process()
                mechanical.exit(force=True)

            raise MechanicalExitedError("Mechanical server connection terminated") from None

        if threading.current_thread().__class__.__name__ == "_MainThread":
            received_interrupt = bool(SIGINT_TRACKER)

            # always clear and revert to old handler
            SIGINT_TRACKER.clear()
            if old_handler:
                signal.signal(signal.SIGINT, old_handler)

            if received_interrupt:  # pragma: no cover
                raise KeyboardInterrupt("Interrupted during Mechanical execution")

        return out

    return wrapper
