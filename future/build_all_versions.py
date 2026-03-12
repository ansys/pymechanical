#!/usr/bin/env python
"""
Build script for Ansys.Mechanical.Future assemblies for all versions

This script builds the Future assembly for versions 24.1, 24.2, 25.1, 25.2, and 26.1
Works on both Windows and Linux.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, 
                              capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def build_version(version, configuration="Release", clean_first=False):
    """Build a specific version of the Future assembly."""
    print(f"\nBuilding version {version}...")
    
    # Check if AWP_ROOT environment variable exists
    env_var = f"AWP_ROOT{version}"
    awp_root = os.environ.get(env_var)
    
    if not awp_root:
        print(f"  Warning: Environment variable {env_var} not found. Skipping version {version}.")
        return False
    
    if not os.path.exists(awp_root):
        print(f"  Warning: Path {awp_root} does not exist. Skipping version {version}.")
        return False
    
    print(f"  Using {env_var} = {awp_root}")
    
    project_file = f"Ansys.Mechanical.Future.{version}.csproj"
    
    if not os.path.exists(project_file):
        print(f"  Error: Project file {project_file} not found!")
        return False
    
    # Clean if requested
    if clean_first:
        print("  Cleaning project...")
        success, output = run_command(f"dotnet clean {project_file} --configuration {configuration}")
        if not success:
            print(f"  Warning: Clean failed: {output}")
    
    # Build the project
    print("  Building project...")
    success, output = run_command(f"dotnet build {project_file} --configuration {configuration} --verbosity minimal --nologo")
    
    if success:
        # Check if output file exists
        output_path = Path(f"bin/x64/{configuration}/{version}/Ansys.Mechanical.Future.{version}.dll")
        if output_path.exists():
            print(f"  ✓ Successfully built: {output_path}")
            return True
        else:
            print(f"  ✗ Build completed but output file not found: {output_path}")
            return False
    else:
        print(f"  ✗ Build failed: {output}")
        return False

def main():
    """Main build function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build Future assemblies for all Ansys Mechanical versions")
    parser.add_argument("--configuration", "-c", default="Release", choices=["Debug", "Release"],
                       help="Build configuration (default: Release)")
    parser.add_argument("--clean", action="store_true", help="Clean before building")
    parser.add_argument("--versions", nargs="*", default=["241", "242", "251", "252", "261"],
                       help="Versions to build (default: all supported versions)")
    
    args = parser.parse_args()
    
    print("Building Ansys.Mechanical.Future assemblies for all versions...")
    print(f"Configuration: {args.configuration}")
    print(f"Clean first: {args.clean}")
    print(f"Versions: {', '.join(args.versions)}")
    
    # Change to the future directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    success_count = 0
    total_count = len(args.versions)
    
    for version in args.versions:
        if build_version(version, args.configuration, args.clean):
            success_count += 1
    
    print(f"\nBuild process completed!")
    print(f"Successfully built: {success_count}/{total_count} versions")
    
    # Show output directory structure
    print(f"\nOutput directory structure:")
    output_base = Path(f"bin/x64/{args.configuration}")
    if output_base.exists():
        for dll_file in output_base.rglob("*.dll"):
            print(f"  {dll_file}")
    else:
        print("  No output files found")
    
    return success_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
