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

"""clr_loader for pymechanical embedding. This loads the CLR on both windows and linux."""
import os
import warnings


def __get_mono(assembly_dir, config_dir):
    import clr_loader

    libmono = os.path.join(assembly_dir, "libmonosgen-2.0.so")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mono = clr_loader.get_mono(
            set_signal_chaining=True,
            libmono=libmono,  # TODO: find_mono is broken on clr-loader v0.2.6
            assembly_dir=assembly_dir,
            config_dir=config_dir,
        )
    return mono


def _set_mono_trace():  # pragma: no cover
    if "ANS_MONO_TRACE" in os.environ:
        os.environ["MONO_LOG_LEVEL"] = "message"
        os.environ["MONO_LOG_MASK"] = "all"


def _load_mono(install_loc):
    """Load the clr using mono that is shipped with the unified install."""
    from pythonnet import load

    _set_mono_trace()
    mono_dir = os.path.join(install_loc, "Tools", "mono", "Linux64")
    assembly_dir = os.path.join(mono_dir, "lib")
    config_dir = os.path.join(mono_dir, "etc")
    mono = __get_mono(assembly_dir, config_dir)
    load(mono)


def load_clr(install_loc: str) -> None:
    """Load the clr, the outcome of this function is that `clr` is usable."""
    if os.name == "nt":  # pragma: no cover
        return
    _load_mono(install_loc)
