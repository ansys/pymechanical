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
from pxr import Gf, Usd, UsdGeom

clr.AddReference("Ansys.Mechanical.DataModel")
clr.AddReference("Ansys.ACT.Interfaces")

import Ansys  # isort: skip

from .utils import bgr_to_rgb_tuple, get_nodes_and_coords


def _transform_to_rotation_translation(
    transform: "Ansys.ACT.Math.Matrix4D",
) -> typing.Tuple[Gf.Quatf, Gf.Vec3f]:
    """Convert the Transformation matrix to a single-precision quaternion."""
    transforms = [transform[i] for i in range(16)]
    m = Gf.Matrix4d()
    m.SetRow(0, transforms[0:4])
    m.SetRow(1, transforms[4:8])
    m.SetRow(2, transforms[8:12])
    m.SetRow(3, transforms[12:16])

    # Get quaternion from transformation matrix
    quatd: Gf.Quatd = m.ExtractRotationQuat()

    # Get translation from transformation matrix
    transd: Gf.Vec3d = m.ExtractTranslation()

    # Return as single precision
    return Gf.Quatf(quatd), Gf.Vec3f(transd)


def _convert_tri_tessellation_node(
    node: "Ansys.Mechanical.Scenegraph.TriTessellationNode",
    stage: Usd.Stage,
    path: str,
    rgb: typing.Tuple[int, int, int],
) -> Usd.Prim:
    """Convert a mechanical TriTessellationNode node into a Usd Mesh prim."""
    mesh_prim = UsdGeom.Mesh.Define(stage, path)
    np_coordinates, np_indices = get_nodes_and_coords(node)
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
    """Convert a mechanical transform node into a Usd Xform prim."""
    prim = UsdGeom.Xform.Define(stage, path)
    rotation, translation = _transform_to_rotation_translation(node.Transform)
    prim.AddOrientOp().Set(rotation)
    prim.AddTranslateOp().Set(translation)
    child_node = node.Child
    child_path = prim.GetPath().AppendPath("TriTessellation")
    if isinstance(child_node, Ansys.Mechanical.Scenegraph.TriTessellationNode):
        _convert_tri_tessellation_node(child_node, stage, child_path, rgb)
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
