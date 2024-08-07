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

"""Common plotting utilities."""
import typing

import numpy as np


def bgr_to_rgb_tuple(bgr_int: int) -> typing.Tuple[int, int, int]:
    """Convert bgr integer to rgb tuple."""
    r = bgr_int & 255
    g = (bgr_int >> 8) & 255
    b = (bgr_int >> 16) & 255
    return r, g, b


def _reshape_3cols(arr: np.array, name: str = "array"):
    """Reshapes the given array into 3 columns.

    Precondition - the array's length must be divisible by 3.
    """
    err = f"{name} must be of the form (x0,y0,z0,x1,y1,z1,...,xn,yn,zn).\
        Given {name} are not divisible by 3!"
    assert arr.size % 3 == 0, err
    numrows = int(arr.size / 3)
    numcols = 3
    arr = np.reshape(arr, (numrows, numcols))
    return arr


def get_nodes_and_coords(tri_tessellation: "Ansys.Mechanical.Scenegraph.TriTessellationNode"):
    """Extract the nodes and coordinates from the TriTessellationNode.

    The TriTessellationNode contains "Coordinates" and "Indices"
    that are flat arrays. This function converts them to numpy arrays
    """
    np_coordinates = _reshape_3cols(
        np.array(tri_tessellation.Coordinates, dtype=np.double), "coordinates"
    )
    np_indices = _reshape_3cols(np.array(tri_tessellation.Indices, dtype=np.int32), "indices")
    return np_coordinates, np_indices


def get_scene(
    app: "ansys.mechanical.core.embedding.App",
) -> "Ansys.Mechanical.Scenegraph.GroupNode":
    """Get the scene of the model."""
    import clr

    clr.AddReference("Ansys.Mechanical.DataModel")
    clr.AddReference("Ansys.Mechanical.Scenegraph")
    clr.AddReference("Ansys.ACT.Interfaces")

    import Ansys  # isort: skip

    category = Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Body
    group_node = Ansys.Mechanical.Scenegraph.Builders.GroupNodeBuilder()
    for body in app.DataModel.GetObjectsByType(category):
        scenegraph_node = Ansys.ACT.Mechanical.Tools.ScenegraphHelpers.GetScenegraph(body)
        # wrap the body node in an attribute node using the body color
        attribute_node_builder = Ansys.Mechanical.Scenegraph.Builders.AttributeNodeBuilder()
        attribute_node = (
            attribute_node_builder.Tag(f"body{body.ObjectId}")
            .Child(scenegraph_node)
            # set the color, body.Color is a BGR uint bitfield
            .Property(Ansys.Mechanical.Scenegraph.ScenegraphIntAttributes.Color, body.Color)
            .Build()
        )
        group_node.AddChild(attribute_node)
    return group_node.Build()
