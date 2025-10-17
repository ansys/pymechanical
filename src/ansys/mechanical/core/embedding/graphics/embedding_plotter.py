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

from __future__ import annotations

import dataclasses
from enum import Enum
import os
import typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ansys.mechanical.core.embedding import App
import clr
import numpy as np
import pyvista as pv

from ansys.tools.visualization_interface import Plotter

from .utils import (
    bgr_to_rgb_tuple,
    get_line_nodes_and_coords,
    get_scene_for_object,
    get_tri_nodes_and_coords,
    get_tri_result_disp_and_results,
)

clr.AddReference("Ansys.Mechanical.DataModel")
clr.AddReference("Ansys.ACT.Interfaces")

import Ansys  # noqa: E402


@dataclasses.dataclass
class Plottable:
    """Plottable object."""

    polydata: typing.Optional[pv.PolyData] = None

    # TODO : Make this a list of overridable attributes
    color: typing.Optional[pv.Color] = None
    transform: pv.transform.Transform = None
    children: typing.List["Plottable"] = None
    kwargs: typing.Dict = None

    def __post_init__(self):
        """Initialize the plottable.

        The transform will be identity.
        The children will be an empty list.
        """
        self.transform = np.identity(4)
        self.transform = pv.transform.Transform(np.identity(4))
        self.children = list()


def _transform_to_pyvista(transform: "Ansys.ACT.Math.Matrix4D") -> pv.transform.Transform:
    """Convert the Transformation matrix to a numpy array."""
    np_transform = np.array([transform[i] for i in range(16)]).reshape(4, 4)

    # The mechanical scenegraph transform node is the transpose of the pyvista transform matrix
    np_transform = np_transform.transpose()
    return pv.transform.Transform(np_transform)


def _get_color(node: "Ansys.Mechanical.Scenegraph.AttributeNode") -> pv.Color:
    node_color = node.Property(Ansys.Mechanical.Scenegraph.ScenegraphIntAttributes.Color)
    if node_color is None:
        return None
    color = pv.Color(bgr_to_rgb_tuple(node_color))
    return color


class MeshOrientedTransformResizeStyle(Enum):
    """Dynamic resize style flag for mesh oriented transform nodes."""

    NONE = 0
    SCALING = 1
    STRETCHING = 2


@dataclasses.dataclass
class PlotSettings:
    """Settings for a plot."""

    displacement_scale_factor: float = 1.0
    point_size = 5


class ScenegraphNodeVisitor:
    """Class to visit the Mechanical scenegraph nodes."""

    def __init__(self, app, plot_settings: PlotSettings):
        """Construct a new instance of the visitor class."""
        self._app = app
        self._plot_settings = plot_settings

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

    def _visit_tri_tessellation_result_node(
        self,
        node: "Ansys.Mechanical.Scenegraph.TriTessellationResultNode",
    ) -> Plottable:
        coords, indices = get_tri_nodes_and_coords(node)
        if coords is None or indices is None:
            return None
        indices = np.insert(indices, 0, 3, axis=1)

        disps, results = get_tri_result_disp_and_results(node)
        deformed_coords = coords + disps

        plottable = Plottable(pv.PolyData(deformed_coords, indices))
        plottable.polydata.point_data["Results"] = results
        plottable.kwargs = {"cmap": "viridis", "show_edges": True, "remove_color": 1}
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

    def _visit_mesh_oriented_transform_node(
        self, node: "Ansys.Mechanical.Scenegraph.MeshOrientedTransformNode"
    ) -> Plottable:
        if "PYMECHANICAL_SCENE_VISIT_MESH_ORIENTED_TRANSFORM_NODE" not in os.environ:
            self._app.log_warning("Ignoring MeshOrientedTransformNode")
            return None

        plottable = self.visit_node(node.Child)
        if plottable is None:
            return None

        xform2 = _transform_to_pyvista(
            node.GetComputedTransform(self._plot_settings.displacement_scale_factor)
        )
        plottable.transform = xform2
        return plottable

    def _visit_point_cloud_node(
        self, node: "Ansys.Mechanical.Scenegraph.PointCloudNod"
    ) -> Plottable:
        point_coords = np.array(node.Coordinates, dtype=np.double)
        point_indices = np.array(node.Indices, dtype=np.int32)
        points = np.zeros(shape=(len(point_indices), 3))
        for loop_index, point_index in enumerate(point_indices):
            point = point_coords[point_index * 3 : point_index * 3 + 3]
            points[loop_index] = point
        plottable = Plottable(pv.PolyData(points))
        plottable.kwargs = {"render_points_as_spheres": True}
        return plottable

    def visit_node(self, node: "Ansys.Mechanical.Scenegraph.Node") -> Plottable:
        """Visit an arbitrary node.

        Return a plottable object of that node.
        """
        if not isinstance(node, Ansys.Mechanical.Scenegraph.Node):
            raise Exception("Node is not a scenegraph node!")

        self._app.log_info(f"Visiting {node}")

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
        elif isinstance(node, Ansys.Mechanical.Scenegraph.TriTessellationResultNode):
            return self._visit_tri_tessellation_result_node(node)
        elif isinstance(node, Ansys.Mechanical.Scenegraph.MeshOrientedTransformNode):
            return self._visit_mesh_oriented_transform_node(node)
        elif isinstance(node, Ansys.Mechanical.Scenegraph.PointCloudNode):
            return self._visit_point_cloud_node(node)
        else:
            self._app.log_warning(f"Unexpected node: {node}")
        return None


def _add_plottable(plotter: Plotter, plottable: Plottable, plot_settings: PlotSettings):
    for child in plottable.children:
        child.transform *= plottable.transform
        if child.color is None:
            child.color = plottable.color
        _add_plottable(plotter, child, plot_settings)

    if plottable.polydata is None:
        return

    polydata = plottable.polydata.transform(plottable.transform, inplace=True)
    kwargs = {
        "color": plottable.color,
        "smooth_shading": True,
        "point_size": plot_settings.point_size,
    }
    if plottable.kwargs is not None:
        kwargs.update(plottable.kwargs)
    if kwargs.get("remove_color", None):
        kwargs.pop("remove_color")
        if "color" in kwargs:
            kwargs.pop("color")
    plotter.plot(polydata, **kwargs)


def _get_plotter_for_scene(
    app: App,
    node: "Ansys.Mechanical.Scenegraph.Node",
    plot_settings: PlotSettings,
) -> Plotter:
    visitor = ScenegraphNodeVisitor(app, plot_settings)
    plottable = visitor.visit_node(node)
    plotter = Plotter()
    _add_plottable(plotter, plottable, plot_settings)
    return plotter


def _plot_object(app: App, obj, plot_settings: PlotSettings) -> Plotter:
    """Get a ``ansys.tools.visualization_interface.Plotter`` instance for `obj`."""
    scene = get_scene_for_object(app, obj)
    if scene is None:
        app.log_warning(f"No scene available for object {obj}!")
        return None
    plotter = _get_plotter_for_scene(app, scene, plot_settings)
    return plotter


def to_plotter(app: App, obj=None, plot_settings: PlotSettings = None) -> Plotter:
    """Convert the scene for `obj` to an ``ansys.tools.visualization_interface.Plotter`` instance.

    If the `obj` is None, default to the Geometry object.
    Geometry, Mesh, and some Results are currently supported.
    """
    if obj is None:
        obj = app.Model.Geometry
    if plot_settings is None:
        plot_settings = PlotSettings()
    return _plot_object(app, obj, plot_settings)
