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

"""Runtime initialize for pythonnet in embedding."""

from importlib.metadata import distribution
import os

from ansys.mechanical.core.embedding.logger import Logger


def __register_container_codecs():
    import Python.Runtime.Codecs as codecs

    codecs.ListDecoder.Instance.Register()
    codecs.SequenceDecoder.Instance.Register()
    codecs.IterableDecoder.Instance.Register()


def __register_function_codec():
    import clr

    clr.AddReference("Ansys.Mechanical.CPython")
    import Ansys

    Ansys.Mechanical.CPython.Codecs.FunctionCodec.Register()


def _bind_assembly(
    assembly_name: str, explicit_interface: bool = False, pep8_aliases: bool = False
) -> None:
    """Bind the assembly for explicit interface and/or PEP 8 aliases.

    Parameters
    ----------
    assembly_name : str
        The name of the assembly to bind.
    explicit_interface : bool, optional
        If True, allows explicit interface implementation. Default is False.
    pep8_aliases : bool, optional
        If True, enables PEP 8 aliases. Default is False.
    """
    # if pythonnet is not installed, we can't bind the assembly
    try:
        distribution("pythonnet")
        Logger.warning("Cannot bind for explicit interface because pythonnet is installed")
        return
    except ModuleNotFoundError:
        pass
    import clr

    Logger.debug(f"Binding assembly {assembly_name}")
    assembly = clr.AddReference(assembly_name)
    from Python.Runtime import BindingManager, BindingOptions

    binding_options = BindingOptions()
    if explicit_interface:
        Logger.debug(f"Binding explicit interface for {assembly_name}")
        binding_options.AllowExplicitInterfaceImplementation = True
    if pep8_aliases:
        Logger.debug(f"Setting PEP 8 aliases for {assembly_name}")
        binding_options.Pep8Aliases = True
    BindingManager.SetBindingOptions(assembly, binding_options)


def initialize(version: int, pep8_aliases: bool = False) -> None:
    """Initialize the runtime.

    Pythonnet is already initialized but we need to
    do some special codec handling to make sure the
    interop works well for Mechanical. These are
    need to handle (among other things) list and other
    container conversions between C# and python
    """
    Logger.info("Initialize pythonnet interop handling")
    __register_container_codecs()
    if version >= 242 or os.name == "nt":
        # function codec is distributed with pymechanical on linux only
        # at version 242 or later
        Logger.debug("Registering function codec")
        __register_function_codec()
        Logger.debug("Registered function codec")

    explicit_interface = True

    if os.environ.get("PYMECHANICAL_EXPLICIT_INTERFACE") == "0":
        explicit_interface = False

    # TODO: When the PEP 8 aliases option is enabled (True by default),
    # keep three environment variables to turn explicit, PEP 8, and both off.

    _bind_assembly(
        "Ansys.ACT.WB1", explicit_interface=explicit_interface, pep8_aliases=pep8_aliases
    )
