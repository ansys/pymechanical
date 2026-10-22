# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Tests for geometry scenegraphs."""

import numpy as np
import pytest

from ansys.mechanical.core.embedding.graphics.utils import (
    get_scene,
    get_scene_for_object,
    get_tri_nodes_and_coords,
)


def _walk_scene_nodes(node):
    """Yield scene nodes through groups and single-child wrappers."""
    import Ansys

    yield node
    if isinstance(node, Ansys.Mechanical.Scenegraph.GroupNode):
        for child in node.Children:
            yield from _walk_scene_nodes(child)
    elif isinstance(
        node,
        (Ansys.Mechanical.Scenegraph.AttributeNode, Ansys.Mechanical.Scenegraph.TransformNode),
    ):
        yield from _walk_scene_nodes(node.Child)


@pytest.mark.embedding
@pytest.mark.minimum_version(242)
def test_scenegraph_empty_geometry(embedded_app):
    """Test that an empty model produces an empty scene."""
    scene = get_scene(embedded_app)

    assert list(scene.Children) == []


@pytest.mark.embedding
@pytest.mark.minimum_version(242)
def test_scenegraph_geometry_contains_bodies(embedded_app, assets):
    """Test that the scene contains one tagged node per geometry body."""
    from ansys.mechanical.core.embedding.enum_importer import DataModelObjectCategory

    embedded_app.helpers.import_geometry(str(assets / "Eng157.x_t"))
    bodies = list(embedded_app.DataModel.GetObjectsByType(DataModelObjectCategory.Body))
    scene = get_scene(embedded_app)
    nodes = list(scene.Children)

    assert bodies
    assert len(nodes) == len(bodies)
    assert {node.Tag for node in nodes} == {f"body{body.ObjectId}" for body in bodies}
    assert all(node.Child is not None for node in nodes)


@pytest.mark.embedding
@pytest.mark.minimum_version(242)
def test_scenegraph_geometry_preserves_body_colors(embedded_app, assets):
    """Test that geometry object scenes retain each body's color."""
    from ansys.mechanical.core.embedding.enum_importer import DataModelObjectCategory

    embedded_app.helpers.import_geometry(str(assets / "Eng157.x_t"))
    bodies = list(embedded_app.DataModel.GetObjectsByType(DataModelObjectCategory.Body))
    assert bodies
    bodies[0].Color = 0x123456
    scene = get_scene_for_object(embedded_app, embedded_app.Model.Geometry)

    import Ansys

    color_attribute = Ansys.Mechanical.Scenegraph.ScenegraphIntAttributes.Color
    assert {node.Tag: node.Property(color_attribute) for node in scene.Children} == {
        f"body{body.ObjectId}": body.Color for body in bodies
    }


@pytest.mark.embedding
@pytest.mark.minimum_version(242)
def test_scenegraph_geometry_tessellation_readable(embedded_app, assets):
    """Test that tessellations contain finite coordinates and valid connectivity."""
    embedded_app.helpers.import_geometry(str(assets / "Eng157.x_t"))
    scene = get_scene_for_object(embedded_app, embedded_app.Model.Geometry)

    import Ansys

    nodes = [
        node
        for node in _walk_scene_nodes(scene)
        if isinstance(node, Ansys.Mechanical.Scenegraph.TriTessellationNode)
    ]

    assert nodes
    for node in nodes:
        coordinates, indices = get_tri_nodes_and_coords(node)
        assert coordinates.shape[0] > 0
        assert coordinates.shape[1] == 3
        assert np.isfinite(coordinates).all()
        assert indices.shape[0] > 0
        assert indices.shape[1] == 3
        assert (indices >= 0).all()
        assert (indices < len(coordinates)).all()
