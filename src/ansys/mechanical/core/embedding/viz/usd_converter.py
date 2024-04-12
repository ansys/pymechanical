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

"""Converter to OpenUSD."""

import typing

import clr
import numpy as np
from pxr import Gf, Usd, UsdGeom

clr.AddReference("Ansys.Mechanical.DataModel")
clr.AddReference("Ansys.ACT.Interfaces")

import Ansys  # isort: skip

from .utils import bgr_to_rgb_tuple


def _transform_to_rotation_quat(transform) -> Gf.Quatf:
    transforms = [transform[i] for i in range(16)]
    m = Gf.Matrix4d()
    m.SetRow(0, transforms[0:4])
    m.SetRow(1, transforms[4:8])
    m.SetRow(2, transforms[8:12])
    m.SetRow(3, transforms[12:16])

    # TODO: m = m.GetTranspose() # if/when needed?

    # Get quaternion from transformation matrix
    quatd: Gf.Quatd = m.ExtractRotationQuat()

    # Convert to single precision
    quatf = Gf.Quatf(quatd)
    return quatf


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
    return np_coordinates, np_indices


def _convert_tri_tessellation_node(
    node: "Ansys.Mechanical.Scenegraph.TriTessellationNode",
    stage: Usd.Stage,
    path: str,
    rgb: typing.Tuple[int, int, int],
) -> Usd.Prim:
    mesh_prim = UsdGeom.Mesh.Define(stage, path)
    np_coordinates, np_indices = _get_nodes_and_coords(node)
    mesh_prim.CreatePointsAttr(np_coordinates)
    mesh_prim.CreateFaceVertexCountsAttr([3] * len(np_indices))
    mesh_prim.CreateFaceVertexIndicesAttr(np_indices)
    r, g, b = rgb
    mesh_prim.GetDisplayColorAttr().Set([(r / 255, g / 255, b / 255)])
    return mesh_prim


def _convert_transform_node(
    node: "Ansys.Mechanical.Scenegraph.TransformNode",
    stage: Usd.Stage,
    path: str,
    rgb: typing.Tuple[int, int, int],
) -> Usd.Prim:
    prim = UsdGeom.Xform.Define(stage, path)
    prim.AddOrientOp().Set(_transform_to_rotation_quat(node.Transform))
    child_node = node.Child
    if isinstance(child_node, Ansys.Mechanical.Scenegraph.TriTessellationNode):
        _convert_tri_tessellation_node(
            node.Child, stage, prim.GetPath().AppendPath("TriTessellation"), rgb
        )
    return prim


def to_usd_stage(app: "ansys.mechanical.core.embedding.App", name: str) -> None:
    """Convert mechanical scene to usd stage."""
    stage = Usd.Stage.CreateNew(name)

    root_prim = UsdGeom.Xform.Define(stage, "/root")

    category = Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory.Body
    bodies = app.DataModel.GetObjectsByType(category)
    for body in bodies:
        scenegraph_node = Ansys.ACT.Mechanical.Tools.ScenegraphHelpers.GetScenegraph(body)
        body_path = root_prim.GetPath().AppendPath(f"body{body.ObjectId}")
        _convert_transform_node(scenegraph_node, stage, body_path, bgr_to_rgb_tuple(body.Color))

    return stage


def to_usd_file(app, path: str) -> None:
    """Export mechanical scene to usd file."""
    stage = to_usd_stage(app, path)
    stage.GetRootLayer().Save()
