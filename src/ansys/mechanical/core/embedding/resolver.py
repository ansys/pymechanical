# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Provides the .NET assembly resolving for embedding Ansys Mechanical.

Note that for some Mechanical Addons - additional resolving may be
necessary. A resolve handler is shipped with Ansys Mechanical on Windows
starting in version 23.1 and on Linux starting in version 23.2
"""

from pathlib import Path
import sys


def _sys_path_has_shadow_ansys_dir(path_entry: str) -> bool:
    """Check whether *path_entry* contains a subdirectory named exactly ``Ansys``.

    Such a folder is imported as a namespace package and shadows the CLR
    ``Ansys`` module from ``clr.AddReference``, causing
    ``module 'Ansys' has no attribute 'Mechanical'``.

    Only the exact spelling ``Ansys`` is treated as a shadow so
    ``site-packages/ansys`` is not removed from ``sys.path``.
    """
    base = Path(path_entry) if path_entry else Path.cwd()
    try:
        if not base.is_dir():
            return False
        return any(p.is_dir() and p.name == "Ansys" for p in base.iterdir())
    except OSError:
        return False


def resolve(version):
    """Resolve function for all versions of Ansys Mechanical."""
    import clr  # isort: skip
    import System  # isort: skip

    clr.AddReference("Ansys.Mechanical.Embedding")

    _original_sys_path = sys.path[:]
    try:
        sys.path[:] = [p for p in sys.path if not _sys_path_has_shadow_ansys_dir(p)]
        import Ansys  # isort: skip
    finally:
        sys.path[:] = _original_sys_path

    try:
        assembly_resolver = Ansys.Mechanical.Embedding.AssemblyResolver
        resolve_handler = assembly_resolver.MechanicalResolveEventHandler
        System.AppDomain.CurrentDomain.AssemblyResolve += resolve_handler
    except AttributeError as err:
        error_msg = (
            "Unable to resolve Mechanical assemblies. Please ensure the following:\n"
            "    1. Mechanical is installed.\n"
            '    2. A subdirectory named exactly "Ansys" does not exist on sys.path '
            "(e.g. next to an example script), which shadows the CLR Ansys module.\n"
        )
        raise AttributeError(error_msg) from err
