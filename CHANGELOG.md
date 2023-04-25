# CHANGELOG

All notable changes to Python.NET will be documented in this file. This
project adheres to [Semantic Versioning](https://semver.org/).

This document follows the conventions laid out in [Keep a CHANGELOG](https://keepachangelog.com/en/1.0.0).

## [Unreleased][]

### Added

-   changelog (#222)

### Changed

-   Bump sphinx-design from 0.3.0 to 0.4.1 (#219)
-   Bump sphinx-copybutton from 0.5.1 to 0.5.2 (#218)
-   Bump sphinx-gallery from 0.12.2 to 0.13.0 (#217)
-   Bump sphinx-autodoc-typehints from 1.22 to 1.23.0 (#215)
-   cleanup docker ignore file (#206)
-   Update contributing.rst (#213)
-   Bump pytest from 7.3.0 to 7.3.1 (#216)

### Fixed

-   FIX: not necessary anymore to update apt-get (#220)
-   Include amd folder for mapdl solver in the docker image. (#200)
-   Remove jscript references from tests/ folder (#205)
-   Fixes the windows executable path for standalone mechanical (#214)
-   FIX: run_python_script* return empty string for objects that cannot be returned as string (#224)

## [0.7.3](https://github.com/pyansys/pymechanical/releases/tag/v0.7.3) - April 20 2023

### Changed

-   Reuse instance of embedded application when building example gallery (#221)

## [0.7.2](https://github.com/pyansys/pymechanical/releases/tag/v0.7.2) - April 13 2023

### Changed

-   Bump plotly from 5.14.0 to 5.14.1 (#197)
-   Bump pytest from 7.2.2 to 7.3.0 (#196)
-   Bump peter-evans/create-or-update-comment from 2 to 3 (#195)
-   Bump ansys-sphinx-theme from 0.9.6 to 0.9.7 (#198)

### Fixed

-   Fixed documentation for updating global variables (#203)
-   Remove references to unsupported legacy jscript APIs (#205)
-   Clean up docker image (#206, #200)

## [0.7.1](https://github.com/pyansys/pymechanical/releases/tag/v0.7.1) - April 10 2023

First public release of PyMechanical