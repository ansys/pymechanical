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
"""Import Mechanical globals."""

from ansys.mechanical.core.embedding.app import is_initialized

if not is_initialized():
    raise Exception("Globals cannot be imported until the embedded app is initialized.")

import clr

clr.AddReference("Ansys.Mechanical.DataModel")
clr.AddReference("Ansys.ACT.Interfaces")


clr.AddReference("System.Collections")
clr.AddReference("Ansys.ACT.WB1")
clr.AddReference("Ansys.Mechanical.DataModel")

# from Ansys.ACT.Mechanical import Transaction
# When ansys-pythonnet issue #14 is fixed, uncomment above
from Ansys.ACT.Core.Math import Point2D, Point3D  # noqa isort: skip
from Ansys.ACT.Math import Vector3D  # noqa isort: skip
from Ansys.Core.Units import Quantity  # noqa isort: skip
from Ansys.Mechanical.DataModel import MechanicalEnums  # noqa isort: skip
from Ansys.Mechanical.Graphics import Point, SectionPlane  # noqa isort: skip

from ansys.mechanical.core.embedding.transaction import Transaction  # noqa isort: skip

import System  # noqa isort: skip
import Ansys  # noqa isort: skip
