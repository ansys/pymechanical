#!/usr/bin/env python
"""
Version detection test for Future API

This script tests the version detection and assembly loading system.
"""

def test_version_detection():
    """Test version detection without initializing the full app."""
    print("Testing version detection...")
    
    # Check environment variables
    import os
    awp_roots = {key: value for key, value in os.environ.items() if key.startswith("AWP_ROOT")}
    
    if not awp_roots:
        print("❌ No AWP_ROOT environment variables found!")
        print("Set environment variables like AWP_ROOT251=C:\\Program Files\\ANSYS Inc\\v251")
        return False
    
    print("Found Ansys installations:")
    for env_var, path in awp_roots.items():
        version = env_var.replace("AWP_ROOT", "")
        exists = "✓" if os.path.exists(path) else "✗"
        print(f"  {exists} Version {version}: {path}")
    
    return True

def test_future_assemblies():
    """Test if Future assemblies exist for detected versions."""
    print("\nTesting Future assemblies...")
    
    import os
    from pathlib import Path
    
    awp_roots = {key: value for key, value in os.environ.items() if key.startswith("AWP_ROOT")}
    future_base = Path(__file__).parent / "bin" / "x64" / "Release"
    
    found_assemblies = []
    
    for env_var in awp_roots.keys():
        version = env_var.replace("AWP_ROOT", "")
        
        # Check for version-specific assembly
        assembly_path = future_base / version / f"Ansys.Mechanical.Future.{version}.dll"
        
        if assembly_path.exists():
            print(f"  ✓ Version {version}: {assembly_path}")
            found_assemblies.append(version)
        else:
            print(f"  ✗ Version {version}: {assembly_path} (not found)")
    
    if found_assemblies:
        print(f"\nFound {len(found_assemblies)} Future assemblies ready to use")
        return True
    else:
        print("\n❌ No Future assemblies found! Run build_all_versions.py first.")
        return False

def test_with_mechanical():
    """Test the version detection with PyMechanical initialized."""
    print("\nTesting with PyMechanical...")
    
    try:
        from ansys.mechanical.core import App
        print("  Initializing PyMechanical...")
        app = App(globals=globals())
        print("  ✓ PyMechanical initialized")
        
        # Check version detection
        from ansys.mechanical.core.embedding.initializer import INITIALIZED_VERSION
        if INITIALIZED_VERSION:
            print(f"  ✓ Detected version: {INITIALIZED_VERSION}")
            
            # Try to load the version-aware importer
            try:
                from ansys.mechanical.core.embedding.future_importer import (
                    ModelExtensions, ModelHDF5ExportSettings, GeometryType, TransferFileFormat
                )
                print("  ✓ Future extensions loaded successfully")
                print(f"  ✓ Available types: ModelExtensions, ModelHDF5ExportSettings, GeometryType, TransferFileFormat")
                return True
                
            except ImportError as e:
                print(f"  ✗ Future extensions failed to load: {e}")
                return False
        else:
            print("  ✗ Could not detect Mechanical version")
            return False
            
    except Exception as e:
        print(f"  ✗ Failed to initialize PyMechanical: {e}")
        return False

def main():
    """Main test function."""
    print("Future API Version System Test")
    print("=" * 40)
    
    # Test 1: Version detection
    test1_passed = test_version_detection()
    
    # Test 2: Assembly availability  
    test2_passed = test_future_assemblies()
    
    # Test 3: Integration with PyMechanical
    test3_passed = test_with_mechanical()
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print(f"  Version Detection: {'✓' if test1_passed else '✗'}")
    print(f"  Assembly Availability: {'✓' if test2_passed else '✗'}")
    print(f"  PyMechanical Integration: {'✓' if test3_passed else '✗'}")
    
    if all([test1_passed, test2_passed, test3_passed]):
        print("\n🎉 All tests passed! The version system is working correctly.")
        return True
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        if not test2_passed:
            print("\nTo fix assembly issues, run:")
            print("  python build_all_versions.py")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
