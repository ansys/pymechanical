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

"""Analytics embedding tests"""
import json
import os
import sys

import pytest


@pytest.mark.embedding_scripts
def test_analytics(rootdir, run_subprocess, pytestconfig, tmp_path: pytest.TempPathFactory):
    """Test that no output is written when an info is logged when configured at the error level."""
    version = pytestconfig.getoption("ansys_version")
    # Analytics are only captured for 252+
    if int(version) < 252:
        return

    embedded_py = os.path.join(rootdir, "tests", "scripts", "run_analytics.py")

    analytics_env = os.environ.copy()
    analytics_env["ANS_ENABLE_DATA_ANALYTICS"] = "1"
    analytics_env["ANS_DATA_ANALYTICS_DUMP_FOLDER"] = str(tmp_path)

    args = [sys.executable, embedded_py, "--version", version]
    run_subprocess(args, analytics_env)

    temp_files = os.listdir(tmp_path)
    json_files = [file for file in temp_files if file.endswith(".json")]
    assert len(json_files) == 1
    json_file = os.path.join(tmp_path, json_files[0])
    assert os.path.isfile(json_file)
    with open(json_file, "r", encoding="utf-8") as f:
        analytics_data = json.load(f)

    assert analytics_data["Application.Mode"] == "StandaloneMechanical"
    assert "SessionID" in analytics_data
    assert analytics_data["Model.ModelAttributes.NamedSelections"] == 1.0
    assert analytics_data["ApplicationVersion"].replace(".", "") == version

    # 1.0 -> embedding
    assert analytics_data["Application.SystemInfo.PyMechanicalMode"] == 1.0
