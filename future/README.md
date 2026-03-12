# Ansys Mechanical Future API - Multi-Version Support

This directory contains the Future API extensions for PyMechanical that support multiple Ansys Mechanical versions (24.1, 24.2, 25.1, 25.2, and 26.1).

## Overview

The Future API provides additional functionality for PyMechanical, including:
- HDF5 export capabilities with custom settings
- Extended geometry type support
- Version-aware assembly loading

## Supported Versions

- **24.1** (241) - Ansys 2024 R1
- **24.2** (242) - Ansys 2024 R2
- **25.1** (251) - Ansys 2025 R1
- **25.2** (252) - Ansys 2025 R2
- **26.1** (261) - Ansys 2026 R1

## Building the Assemblies

### Prerequisites

1. **Ansys Mechanical Installation**: You need the corresponding Ansys Mechanical versions installed
2. **Environment Variables**: Ensure `AWP_ROOT<version>` environment variables are set (e.g., `AWP_ROOT241`, `AWP_ROOT251`)
3. **.NET Framework 4.7.2** or later
4. **MSBuild** or **dotnet CLI**

### Build Scripts

#### Windows (PowerShell)
```powershell
# Build all versions
.\build_all_versions.ps1

# Build specific configuration
.\build_all_versions.ps1 -Configuration Debug

# Clean and build
.\build_all_versions.ps1 -CleanFirst
```

#### Linux (Bash)
```bash
# Build all versions
./build_all_versions.sh

# Build specific configuration
./build_all_versions.sh Release

# Clean and build
./build_all_versions.sh Release true
```

#### Python (Cross-platform)
```bash
# Build all versions
python build_all_versions.py

# Build specific versions
python build_all_versions.py --versions 251 252 261

# Build with different configuration
python build_all_versions.py --configuration Debug

# Clean and build
python build_all_versions.py --clean
```

### Manual Building

For individual versions, you can build manually:

```bash
# Example for version 25.1
dotnet build Ansys.Mechanical.Future.251.csproj --configuration Release
```

## Output Structure

After building, the assemblies will be organized as follows:

```
future/
├── bin/
│   └── x64/
│       └── Release/
│           ├── 241/
│           │   ├── Ansys.Mechanical.Future.241.dll
│           │   └── Ansys.Mechanical.Future.241.pdb
│           ├── 242/
│           │   ├── Ansys.Mechanical.Future.242.dll
│           │   └── Ansys.Mechanical.Future.242.pdb
│           ├── 251/
│           │   ├── Ansys.Mechanical.Future.251.dll
│           │   └── Ansys.Mechanical.Future.251.pdb
│           ├── 252/
│           │   ├── Ansys.Mechanical.Future.252.dll
│           │   └── Ansys.Mechanical.Future.252.pdb
│           └── 261/
│               ├── Ansys.Mechanical.Future.261.dll
│               └── Ansys.Mechanical.Future.261.pdb
```

## Usage in Python

### Method 1: Version-Aware Importer (Recommended)

```python
from ansys.mechanical.core import App
app = App(globals=globals())

# Import using the version-aware importer
from ansys.mechanical.core.embedding.future_importer import (
    ModelExtensions, ModelHDF5ExportSettings, GeometryType, TransferFileFormat
)

# Create settings
settings = ModelHDF5ExportSettings()
settings.GeometryType = GeometryType.Solid

# Use the extension method
ModelExtensions.ExportHDF5TransferFile(
    app.Model, 
    "output.h5", 
    TransferFileFormat.HDF5, 
    settings
)
```

### Method 2: Manual Loading (Fallback)

```python
from ansys.mechanical.core import App
app = App(globals=globals())

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

# Load version-specific assembly
assembly_name = f"Ansys.Mechanical.Future.{version}"
clr.AddReference(assembly_name)

# Import types
from Ansys.Mechanical.Future import ModelExtensions, ModelHDF5ExportSettings
from Ansys.Mechanical.Future.Enums import GeometryType, TransferFileFormat

# Use the API
settings = ModelHDF5ExportSettings()
settings.GeometryType = GeometryType.Solid
ModelExtensions.ExportHDF5TransferFile(app.Model, "output.h5", settings=settings)
```

## API Reference

### Classes

#### `ModelHDF5ExportSettings`
Configuration settings for HDF5 export.

**Properties:**
- `GeometryType`: Specifies the geometry type (Solid or Sheet)
- `UnitSystemType`: Specifies the unit system for export

#### `ModelExtensions`
Static class containing extension methods for the Model class.

**Methods:**
- `ExportHDF5TransferFile(model, filename, format=HDF5, settings=None)`: Exports model to HDF5 format

### Enums

#### `GeometryType`
- `Solid`: Solid geometry type
- `Sheet`: Sheet geometry type

#### `TransferFileFormat`
- `HDF5`: HDF5 file format

## How Version Detection Works

1. **Initialization**: When PyMechanical initializes, it detects the Ansys version from environment variables
2. **Path Addition**: The appropriate version-specific assembly path is added to `sys.path`
3. **Assembly Loading**: The version-specific assembly (e.g., `Ansys.Mechanical.Future.251.dll`) is loaded
4. **Runtime Binding**: The appropriate Ansys libraries for that version are used

## Troubleshooting

### Common Issues

1. **Environment Variable Not Set**
   - Ensure `AWP_ROOT<version>` is set for your Ansys installation
   - Example: `AWP_ROOT251=C:\Program Files\ANSYS Inc\v251`

2. **Assembly Not Found**
   - Make sure you've built the assembly for your version
   - Check that the DLL exists in `future/bin/x64/Release/<version>/`

3. **Version Mismatch**
   - The system automatically detects the Ansys version being used
   - Ensure the corresponding Future assembly is built and available

### Debug Mode

To enable debug logging, set the logging level in your Python script:

```python
import logging
from ansys.mechanical.core.mechanical import LOG
LOG.setLevel(logging.DEBUG)
```

## Contributing

When adding new functionality:

1. Add your code to the shared C# files (`ModelExtensions.cs`, `Enums.cs`)
2. Build all version-specific assemblies
3. Test with multiple Ansys versions
4. Update this documentation

## License

This code is licensed under the MIT License. See the main PyMechanical license for details.
