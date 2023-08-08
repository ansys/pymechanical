"""Runtime initialize for pythonnet in embedding."""
from ansys.mechanical.core.embedding import loader


def __initialize_runtime_pythonnet_3():
    """Add the codecs that are in python3.

    These are needed for many things, including
    Mechanical's list conversions (python list to C# lists).
    """
    import Python.Runtime.Codecs as codecs

    codecs.ListDecoder.Instance.Register()
    codecs.SequenceDecoder.Instance.Register()
    codecs.IterableDecoder.Instance.Register()
    # TODO - FunctionCodec


def initialize(version: int) -> None:
    """Initialize the runtime.

    Pythonnet is already initialized but we need to
    do some special codec handling to make sure the
    interop works well for Mechanical.
    """
    __initialize_runtime_pythonnet_3()
