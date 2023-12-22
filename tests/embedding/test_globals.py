# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
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

"""Embedding tests for global variables associated with Mechanical"""
import pytest

import ansys.mechanical.core as pymechanical
from ansys.mechanical.core import global_variables


@pytest.mark.embedding
def test_global_variables(embedded_app):
    """Test the global variables"""
    globals_dict = global_variables(embedded_app, True)
    assert "ExtAPI" in globals_dict
    assert "DataModel" in globals_dict
    assert "Model" in globals_dict
    assert "Tree" in globals_dict
    assert "Quantity" in globals_dict
    assert "System" in globals_dict
    assert "Ansys" in globals_dict
    assert "Transaction" in globals_dict


@pytest.mark.embedding
def test_transaction(embedded_app):
    """Test Transaction"""
    globals().update(pymechanical.global_variables(embedded_app, True))

    with Transaction() as transaction:
        assert isinstance(transaction, Transaction)
        assert transaction._disposed is False, "Transaction remains in scope"

    assert transaction._disposed is True, "Transaction instance has been disposed"
