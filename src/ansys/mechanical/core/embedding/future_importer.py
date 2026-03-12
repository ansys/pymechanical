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
"""Version-aware Future Mechanical extensions importer."""

import os
import sys
from pathlib import Path

from ansys.mechanical.core.embedding.app import is_initialized

if not is_initialized():
    raise Exception("Future extensions cannot be imported until the embedded app is initialized.")

def _get_mechanical_version():
    """Get the current Mechanical version from the initialized app."""
    try:
        from ansys.mechanical.core.embedding.initializer import INITIALIZED_VERSION
        if INITIALIZED_VERSION is not None:
            return INITIALIZED_VERSION
    except ImportError:
        pass
    
    # Fallback: try to detect version from environment variables
    awp_roots = [key for key in os.environ.keys() if key.startswith("AWP_ROOT")]
    if awp_roots:
        # Use the first one found
        version_str = awp_roots[0].replace("AWP_ROOT", "")
        try:
            return int(version_str)
        except ValueError:
            pass
    
    raise RuntimeError("Could not determine Mechanical version. Make sure PyMechanical is properly initialized.")

def _add_version_specific_path(version):
    """Add the version-specific Future assembly path to sys.path."""
    platform_string = "winx64" if os.name == "nt" else "linx64"
    
    # Path to the version-specific DLL
    future_dll_path = (
        Path(__file__).parent.parent.parent.parent.parent / 
        "future" / "bin" / "x64" / "Release" / str(version)
    )
    
    if future_dll_path.exists() and str(future_dll_path) not in sys.path:
        sys.path.append(str(future_dll_path.resolve()))
        return str(future_dll_path.resolve())
    
    return None

def _load_future_assembly(version):
    """Load the version-specific Future assembly."""
    import clr
    
    assembly_name = f"Ansys.Mechanical.Future.{version}"
    
    try:
        clr.AddReference(assembly_name)
        return assembly_name
    except Exception as e:
        raise ImportError(f"Failed to load {assembly_name} assembly: {e}")

# Get the current Mechanical version
try:
    mechanical_version = _get_mechanical_version()
    print(f"Detected Mechanical version: {mechanical_version}")
    
    # Add the version-specific path
    added_path = _add_version_specific_path(mechanical_version)
    if added_path:
        print(f"Added Future assembly path: {added_path}")
    else:
        print("Warning: Future assembly path not found or already in sys.path")
    
    # Load the version-specific assembly
    loaded_assembly = _load_future_assembly(mechanical_version)
    print(f"Loaded assembly: {loaded_assembly}")
    
    # Import the Future namespace and classes
    from Ansys.Mechanical.Future import ModelExtensions, ModelHDF5ExportSettings  # noqa isort: skip
    from Ansys.Mechanical.Future.Enums import GeometryType, TransferFileFormat  # noqa isort: skip
    
    # Make the extensions available at module level
    __all__ = ["ModelExtensions", "ModelHDF5ExportSettings", "GeometryType", "TransferFileFormat"]
    
    print("✓ Future extensions imported successfully")
    
except Exception as e:
    raise ImportError(f"Failed to initialize Future extensions: {e}")
