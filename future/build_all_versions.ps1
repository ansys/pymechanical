#!/usr/bin/env pwsh
# Build script for Ansys.Mechanical.Future assemblies for all versions
# This script builds the Future assembly for versions 24.1, 24.2, 25.1, 25.2, and 26.1

param(
    [string]$Configuration = "Release",
    [switch]$CleanFirst = $false
)

$ErrorActionPreference = "Stop"

Write-Host "Building Ansys.Mechanical.Future assemblies for all versions..." -ForegroundColor Green

$versions = @("241", "242", "251", "252", "261")
$currentDir = Get-Location

foreach ($version in $versions) {
    Write-Host "`nBuilding version $version..." -ForegroundColor Yellow
    
    $envVar = "AWP_ROOT$version"
    $awpRoot = [Environment]::GetEnvironmentVariable($envVar)
    
    if (-not $awpRoot) {
        Write-Warning "Environment variable $envVar not found. Skipping version $version."
        continue
    }
    
    if (-not (Test-Path $awpRoot)) {
        Write-Warning "Path $awpRoot does not exist. Skipping version $version."
        continue
    }
    
    Write-Host "  Using $envVar = $awpRoot"
    
    $projectFile = "Ansys.Mechanical.Future.$version.csproj"
    
    if (-not (Test-Path $projectFile)) {
        Write-Error "Project file $projectFile not found!"
        continue
    }
    
    try {
        if ($CleanFirst) {
            Write-Host "  Cleaning project..."
            dotnet clean $projectFile --configuration $Configuration --verbosity quiet
        }
        
        Write-Host "  Building project..."
        dotnet build $projectFile --configuration $Configuration --verbosity minimal --nologo
        
        $outputPath = "bin\x64\$Configuration\$version\Ansys.Mechanical.Future.$version.dll"
        if (Test-Path $outputPath) {
            Write-Host "  ✓ Successfully built: $outputPath" -ForegroundColor Green
        } else {
            Write-Error "  ✗ Build failed - output file not found: $outputPath"
        }
        
    } catch {
        Write-Error "  ✗ Build failed for version $version`: $_"
    }
}

Write-Host "`nBuild process completed!" -ForegroundColor Green
Write-Host "`nOutput directory structure:" -ForegroundColor Cyan
Get-ChildItem -Path "bin\x64\$Configuration" -Recurse -Filter "*.dll" | ForEach-Object {
    Write-Host "  $($_.FullName.Replace($currentDir, '.'))" -ForegroundColor Gray
}
