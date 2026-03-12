#!/bin/bash
# Build script for Ansys.Mechanical.Future assemblies for all versions (Linux)
# This script builds the Future assembly for versions 24.1, 24.2, 25.1, 25.2, and 26.1

set -e

CONFIGURATION="${1:-Release}"
CLEAN_FIRST="${2:-false}"

echo "Building Ansys.Mechanical.Future assemblies for all versions..."

versions=("241" "242" "251" "252" "261")
current_dir=$(pwd)

for version in "${versions[@]}"; do
    echo ""
    echo "Building version $version..."
    
    env_var="AWP_ROOT$version"
    awp_root="${!env_var}"
    
    if [ -z "$awp_root" ]; then
        echo "Warning: Environment variable $env_var not found. Skipping version $version."
        continue
    fi
    
    if [ ! -d "$awp_root" ]; then
        echo "Warning: Path $awp_root does not exist. Skipping version $version."
        continue
    fi
    
    echo "  Using $env_var = $awp_root"
    
    project_file="Ansys.Mechanical.Future.$version.csproj"
    
    if [ ! -f "$project_file" ]; then
        echo "Error: Project file $project_file not found!"
        continue
    fi
    
    if [ "$CLEAN_FIRST" = "true" ]; then
        echo "  Cleaning project..."
        dotnet clean "$project_file" --configuration "$CONFIGURATION" --verbosity quiet || true
    fi
    
    echo "  Building project..."
    if dotnet build "$project_file" --configuration "$CONFIGURATION" --verbosity minimal --nologo; then
        output_path="bin/x64/$CONFIGURATION/$version/Ansys.Mechanical.Future.$version.dll"
        if [ -f "$output_path" ]; then
            echo "  ✓ Successfully built: $output_path"
        else
            echo "  ✗ Build failed - output file not found: $output_path"
        fi
    else
        echo "  ✗ Build failed for version $version"
    fi
done

echo ""
echo "Build process completed!"
echo ""
echo "Output directory structure:"
find "bin/x64/$CONFIGURATION" -name "*.dll" 2>/dev/null | while read -r file; do
    echo "  ./${file#$current_dir/}"
done || echo "  No output files found"
