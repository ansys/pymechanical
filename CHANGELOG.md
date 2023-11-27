# CHANGELOG

All notable changes to PyMechanical will be documented in this file. This
project adheres to [Semantic Versioning](https://semver.org/).

This document follows the conventions laid out in [Keep a CHANGELOG](https://keepachangelog.com/en/1.0.0).

## [Unreleased]()

### Added

- Add codeql.yml for security checks ([#423](https://github.com/ansys/pymechanical/pull/423))
- add readonly flag and assertion ([#441](https://github.com/ansys/pymechanical/pull/441))

### Fixed

 - Fix enum printout ([#421](https://github.com/ansys/pymechanical/pull/421))
 - fix appdata tests ([#425](https://github.com/ansys/pymechanical/pull/425))
 - Run all embedding tests & fix appdata tests ([#433](https://github.com/ansys/pymechanical/pull/433))
 - unset all logging environment variables ([#434](https://github.com/ansys/pymechanical/pull/434))
 - pytest --ansys-version dependent on existing install ([#439](https://github.com/ansys/pymechanical/pull/439))
 - Fix app.save method for saving already saved project in current session ([#453](https://github.com/ansys/pymechanical/pull/453))
 - Flexible version for embedding & remote example ([#459](https://github.com/ansys/pymechanical/pull/459))
 - Fix obsolete API call in embedding test ([#456](https://github.com/ansys/pymechanical/pull/456))
 - Fix ignored env passing to cli ([#465](https://github.com/ansys/pymechanical/pull/465)
 - Fix private appdata environment variables and folder layout ([#474](https://github.com/ansys/pymechanical/pull/474))
 - Fix hanging embedding tests ([#498](https://github.com/ansys/pymechanical/pull/498))

### Changed

 - Update python minimum requirement from 3.8 to 3.9 ([#484](https://github.com/ansys/pymechanical/pull/484))
 - remove version limit for protobuf ([#432](https://github.com/ansys/pymechanical/pull/432))
 - remove legacy configuration test ([#436](https://github.com/ansys/pymechanical/pull/436))
 - Update examples page ([#450](https://github.com/ansys/pymechanical/pull/450))
 - remove unneeded try/except ([#457](https://github.com/ansys/pymechanical/pull/457))
 - Updated wording for revn-variations section ([#458](https://github.com/ansys/pymechanical/pull/458))
 - Update temporary file creation in test_app ([#466](https://github.com/ansys/pymechanical/pull/466))
 - Remove .reuse and LICENSES directories & bump add-license-header version ([#496](https://github.com/ansys/pymechanical/pull/496))

### Dependencies
- Update ``pre-commit`` ([#431](https://github.com/ansys/pymechanical/pull/431), [#471](https://github.com/ansys/pymechanical/pull/471), [#489](https://github.com/ansys/pymechanical/pull/489))
- Bump `numpydoc` from 1.5.0 to 1.6.0 ([#428](https://github.com/ansys/pymechanical/pull/428))
- Bump `ansys-sphinx-theme` from 0.11.2 to 0.12.5 ([#427](https://github.com/ansys/pymechanical/pull/427), [#463](https://github.com/ansys/pymechanical/pull/463), [#480](https://github.com/ansys/pymechanical/pull/480), [#493](https://github.com/ansys/pymechanical/pull/493))
- Bump `grpcio` from 1.58.0 to 1.59.3 ([#429](https://github.com/ansys/pymechanical/pull/429), [#485](https://github.com/ansys/pymechanical/pull/485), [#504](https://github.com/ansys/pymechanical/pull/504))
- Bump `actions/checkout` from 3 to 4 ([#426](https://github.com/ansys/pymechanical/pull/426))
- Bump `pyvista` from 0.42.2 to 0.42.3 ([#446](https://github.com/ansys/pymechanical/pull/446))
- Bump `ansys-sphinx-theme` from 0.12.1 to 0.12.2 ([#447](https://github.com/ansys/pymechanical/pull/447))
- Bump `stefanzweifel/git-auto-commit-action` from 4 to 5 ([#448](https://github.com/ansys/pymechanical/pull/448))
- Bump `numpy` from 1.26.0 to 1.26.2 ([#464](https://github.com/ansys/pymechanical/pull/464), [#495](https://github.com/ansys/pymechanical/pull/495))
- Bump `pypandoc` from 1.11 to 1.12 ([#470](https://github.com/ansys/pymechanical/pull/470))
- Bump `imageio` from 2.31.5 to 2.33.0 ([#469](https://github.com/ansys/pymechanical/pull/469), [#487](https://github.com/ansys/pymechanical/pull/487), [#503](https://github.com/ansys/pymechanical/pull/503))
- Bump `add-license-headers` from v0.1.3 to v0.2.0 ([#472](https://github.com/ansys/pymechanical/pull/472))
- Bump `panel` from 1.2.3 to 1.3.2 ([#479](https://github.com/ansys/pymechanical/pull/479), [#486](https://github.com/ansys/pymechanical/pull/486), [#510](https://github.com/ansys/pymechanical/pull/510))
- Bump `pytest` from 7.4.2 to 7.4.3 ([#482](https://github.com/ansys/pymechanical/pull/482))
- Bump `tj-actions/changed-files` from 39 to 40 ([#477](https://github.com/ansys/pymechanical/pull/477))
- Bump `plotly` from 5.17.0 to 5.18.0 ([#478](https://github.com/ansys/pymechanical/pull/478))
- Bump `pandas` from 2.1.1 to 2.1.3 ([#481](https://github.com/ansys/pymechanical/pull/481), [#494](https://github.com/ansys/pymechanical/pull/494))
- Bump `matplotlib` from 3.8.0 to 3.8.2 ([#488](https://github.com/ansys/pymechanical/pull/488), [#502](https://github.com/ansys/pymechanical/pull/502))

## [0.10.4](https://github.com/ansys/pymechanical/releases/tag/v0.10.4) - October 6 2023

### Dependencies

- Update `ansys_mechanical_api` from 0.1.0 to 0.1.1 ([#444](https://github.com/ansys/pymechanical/pull/444))

## [0.10.3](https://github.com/ansys/pymechanical/releases/tag/v0.10.3) - September 26 2023

### Added

-   Set up daily run for 241 testing and added manual inputs for workflow dispatch (#385)
-   add option to include enums in global variables (#394)
-   add experimental libraries method (#395)
-   add nonblocking sleep (#399)
-   Add test case for exporting off screen image([#400](https://github.com/ansys/pymechanical/pull/400))
-   Warn for obsolete apis (#409)

### Fixed

-   Fix embedded testing for all python version in CI/CD ([#393](https://github.com/ansys/pymechanical/pull/393))
-   fix broken link (#397)
-   use Application.Exit() in 241+ (#396)
-   Fix stale globals by wrapping them (#398)
-   Fix API documentation (#411)
-   doc fix (#412)

### Dependencies

- Bump `sphinx` from 7.2.5 to 7.2.6 ([#403](https://github.com/ansys/pymechanical/pull/403))
- Bump `matplotlib` from 3.7.2 to 3.8.0 ([#404](https://github.com/ansys/pymechanical/pull/404)
- Bump `imageio-ffmpeg` from 0.4.8 to 0.4.9 ([#405](https://github.com/ansys/pymechanical/pull/405)
- Bump `ansys-sphinx-theme` from 0.11.1 to 0.11.2 ([#406](https://github.com/ansys/pymechanical/pull/406))
- Bump `plotly` from 5.16.1 to 5.17.0 ([#407](https://github.com/ansys/pymechanical/pull/407))
- Bump `docker/login-action` from 2 to 3 ([#408](https://github.com/ansys/pymechanical/pull/408))
- Bump `pyvista` from 0.42.1 to 0.42.2 ([#414](https://github.com/ansys/pymechanical/pull/414))

## [0.10.2](https://github.com/ansys/pymechanical/releases/tag/v0.10.2) - September 8 2023

### Added

-   Max parallel 2 for embedding tests - ci_cd.yml (#341)
-   New features for ansys-mechanical console script (#343)
-   Add a "Documentation and issues" section to README and doc landing page (#347)
-   Dependabot changelog automation (#354)
-   Follow up of dependabot automated changelog (#359)
-   Add license headers to files in src (#373)

### Changed

-   Remove library-namespace from CI/CD (#342)
-   Bump grpcio from 1.56.2 to 1.57.0 (#349)
-   Bump plotly from 5.15.0 to 5.16.0 (#348)
-   Bump sphinxcontrib-websupport from 1.2.4 to 1.2.6 (#350)
-   Bump ansys-sphinx-theme from 0.10.2 to 0.10.3 (#351)
-   pre-commit autoupdate ([#362](https://github.com/ansys/pymechanical/pull/362)), ([#380](https://github.com/ansys/pymechanical/pull/380)), ([#391](https://github.com/ansys/pymechanical/pull/391))

### Fixed

-   Fix private appdata issue (#344)
-   Fix issues with PyPIM object.inv location (#345)

### Dependencies
- Bump `plotly` from 5.16.0 to 5.16.1 ([#357](https://github.com/ansys/pymechanical/pull/357))
- Bump `sphinx` from 7.1.2 to 7.2.5 ([#358](https://github.com/ansys/pymechanical/pull/358), [#378](https://github.com/ansys/pymechanical/pull/378))
- Bump `sphinx-gallery` from 0.13.0 to 0.14.0 ([#361](https://github.com/ansys/pymechanical/pull/361))
- Bump `ansys-sphinx-theme` from 0.10.3 to 0.11.1 ([#360](https://github.com/ansys/pymechanical/pull/360), [#387](https://github.com/ansys/pymechanical/pull/387))
- Bump `pytest-print` from 0.3.3 to 1.0.0 ([#369](https://github.com/ansys/pymechanical/pull/369))
- Bump `tj-actions/changed-files` from 37 to 39 ([#367](https://github.com/ansys/pymechanical/pull/367), [#386](https://github.com/ansys/pymechanical/pull/386))
- Bump `imageio` from 2.31.1 to 2.31.2 ([#370](https://github.com/ansys/pymechanical/pull/370))
- Bump `pytest` from 7.4.0 to 7.4.2 ([#375](https://github.com/ansys/pymechanical/pull/375), [#389](https://github.com/ansys/pymechanical/pull/389))
- Bump `actions/checkout` from 3 to 4 ([#379](https://github.com/ansys/pymechanical/pull/379))
- Bump `imageio` from 2.31.2 to 2.31.3 ([#376](https://github.com/ansys/pymechanical/pull/376))
- Bump `sphinx-notfound-page` from 1.0.0rc1 to 1.0.0 ([#374](https://github.com/ansys/pymechanical/pull/374))
- Bump `pyvista` from 0.42.0 to 0.42.1 ([#388](https://github.com/ansys/pymechanical/pull/388))

## [0.10.1](https://github.com/ansys/pymechanical/releases/tag/v0.10.1) - August 8 2023

### Changed

-   Bump ansys-sphinx-theme from 0.10.0 to 0.10.2 (#337)
-   Update clr-loader dependency (#339)

## [0.10.0](https://github.com/ansys/pymechanical/releases/tag/v0.10.0) - August 7 2023

### Added

-   Added warning for ansys-mechanical when provided an input script (#319)
-   Add changelog check to CI/CD (#322)
-   Added version check for ansys-mechanical warning message (#323)
-   Added TempPathFactory to test_app_save_open (#332)

### Changed

-   Update python minimum requirement from 3.7 to 3.8 (#333)
-   Minor private appdata updates (#335)

### Fixed

-   Broken links (#316)
-   Remove project lock file on close (#320)
-   Fixed warning message for ansys-mechanical (#326)

## [0.9.3](https://github.com/ansys/pymechanical/releases/tag/v0.9.3) - July 27 2023

### Added

-   Add ansys-mechanical console script (#297)
-   addin configuration and tests (#308)

### Changed

-   Bump matplotlib from 3.7.1 to 3.7.2 (#294)
-   Bump pyvista from 0.40.0 to 0.40.1 (#293)
-   Bump sphinx-autodoc-typehints from 1.23.0 to 1.23.3 (#284)
-   Bump patch version (#292)
-   Remove pkg-resources and importlib_metadata (#300)
-   Bump grpcio from 1.56.0 to 1.56.2 (#305)
-   Bump pyvista from 0.40.1 to 0.41.1 (#306)

### Fixed

-   Update code snippet for accessing project directory. (#295)
-   Added import logging to doc file (#299)
-   Fix version variable issue running "ansys-mechanical -r {revn} -g" (#302)
-   Update wording in running_mechanical.rst (#303)

## [0.9.2](https://github.com/ansys/pymechanical/releases/tag/v0.9.1) - July 7 2023

### Added

-   Added private AppData functionality to embedding (#285)

### Fixed

-   Updated pythonnet warning message (#286)

### Changed

-   Bump pytest from 7.3.2 to 7.4.0 (#282)
-   Bump grpcio from 1.54.2 to 1.56.0 (#283)

## [0.9.1](https://github.com/ansys/pymechanical/releases/tag/v0.9.1) - June 21 2023

### Added

-   Add version configuration for embedding tests (#270)

### Changed

-   Bump pytest-print from 0.3.1 to 0.3.2 (#273)

### Fixed

-   FIX: Use updated ansys-tools-path to resolve - missing 1 required positional argument: 'exe_loc' issue (#280)

## [0.9.0](https://github.com/ansys/pymechanical/releases/tag/v0.9.0) - June 13 2023

### Added

-   link to pymechanical remote sessions examples (#252)
-   add doc to run script without embedding (#262)
-   pre-commit autoupdate (#269)

### Changed

-   Bump ansys-sphinx-theme from 0.9.8 to 0.9.9 (#248)
-   Bump grpcio from 1.54.0 to 1.54.2 (#249)
-   Bump sphinx from 6.2.0 to 6.2.1 (#250)
-   change image tag in ci/cd (#254)
-   Bump pyvista from 0.39.0 to 0.39.1 (#256)
-   Standardizing data paths (#257)
-   Bump imageio from 2.28.1 to 2.30.0 (#258)
-   Bump pytest-cov from 4.0.0 to 4.1.0 (#259)
-   Bump imageio from 2.30.0 to 2.31.0 (#264)
-   Bump pytest from 7.3.1 to 7.3.2 (#267)
-   Bump plotly from 5.14.1 to 5.15.0 (#268)

### Fixed

-   FIX: GitHub organization rename to Ansys (#251)
-   fix examples links (#253)
-   fix windows pythonnet warning unit tests (#260)

## [0.8.0](https://github.com/ansys/pymechanical/releases/tag/v0.8.0) - May 12 2023

### Added

-   changelog (#222)
-   add link to embedding examples (#228)
-   Add `close()` method to `Ansys.Mechanical.Embedding.Application`. See (#229)
-   Add check if pythonnet exists in the user environment (#235)

### Changed

-   cleanup docker ignore file (#206)
-   Update contributing.rst (#213)
-   Bump sphinx-autodoc-typehints from 1.22 to 1.23.0 (#215)
-   Bump pytest from 7.3.0 to 7.3.1 (#216)
-   Bump sphinx-gallery from 0.12.2 to 0.13.0 (#217)
-   Bump sphinx-copybutton from 0.5.1 to 0.5.2 (#218)
-   Bump sphinx-design from 0.3.0 to 0.4.1 (#219)
-   Remove python 3.7 (#230)
-   Use ansys-tools-path (#231)
-   Bump sphinx from 6.2.0 to 7.0.0 (#232)
-   Bump imageio from 2.28.0 to 2.28.1 (#233)
-   ignore generated *.ipynb, *.py, *.rst, *.md5, *.png and *.pickle files (#239)
-   Bump pyvista from 0.38.5 to 0.39.0 (#245)

### Fixed

-   FIX: not necessary anymore to update apt-get (#220)
-   Include amd folder for mapdl solver in the docker image. (#200)
-   Remove jscript references from tests/ folder (#205)
-   Fixes the windows executable path for standalone mechanical (#214)
-   FIX: run_python_script* return empty string for objects that cannot be returned as string (#224)
-   call `new()` in the BUILDING_GALLERY constructor of `Ansys.Mechanical.Embedding.Application` (#229)
-   fix documentation link (#234)
-   changed python doc url to fix doc pipeline error (#236)
-   Docker dependencies to support topo and smart tests (#237)

## [0.7.3](https://github.com/ansys/pymechanical/releases/tag/v0.7.3) - April 20 2023

### Changed

-   Reuse instance of embedded application when building example gallery (#221)

## [0.7.2](https://github.com/ansys/pymechanical/releases/tag/v0.7.2) - April 13 2023

### Changed

-   Bump plotly from 5.14.0 to 5.14.1 (#197)
-   Bump pytest from 7.2.2 to 7.3.0 (#196)
-   Bump peter-evans/create-or-update-comment from 2 to 3 (#195)
-   Bump ansys-sphinx-theme from 0.9.6 to 0.9.7 (#198)

### Fixed

-   Fixed documentation for updating global variables (#203)
-   Remove references to unsupported legacy jscript APIs (#205)
-   Clean up docker image (#206, #200)

## [0.7.1](https://github.com/ansys/pymechanical/releases/tag/v0.7.1) - April 10 2023

First public release of PyMechanical
