"""Runtime initialize for pythonnet in embedding."""


def initialize() -> None:
    """Initialize the runtime.

    Pythonnet is already initialized but we need to
    do some special codec handling to make sure the
    interop works well for Mechanical. These are
    need to handle (among other things) list and other
    container conversions between C# and python
    """
    import Python.Runtime.Codecs as codecs

    codecs.ListDecoder.Instance.Register()
    codecs.SequenceDecoder.Instance.Register()
    codecs.IterableDecoder.Instance.Register()
    # TODO - FunctionCodec
