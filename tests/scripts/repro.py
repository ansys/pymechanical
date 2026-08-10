# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Sample reproducer script for matrix testing."""

import sys
import ansys.mechanical.core as pymechanical

print("==================================================")
print(f"Running reproducer test with Python {sys.version}")
print(f"PyMechanical version: {pymechanical.__version__}")
print("==================================================")

# Simple assertion or workflow validation
print("Reproducer execution successful.")
