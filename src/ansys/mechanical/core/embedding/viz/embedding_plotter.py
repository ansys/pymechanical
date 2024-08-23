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

"""PyVista plotter."""

import clr

clr.AddReference("Ansys.Mechanical.DataModel")
clr.AddReference("Ansys.ACT.Interfaces")

import Ansys  # isort: skip

from ansys.tools.visualization_interface import Plotter
import numpy as np
import pyvista as pv

from .utils import bgr_to_rgb_tuple, get_nodes_and_coords


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


def to_plotter(app: "ansys.mechanical.core.embedding.App"):
    """Convert the app's geometry to an ``ansys.tools.visualization_interface.Plotter`` instance."""
    plotter = Plotter()

    # TODO - use get_scene from utils instead of looping over bodies directly here.
    for body in app.DataModel.GetObjectsByType(
        Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Body
    ):
        scenegraph_node = Ansys.ACT.Mechanical.Tools.ScenegraphHelpers.GetScenegraph(body)
        np_coordinates, np_indices = _get_nodes_and_coords(scenegraph_node.Child)
        if np_coordinates is None or np_indices is None:
            continue
        pv_transform = _transform_to_pyvista(scenegraph_node.Transform)
        polydata = pv.PolyData(np_coordinates, np_indices).transform(pv_transform)
        color = pv.Color(bgr_to_rgb_tuple(body.Color))
        plotter.plot(polydata, color=color, smooth_shading=True)
    return plotter
