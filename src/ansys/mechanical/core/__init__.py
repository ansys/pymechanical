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

"""Initialize the package level imports."""
import logging
import os

from ansys.tools.path import find_mechanical
import appdirs

# Setup data directory
USER_DATA_PATH = appdirs.user_data_dir(appname="ansys_mechanical_core", appauthor="Ansys")
if not os.path.exists(USER_DATA_PATH):
    os.makedirs(USER_DATA_PATH)

EXAMPLES_PATH = os.path.join(USER_DATA_PATH, "examples")
if not os.path.exists(EXAMPLES_PATH):
    os.makedirs(EXAMPLES_PATH)

from ansys.mechanical.core.logging import Logger

# Create logger for package level use
LOG = Logger(level=logging.ERROR, to_file=False, to_stdout=True)
LOG.debug("Loaded logging module as LOG")

from ansys.mechanical.core._version import __version__
from ansys.mechanical.core.mechanical import (
    change_default_mechanical_path,
    close_all_local_instances,
    get_mechanical_path,
    launch_mechanical,
)

# import few classes / functions
from ansys.mechanical.core.mechanical import Mechanical as Mechanical

try:
    from ansys.mechanical.core.embedding import App, global_variables

    HAS_EMBEDDING = True
except:
    HAS_EMBEDDING = False

# manage the package level ports
LOCAL_PORTS = []

from ansys.mechanical.core.pool import LocalMechanicalPool

BUILDING_GALLERY = False
