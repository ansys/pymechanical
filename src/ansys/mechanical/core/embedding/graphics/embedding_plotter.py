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

"""PyVista plotter."""

import clr

clr.AddReference("Ansys.Mechanical.DataModel")
clr.AddReference("Ansys.ACT.Interfaces")

import Ansys  # isort: skip

from ansys.tools.visualization_interface import Plotter
import numpy as np
import pyvista as pv

from .utils import bgr_to_rgb_tuple, get_nodes_and_coords, get_scene


def _transform_to_pyvista(transform: "Ansys.ACT.Math.Matrix4D"):
    """Convert the Transformation matrix to a numpy array."""
    np_transform = np.array([transform[i] for i in range(16)]).reshape(4, 4)

    # The mechanical scenegraph transform node is the transpose of the pyvista transform matrix
    np_transform = np_transform.transpose()
    return np_transform


def _get_tri_nodes_and_coords(tri_tessellation: "Ansys.Mechanical.Scenegraph.TriTessellationNode"):
    """Get the nodes and indices of the TriTessellationNode.

    pyvista format expects a number of vertices per facet which is always 3
    from this kind of node.
    """
    np_coordinates, np_indices = get_nodes_and_coords(tri_tessellation)
    np_indices = np.insert(np_indices, 0, 3, axis=1)
    return np_coordinates, np_indices


def _get_nodes_and_coords(node: "Ansys.Mechanical.Scenegraph.Node"):
    """Get the nodes and indices of the Scenegraph node.

    Currently only supported for tri tessellation nodes
    """
    if isinstance(node, Ansys.Mechanical.Scenegraph.TriTessellationNode):
        return _get_tri_nodes_and_coords(node)

    # TODO - support line tessellation node. See issue #809
    # if isinstance(node, Ansys.Mechanical.Scenegraph.LineTessellationNode):
    return None, None


def _tri_tessellation_to_mesh(
    node: "Ansys.Mechanical.Scenegraph.TriTessellationNode",
) -> pv.PolyData:
    np_coordinates, np_indices = _get_nodes_and_coords(node)
    if np_coordinates is None or np_indices is None:
        return None
    polydata = pv.PolyData(np_coordinates, np_indices)
    return polydata


def _get_mesh(node: "Ansys.Mechanical.Scenegraph.Node") -> pv.PolyData:
    import Ansys

    if isinstance(node, Ansys.Mechanical.Scenegraph.TriTessellationNode):
        polydata = _tri_tessellation_to_mesh(node)
        return polydata
    else:
        print(f"Cannot get mesh from {type(node)}")
    return None


def _handle_transform_node(node: "Ansys.Mechanical.Scenegraph.TransformNode") -> pv.PolyData:
    polydata = _get_mesh(node.Child)
    if polydata is None:
        return None
    pv_transform = _transform_to_pyvista(node.Transform)
    polydata = polydata.transform(pv_transform, inplace=True)
    return polydata


def _get_polydata(node: "Ansys.Mechanical.Scenegraph.Node") -> pv.PolyData:
    import Ansys

    if isinstance(node, Ansys.Mechanical.Scenegraph.TransformNode):
        polydata = _handle_transform_node(node)
        return polydata
    else:
        print(f"unexpected attribute node: {node}")
        return None


def _visit_attribute_node(plotter: Plotter, node: "Ansys.Mechanical.Scenegraph.AttributeNode"):
    scenegraph_node = node.Child
    node_color = node.Property(Ansys.Mechanical.Scenegraph.ScenegraphIntAttributes.Color)
    polydata = _get_polydata(scenegraph_node)
    if polydata is None:
        return
    color = pv.Color(bgr_to_rgb_tuple(node_color))
    plotter.plot(polydata, color=color, smooth_shading=True)


def _visit_group_node(plotter: Plotter, node: "Ansys.Mechanical.Scenegraph.GroupNode"):
    for child in node.Children:
        _visit_node(plotter, child)


def _visit_node(plotter: Plotter, node: "Ansys.Mechanical.Scenegraph.Node"):
    import Ansys  # the reference to the scenegraph assembly has already been added in `get_scene`

    if not isinstance(node, Ansys.Mechanical.Scenegraph.Node):
        raise Exception("Node is not a scenegraph node!")

    if isinstance(node, Ansys.Mechanical.Scenegraph.GroupNode):
        _visit_group_node(plotter, node)
    if isinstance(node, Ansys.Mechanical.Scenegraph.AttributeNode):
        _visit_attribute_node(plotter, node)


def _get_scene_for_object(app, obj):
    import Ansys

    if (
        obj.DataModelObjectCategory
        == Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Geometry
    ):
        scene = get_scene(app)
        return scene
    active_objects = app.Tree.ActiveObjects
    app.Tree.Activate([obj])
    scenegraph_node = app.Graphics.GetScenegraphForActiveObject()
    app.Tree.Activate(active_objects)
    return scenegraph_node


def _plot_object(app, obj) -> Plotter:
    """Convert the scenegraph for obj to an ``ansys.tools.visualization_interface.Plotter`` instance."""
    scene = _get_scene_for_object(app, obj)
    if scene is None:
        print(f"No scene available for object {obj}")
        return None
    plotter = Plotter()
    _visit_node(plotter, scene)
    return plotter


def to_plotter(app: "ansys.mechanical.core.embedding.App", obj=None) -> Plotter:
    """Convert the scene for `obj` to an ``ansys.tools.visualization_interface.Plotter`` instance.

    If the `obj` is None, default to the Geometry object."""
    if obj is None:
        obj = app.Model.Geometry
    return _plot_object(app, obj)
