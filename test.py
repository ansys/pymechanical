#!/usr/bin/env python
"""Test the version-aware Future API."""

from ansys.mechanical.core import App
app = App(globals=globals())

print("Testing version-aware Future API...")

# Method 1: Use the version-aware future importer
try:
    from ansys.mechanical.core.embedding.future_importer import (
        ModelExtensions, ModelHDF5ExportSettings, GeometryType, TransferFileFormat
    )
    print("✓ Future extensions loaded via version-aware importer")
    
except ImportError as e:
    print(f"Version-aware importer failed: {e}")
    print("Falling back to manual loading...")
    
    # Method 2: Manual loading (fallback)
    from ansys.mechanical.core.embedding.initializer import INITIALIZED_VERSION
    import clr
    import sys
    from pathlib import Path
    
    version = INITIALIZED_VERSION
    print(f"Detected version: {version}")
    
    # Add version-specific path
    future_dll_path = Path(__file__).parent / "future" / "bin" / "x64" / "Release" / str(version)
    if future_dll_path.exists():
        sys.path.append(str(future_dll_path.resolve()))
        print(f"Added path: {future_dll_path}")
    
    # Load version-specific assembly
    assembly_name = f"Ansys.Mechanical.Future.{version}"
    clr.AddReference(assembly_name)
    print(f"Loaded assembly: {assembly_name}")
    
    from Ansys.Mechanical.Future import ModelExtensions, ModelHDF5ExportSettings
    from Ansys.Mechanical.Future.Enums import GeometryType, TransferFileFormat

# Test the functionality
print("Testing enums...")
print(f"GeometryType.Solid = {GeometryType.Solid}")
print(f"GeometryType.Sheet = {GeometryType.Sheet}")
print(f"TransferFileFormat.HDF5 = {TransferFileFormat.HDF5}")

print("Creating settings...")
settings = ModelHDF5ExportSettings()
settings.GeometryType = GeometryType.Solid
print("✓ Settings created successfully")

print("Testing extension method...")
try:
    ModelExtensions.ExportHDF5TransferFile(app.Model, r"D:\PyAnsys\Repos\exp6\pymechanical\test.hdf5", settings=settings)
    print("✓ ExportHDF5TransferFile completed successfully")
except Exception as e:
    print(f"ExportHDF5TransferFile failed (this may be expected if no geometry is loaded): {e}")

print("Future API test completed!")