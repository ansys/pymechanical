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

import numpy as np
import pyvista as pv

from .utils import bgr_to_rgb_tuple


def _transform_to_pyvista(transform):
    np_transform = np.array([transform[i] for i in range(16)]).reshape(4, 4)
    # There's a bug in mechanical, the scenegraph wrappers use theMatrix4D
    # type, which puts the tranformations in the transposed location relative
    # to pyvista. But they use the same matrix layout as pyvista, so that
    # doesn't conform to the expectations of Matrix4D. When it is fixed there,
    # the below line has to be uncommented

    # np_transform = np_transform.transpose()
    return np_transform


def _reshape_3cols(arr: np.array, name: str):
    err = f"{name} must be of the form (x0,y0,z0,x1,y1,z1,...,xn,yn,zn).\
        Given {name} are not divisible by 3!"
    assert arr.size % 3 == 0, err
    numrows = int(arr.size / 3)
    numcols = 3
    arr = np.reshape(arr, (numrows, numcols))
    return arr


def _get_nodes_and_coords(tri_tessellation):
    np_coordinates = _reshape_3cols(
        np.array(tri_tessellation.Coordinates, dtype=np.double), "coordinates"
    )
    np_indices = _reshape_3cols(np.array(tri_tessellation.Indices, dtype=np.int32), "indices")
    np_indices = np.insert(np_indices, 0, 3, axis=1)
    return np_coordinates, np_indices


def plot_model(app):
    """Plot the model."""
    plotter = pv.Plotter()

    for body in app.DataModel.GetObjectsByType(
        Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Body
    ):
        scenegraph_node = Ansys.ACT.Mechanical.Tools.ScenegraphHelpers.GetScenegraph(body)
        np_coordinates, np_indices = _get_nodes_and_coords(scenegraph_node.Child)
        pv_transform = _transform_to_pyvista(scenegraph_node.Transform)
        polydata = pv.PolyData(np_coordinates, np_indices).transform(pv_transform)
        color = pv.Color(bgr_to_rgb_tuple(body.Color))
        plotter.add_mesh(polydata, color=color, smooth_shading=True)

    plotter.show()
