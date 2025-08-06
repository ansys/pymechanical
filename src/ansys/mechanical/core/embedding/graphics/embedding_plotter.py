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

import dataclasses
import typing

import clr

clr.AddReference("Ansys.Mechanical.DataModel")
clr.AddReference("Ansys.ACT.Interfaces")

import Ansys  # isort: skip

from ansys.tools.visualization_interface import Plotter
import numpy as np
import pyvista as pv

from .utils import bgr_to_rgb_tuple, get_tri_nodes_and_coords, get_line_nodes_and_coords, get_scene_for_object


@dataclasses.dataclass
class Plottable:
    """Plottable object."""

    polydata: typing.Optional[pv.PolyData] = None

    # TODO - make this a list of overridable attributes
    color: typing.Optional[pv.Color] = None
    transform: np.ndarray = None
    children: typing.List["Plottable"] = None

    def __post_init__(self):
        """Initialize the plottable.

        The transform will be identity.
        The children will be an empty list.
        """
        self.transform = np.identity(4)
        # pv.transform.Transform(np.identity(4))
        self.children = list()


def _transform_to_pyvista(transform: "Ansys.ACT.Math.Matrix4D"):
    """Convert the Transformation matrix to a numpy array."""
    np_transform = np.array([transform[i] for i in range(16)]).reshape(4, 4)

    # The mechanical scenegraph transform node is the transpose of the pyvista transform matrix
    np_transform = np_transform.transpose()
    return np_transform


def _get_color(node: "Ansys.Mechanical.Scenegraph.AttributeNode") -> pv.Color:
    node_color = node.Property(Ansys.Mechanical.Scenegraph.ScenegraphIntAttributes.Color)
    if node_color is None:
        return None
    color = pv.Color(bgr_to_rgb_tuple(node_color))
    return color


class ScenegraphNodeVisitor:
    def __init__(self, app):
        self._app = app

    def _visit_group_node(self, node: "Ansys.Mechanical.Scenegraph.GroupNode") -> Plottable:
        """Return a new plottable grouping all the children of the group node."""
        plottable = Plottable()
        for child in node.Children:
            child_plottable = self.visit_node(child)
            if child_plottable is not None:
                plottable.children.append(child_plottable)
        return plottable

    def _visit_line_tessellation_node(
        self,
        node: "Ansys.Mechanical.Scenegraph.LineTessellationNode",
    ) -> Plottable:
        np_coordinates, np_indices = get_line_nodes_and_coords(node)
        np_indices = np.insert(np_indices, 0, 2, axis=1)
        line_mesh = pv.PolyData()
        line_mesh.points = np_coordinates
        line_mesh.lines = np_indices
        plottable = Plottable(line_mesh)
        return plottable


    def _visit_tri_tessellation_node(
        self,
        node: "Ansys.Mechanical.Scenegraph.TriTessellationNode",
    ) -> Plottable:
        np_coordinates, np_indices = get_tri_nodes_and_coords(node)
        if np_coordinates is None or np_indices is None:
            return None
        np_indices = np.insert(np_indices, 0, 3, axis=1)
        plottable = Plottable(pv.PolyData(np_coordinates, np_indices))
        return plottable

    def _visit_transform_node(self, node: "Ansys.Mechanical.Scenegraph.TransformNode") -> Plottable:
        plottable = self.visit_node(node.Child)
        if plottable is None:
            return None
        plottable.transform = _transform_to_pyvista(node.Transform)
        return plottable

    def _visit_attribute_node(self, node: "Ansys.Mechanical.Scenegraph.AttributeNode") -> Plottable:
        """Return the plottable of the child node with the color attached."""
        plottable = self.visit_node(node.Child)
        if plottable is None:
            return None
        plottable.color = _get_color(node)
        return plottable

    def visit_node(self, node: "Ansys.Mechanical.Scenegraph.Node") -> Plottable:
        if not isinstance(node, Ansys.Mechanical.Scenegraph.Node):
            raise Exception("Node is not a scenegraph node!")

        if isinstance(node, Ansys.Mechanical.Scenegraph.GroupNode):
            return self._visit_group_node(node)
        elif isinstance(node, Ansys.Mechanical.Scenegraph.AttributeNode):
            return self._visit_attribute_node(node)
        elif isinstance(node, Ansys.Mechanical.Scenegraph.TransformNode):
            return self._visit_transform_node(node)
        elif isinstance(node, Ansys.Mechanical.Scenegraph.TriTessellationNode):
            return self._visit_tri_tessellation_node(node)
        elif isinstance(node, Ansys.Mechanical.Scenegraph.LineTessellationNode):
            return self._visit_line_tessellation_node(node)
        else:
            self._app.log_warning(f"Unexpected node: {node}")
        return None


def _add_plottable(plotter: Plotter, plottable: Plottable):
    for child in plottable.children:
        child.transform *= plottable.transform
        if child.color is None:
            child.color = plottable.color
        _add_plottable(plotter, child)

    if plottable.polydata is None:
        return

    polydata = plottable.polydata.transform(plottable.transform, inplace=True)
    plotter.plot(polydata, color=plottable.color, smooth_shading=True)


def _get_plotter_for_scene(app: "ansys.mechanical.core.embedding.App", node: "Ansys.Mechanical.Scenegraph.Node") -> Plotter:
    visitor = ScenegraphNodeVisitor(app)
    plottable = visitor.visit_node(node)
    plotter = Plotter()
    _add_plottable(plotter, plottable)
    return plotter


def _plot_object(app: "ansys.mechanical.core.embedding.App", obj) -> Plotter:
    """Get a ``ansys.tools.visualization_interface.Plotter`` instance for `obj`."""
    scene = get_scene_for_object(app, obj)
    if scene is None:
        app.log_warning(f"No scene available for object {obj}!")
        return None
    plotter = _get_plotter_for_scene(app, scene)
    return plotter


def to_plotter(app: "ansys.mechanical.core.embedding.App", obj=None) -> Plotter:
    """Convert the scene for `obj` to an ``ansys.tools.visualization_interface.Plotter`` instance.

    If the `obj` is None, default to the Geometry object.
    Geometry, Mesh, and some Results are currently supported.
    """
    if obj is None:
        obj = app.Model.Geometry
    return _plot_object(app, obj)
