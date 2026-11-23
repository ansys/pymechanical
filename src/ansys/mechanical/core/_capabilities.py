# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Answer what each Mechanical version supports, in one place."""

from dataclasses import dataclass

_GRPC_SERVICE_PACKS = {242: 5, 251: 4, 252: 3}


@dataclass(frozen=True)
class Capabilities:
    """Provides what a Mechanical version supports.

    Known defects that need a workaround are in
    :class:`~ansys.mechanical.core._limitations.Limitations` instead.

    Examples
    --------
    >>> Capabilities(261).interactive
    True
    >>> Capabilities(252).interactive
    False
    """

    version: int

    @property
    def grpc_launch(self) -> bool:
        """Whether Mechanical can be launched with the gRPC interface.

        Examples
        --------
        >>> Capabilities(232).grpc_launch
        True
        """
        return self.version >= 232

    @property
    def grpc_service_pack(self) -> int | None:
        """Service pack required for secure gRPC options.

        ``0`` means every build supports them, and ``None`` means no build does.

        Examples
        --------
        >>> Capabilities(251).grpc_service_pack
        4
        >>> Capabilities(261).grpc_service_pack
        0
        """
        if self.version >= 261:
            return 0
        return _GRPC_SERVICE_PACKS.get(self.version)

    @property
    def plotting(self) -> bool:
        """Whether an embedded app can plot.

        Examples
        --------
        >>> Capabilities(242).plotting
        True
        """
        return self.version >= 242

    @property
    def linux_function_codec(self) -> bool:
        """Whether PyMechanical ships the pythonnet function codec on Linux.

        Examples
        --------
        >>> Capabilities(242).linux_function_codec
        True
        """
        return self.version >= 242

    @property
    def license_manager(self) -> bool:
        """Whether an embedded app provides a license manager.

        Examples
        --------
        >>> Capabilities(252).license_manager
        True
        """
        return self.version >= 252

    @property
    def license_coordinator(self) -> bool:
        """Whether the license manager uses Mechanical's license coordinator.

        Examples
        --------
        >>> Capabilities(271).license_coordinator
        True
        """
        return self.version >= 271

    @property
    def interactive(self) -> bool:
        """Whether an embedded app supports interactive mode and the wait dialog.

        Examples
        --------
        >>> Capabilities(261).interactive
        True
        """
        return self.version >= 261

    @property
    def startup_arguments(self) -> bool:
        """Whether an embedded app accepts read-only, feature flag, and license arguments.

        Examples
        --------
        >>> Capabilities(261).startup_arguments
        True
        """
        return self.version >= 261

    @property
    def cpython_engine(self) -> bool:
        """Whether the ``ansys-mechanical`` CLI can run scripts with the CPython engine.

        Examples
        --------
        >>> Capabilities(261).cpython_engine
        True
        """
        return self.version >= 261

    @property
    def object_scenegraph(self) -> bool:
        """Whether the scenegraph of a single tree object can be retrieved.

        Examples
        --------
        >>> Capabilities(261).object_scenegraph
        True
        """
        return self.version >= 261

    @property
    def clr_host_lite_default(self) -> bool:
        """Whether embedding uses the lite CLR host unless turned off.

        Examples
        --------
        >>> Capabilities(261).clr_host_lite_default
        True
        """
        return self.version > 252
