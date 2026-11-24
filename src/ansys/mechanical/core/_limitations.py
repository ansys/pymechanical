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

"""Answer which known defects of each Mechanical version need a workaround, in one place."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Limitations:
    """Provides the known defects of a Mechanical version that PyMechanical works around.

    Each property is ``True`` when the version has the defect, so the caller
    applies the matching workaround.

    Examples
    --------
    >>> Limitations(241).material_server_race
    True
    >>> Limitations(261).material_server_race
    False
    """

    version: int

    @property
    def material_server_race(self) -> bool:
        """Whether the material server races on shutdown unless it runs serially.

        In 2024 R1, the REST server behind the material model GUI starts on a
        background thread, even in batch mode.

        Examples
        --------
        >>> Limitations(241).material_server_race
        True
        """
        return self.version == 241

    @property
    def unoptimized_startup(self) -> bool:
        """Whether embedding on Windows must use the unoptimized startup.

        Examples
        --------
        >>> Limitations(242).unoptimized_startup
        True
        """
        return self.version < 251

    @property
    def clr_host_lite_opt_in(self) -> bool:
        """Whether the lite CLR host is off unless embedding turns it on.

        Examples
        --------
        >>> Limitations(251).clr_host_lite_opt_in
        True
        """
        return self.version in (251, 252)

    @property
    def libx11_shutdown_crash(self) -> bool:
        """Whether a preloaded ``libX11.so`` crashes Python on shutdown on Linux.

        Examples
        --------
        >>> Limitations(251).libx11_shutdown_crash
        True
        """
        return self.version >= 251
