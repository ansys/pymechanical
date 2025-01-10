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
"""functions that can be installed in Server."""


# free functions: first argument of each must be app
def run_python_script(
    app: "ansys.mechanical.core.embedding.App",
    script: str,
    enable_logging=False,
    log_level="WARNING",
    progress_interval=2000,
):
    """Run scripts using Internal python engine."""
    try:
        app.execute_script(script)
    except Exception as e:
        raise Exception({str(e)})
    return app.execute_script(script)


def run_python_script_from_file(
    app: "ansys.mechanical.core.embedding.App",
    file_path: str,
    enable_logging=False,
    log_level="WARNING",
    progress_interval=2000,
):
    """Run scripts using Internal python engine."""
    return app.execute_script_from_file(file_path)


def clear(app: "ansys.mechanical.core.embedding.App"):
    app.new()


# def project_directory(app: "ansys.mechanical.core.embedding.App"):
#     return app.execute_script("ExtAPI.DataModel.Project.ProjectDirectory")
