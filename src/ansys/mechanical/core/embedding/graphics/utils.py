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

"""Common plotting utilities."""
import os
import typing

import numpy as np


def bgr_to_rgb_tuple(bgr_int: int) -> typing.Tuple[int, int, int]:
    """Convert bgr integer to rgb tuple."""
    r = bgr_int & 255
    g = (bgr_int >> 8) & 255
    b = (bgr_int >> 16) & 255
    return r, g, b


def _reshape_ncols(arr: np.array, ncols: int, name: str = "array"):
    """Reshapes the given array into `ncols` columns.

    Precondition - the array's length must be divisible by `ncols`.
    """
    err = f"{name} must be of the form (x0,y0,z0,x1,y1,z1,...,xn,yn,zn).\
        Given {name} are not divisible by 3!"
    if arr.size % ncols != 0:
        raise ValueError(err)
    numrows = int(arr.size / ncols)
    arr = np.reshape(arr, (numrows, ncols))
    return arr


def get_line_nodes_and_coords(
    line_tessellation: "Ansys.Mechanical.Scenegraph.LineTessellationNode",
):
    """Extract the nodes and coordinates from the LineTessellationNode.

    The TriTessellationNode contains "Coordinates" and "Indices"
    that are flat arrays. This function converts them to numpy arrays
    """
    np_coordinates = _reshape_ncols(
        np.array(line_tessellation.Coordinates, dtype=np.double), 3, "coordinates"
    )

    np_indices = _reshape_ncols(np.array(line_tessellation.Indices, dtype=np.int32), 2, "indices")
    return np_coordinates, np_indices


def get_tri_nodes_and_coords(tri_tessellation: "Ansys.Mechanical.Scenegraph.TriTessellationNode"):
    """Extract the nodes and coordinates from the TriTessellationNode.

    The TriTessellationNode contains "Coordinates" and "Indices"
    that are flat arrays. This function converts them to numpy arrays of the appropriate shape.
    """
    np_coordinates = _reshape_ncols(
        np.array(tri_tessellation.Coordinates, dtype=np.double), 3, "coordinates"
    )
    np_indices = _reshape_ncols(np.array(tri_tessellation.Indices, dtype=np.int32), 3, "indices")
    return np_coordinates, np_indices


def get_tri_result_disp_and_results(
    tri_tessellation: "Ansys.Mechanical.Scenegraph.TriTessellationResultNode",
):
    """Extract the defomation and results from the TriTessellationResultNode.

    The TriTessellationResultNode contains "Displacements" and "Results"
    that are flat arrays. This function converts them to numpy arrays of the appropriate shape.
    """
    np_disp = _reshape_ncols(
        np.array(tri_tessellation.Displacements, dtype=np.double), 3, "deformation"
    )
    np_results = np.array(tri_tessellation.Results, dtype=np.double)
    return np_disp, np_results


def _get_geometry_scene(
    app: "ansys.mechanical.core.embedding.App",
) -> "Ansys.Mechanical.Scenegraph.GroupNode":
    """Get the scene for the geometry.

    using the undocumented apis under ScenegraphHelpers.
    """
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


def get_scene(
    app: "ansys.mechanical.core.embedding.App",
) -> "Ansys.Mechanical.Scenegraph.GroupNode":
    """Get the scene of the model."""
    return _get_geometry_scene(app)


def _get_scene_for_object(
    app: "ansys.mechanical.core.embedding.App", obj
) -> "Ansys.Mechanical.Scenegraph.Node":
    from Ansys.Mechanical.DataModel.Enums import DataModelObjectCategory

    if obj.DataModelObjectCategory == DataModelObjectCategory.Geometry:
        scene = get_scene(app)
        return scene
    if app.version < 261:
        return None
    active_objects = app.Tree.ActiveObjects
    app.Tree.Activate([obj])
    scenegraph_node = app.Graphics.GetScenegraphForActiveObject()
    app.Tree.Activate(active_objects)
    return scenegraph_node


def get_scene_for_object(
    app: "ansys.mechanical.core.embedding.App", obj
) -> "Ansys.Mechanical.Scenegraph.Node":
    """Get the scene for the given object.

    2025R2 and before: only geometry is supported
    later, Mesh and some Results will be supported.
    """
    node = _get_scene_for_object(app, obj)
    if node is not None:
        save_file = os.environ.get("PYMECHANICAL_SAVE_SCENE_FILE", None)
        if save_file is not None:
            import Ansys

            Ansys.Mechanical.Scenegraph.Persistence.SaveToFile(save_file, node)
    return node
