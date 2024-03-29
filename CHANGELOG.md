# CHANGELOG

All notable changes to PyMechanical will be documented in this file. This
project adheres to [Semantic Versioning](https://semver.org/).

This document follows the conventions laid out in [Keep a CHANGELOG](https://keepachangelog.com/en/1.0.0).

This project uses [towncrier](https://towncrier.readthedocs.io/) and the changes for the upcoming release can be found in <https://github.com/ansys/pymechanical/tree/main/doc/changelog.d/>.

<!-- towncrier release notes start -->

## [0.10.8](https://github.com/ansys/pymechanical/releases/tag/v0.10.8) - March 18 2024

### Added
- Add poster ([#642](https://github.com/ansys/pymechanical/pull/642))
- Add LS Dyna unit test ([#584](https://github.com/ansys/pymechanical/pull/584))

### Fixed
- Add logo for dark theme ([#601](https://github.com/ansys/pymechanical/pull/601))
- Architecture doc ([#612](https://github.com/ansys/pymechanical/pull/612))
- Put remote example before embedding example ([#621](https://github.com/ansys/pymechanical/pull/621))
- Minor updates to Architecture doc ([#618](https://github.com/ansys/pymechanical/pull/618))
- Add MechanicalEnums ([#626](https://github.com/ansys/pymechanical/pull/626))
- Update Release action to use Stable version of Mechanical ([#628](https://github.com/ansys/pymechanical/pull/628))
- Update nightly run image version ([#636](https://github.com/ansys/pymechanical/pull/636))
- Update logo without slash ([#640](https://github.com/ansys/pymechanical/pull/640))

### Changed
- Update ``pre-commit`` ([#610](https://github.com/ansys/pymechanical/pull/610))
- Update vale version to 3.1.0 ([#613](https://github.com/ansys/pymechanical/pull/613))
- Update timeout for actions ([#631](https://github.com/ansys/pymechanical/pull/631))
- Update cheat sheet with ansys-sphinx-theme ([#638](https://github.com/ansys/pymechanical/pull/638))

### Dependencies
- Bump `ansys-sphinx-theme` from 0.13.4 to 0.14.0 ([#608](https://github.com/ansys/pymechanical/pull/608))
- Bump `plotly` from 5.18.0 to 5.20.0 ([#605](https://github.com/ansys/pymechanical/pull/605), [#644](https://github.com/ansys/pymechanical/pull/644))
- Bump `pypandoc` from 1.12 to 1.13 ([#609](https://github.com/ansys/pymechanical/pull/609))
- Bump `pytest` from 8.0.0 to 8.1.1 ([#606](https://github.com/ansys/pymechanical/pull/606), [#623](https://github.com/ansys/pymechanical/pull/623), [#634](https://github.com/ansys/pymechanical/pull/634))
- Bump `grpcio` from 1.60.1 to 1.62.1 ([#620](https://github.com/ansys/pymechanical/pull/620), [#635](https://github.com/ansys/pymechanical/pull/635))
- Bump `pandas` from 2.2.0 to 2.2.1 ([#619](https://github.com/ansys/pymechanical/pull/619))
- Bump `matplotlib` from 3.8.2 to 3.8.3 ([#607](https://github.com/ansys/pymechanical/pull/607))
- Bump `ansys-mechanical-env` from 0.1.3 to 0.1.4 ([#624](https://github.com/ansys/pymechanical/pull/624))
- Bump `pyvista` from 0.43.3 to 0.43.4 ([#643](https://github.com/ansys/pymechanical/pull/643))

## [0.10.7](https://github.com/ansys/pymechanical/releases/tag/v0.10.7) - February 13 2024

### Added
- Upload 241 docker files ([#567](https://github.com/ansys/pymechanical/pull/567))
- Add pre-commit hooks ([#575](https://github.com/ansys/pymechanical/pull/575))
- Add Automatic version update for Mechanical scripting external links ([#585](https://github.com/ansys/pymechanical/pull/585))
- Add PyMechanical logo ([#592](https://github.com/ansys/pymechanical/pull/592))

### Changed
- Update getting started page ([#561](https://github.com/ansys/pymechanical/pull/561))
- Update 232 to 241 in docs, docstrings, examples, and tests ([#566](https://github.com/ansys/pymechanical/pull/566))
- Update workflow versions to run 241 and 242 ([#590](https://github.com/ansys/pymechanical/pull/590))

### Dependencies
- Bump `pyvista` from 0.43.1 to 0.43.3 ([#564](https://github.com/ansys/pymechanical/pull/564), [#598](https://github.com/ansys/pymechanical/pull/598))
- Bump `sphinxcontrib-websupport` from 1.2.6 to 1.2.7 ([#562](https://github.com/ansys/pymechanical/pull/562))
- Bump `ansys-sphinx-theme` from 0.13.0 to 0.13.4 ([#563](https://github.com/ansys/pymechanical/pull/563), [#586](https://github.com/ansys/pymechanical/pull/586), [#596](https://github.com/ansys/pymechanical/pull/596))
- Bump `pandas` from 2.1.4 to 2.2.0 ([#571](https://github.com/ansys/pymechanical/pull/571))
- Bump `sphinxemoji` from 0.2.0 to 0.3.1 ([#569](https://github.com/ansys/pymechanical/pull/569))
- Bump `tj-actions/changed-files` from 41 to 42 ([#572](https://github.com/ansys/pymechanical/pull/572))
- Bump `panel` from 1.3.6 to 1.3.8 ([#570](https://github.com/ansys/pymechanical/pull/570), [#579](https://github.com/ansys/pymechanical/pull/579))
- Bump `peter-evans/create-or-update-comment` from 3 to 4 ([#576](https://github.com/ansys/pymechanical/pull/576))
- Bump `pytest` from 7.4.4 to 8.0.0 ([#577](https://github.com/ansys/pymechanical/pull/577))
- Bump `sphinx-autodoc-typehints` from 1.25.2 to 2.0.0 ([#578](https://github.com/ansys/pymechanical/pull/578), [#597](https://github.com/ansys/pymechanical/pull/597))
- Update ``pre-commit`` ([#580](https://github.com/ansys/pymechanical/pull/580), [#599](https://github.com/ansys/pymechanical/pull/599))
- Bump ``ansys.mechanical.env`` from 0.1.2 to 0.1.3 ([#583](https://github.com/ansys/pymechanical/pull/583))
- Bump `sphinx-autobuild` from 2021.3.14 to 2024.2.4 ([#588](https://github.com/ansys/pymechanical/pull/588))
- Bump `pytest-sphinx` from 0.5.0 to 0.6.0 ([#587](https://github.com/ansys/pymechanical/pull/587))
- Bump `grpcio` from 1.60.0 to 1.60.1 ([#589](https://github.com/ansys/pymechanical/pull/589))
- Bump `numpy` from 1.26.3 to 1.26.4 ([#595](https://github.com/ansys/pymechanical/pull/595))
- Bump `imageio` from 2.33.1 to 2.34.0 ([#594](https://github.com/ansys/pymechanical/pull/594))
- Bump `mikepenz/action-junit-report` from 3 to 4 ([#593](https://github.com/ansys/pymechanical/pull/593))

## [0.10.6](https://github.com/ansys/pymechanical/releases/tag/v0.10.6) - January 11 2024

### Added

- Add release note configuration ([#512](https://github.com/ansys/pymechanical/pull/512))
- Add 242 to scheduled nightly run ([#519](https://github.com/ansys/pymechanical/pull/519))
- Add transaction for embedding ([#542](https://github.com/ansys/pymechanical/pull/542))

### Fixed

- Fix pymeilisearch name typo and favicon ([#538](https://github.com/ansys/pymechanical/pull/538))
- Update the gif to reduce the whitespace ([#540](https://github.com/ansys/pymechanical/pull/540))
- Update ansys/actions to v5 ([#541](https://github.com/ansys/pymechanical/pull/541))
- Fix cli find mechanical ([#550](https://github.com/ansys/pymechanical/pull/550))

### Changed

- Update LICENSE ([#548](https://github.com/ansys/pymechanical/pull/548))
- Update license headers and package versions ([#556](https://github.com/ansys/pymechanical/pull/556))

### Dependencies

- Bump `github/codeql-action` from 2 to 3 ([#532](https://github.com/ansys/pymechanical/pull/532))
- Update ``pre-commit`` ([#537](https://github.com/ansys/pymechanical/pull/537), [#545](https://github.com/ansys/pymechanical/pull/545), [#553](https://github.com/ansys/pymechanical/pull/553))
- Bump `pyvista` from 0.43.0 to 0.43.1 ([#536](https://github.com/ansys/pymechanical/pull/536))
- Bump `panel` from 1.3.4 to 1.3.6 ([#535](https://github.com/ansys/pymechanical/pull/535), [#543](https://github.com/ansys/pymechanical/pull/543))
- Bump `actions/upload-artifact` and `actions/dwonload-artifact`from 3 to 4 ([#533](https://github.com/ansys/pymechanical/pull/533))
- Bump `jupyter-sphinx` from 0.4.0 to 0.5.3 ([#547](https://github.com/ansys/pymechanical/pull/547))
- Bump `tj-actions/changed-files` from 40 to 41 ([#544](https://github.com/ansys/pymechanical/pull/544))
- Bump `pytest` from 7.4.3 to 7.4.4 ([#546](https://github.com/ansys/pymechanical/pull/546))
- Bump `add-license-headers` from 0.2.2 to 0.2.4 ([#549](https://github.com/ansys/pymechanical/pull/549))
- Bump `numpy` from 1.26.2 to 1.26.3 ([#551](https://github.com/ansys/pymechanical/pull/551))

## [0.10.5](https://github.com/ansys/pymechanical/releases/tag/v0.10.5) - December 15, 2023

### Added

- Add codeql.yml for security checks ([#423](https://github.com/ansys/pymechanical/pull/423))
- add readonly flag and assertion ([#441](https://github.com/ansys/pymechanical/pull/441))
- Add PyMeilisearch in documentation ([#508](https://github.com/ansys/pymechanical/pull/508))
- Add cheetsheat and improve example visibility ([#506](https://github.com/ansys/pymechanical/pull/506))
- Add mechanical-env to workflow ([#521](https://github.com/ansys/pymechanical/pull/521))
- Add doc pdf build to workflow ([#529](https://github.com/ansys/pymechanical/pull/529))

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
 - Fix ansys-mechanical finding path ([#516](https://github.com/ansys/pymechanical/pull/516))

### Changed
 - Update ``pre-commit`` ([#528](https://github.com/ansys/pymechanical/pull/528))
 - Update python minimum requirement from 3.8 to 3.9 ([#484](https://github.com/ansys/pymechanical/pull/484))
 - remove version limit for protobuf ([#432](https://github.com/ansys/pymechanical/pull/432))
 - remove legacy configuration test ([#436](https://github.com/ansys/pymechanical/pull/436))
 - Update examples page ([#450](https://github.com/ansys/pymechanical/pull/450))
 - remove unneeded try/except ([#457](https://github.com/ansys/pymechanical/pull/457))
 - Updated wording for revn-variations section ([#458](https://github.com/ansys/pymechanical/pull/458))
 - Update temporary file creation in test_app ([#466](https://github.com/ansys/pymechanical/pull/466))
 - Remove .reuse and LICENSES directories & bump add-license-header version ([#496](https://github.com/ansys/pymechanical/pull/496))
 - Replace workbench_lite with mechanical-env in the docs ([#522](https://github.com/ansys/pymechanical/pull/522))

### Dependencies
- Update ``pre-commit`` ([#431](https://github.com/ansys/pymechanical/pull/431), [#471](https://github.com/ansys/pymechanical/pull/471), [#489](https://github.com/ansys/pymechanical/pull/489))
- Bump `numpydoc` from 1.5.0 to 1.6.0 ([#428](https://github.com/ansys/pymechanical/pull/428))
- Bump `ansys-sphinx-theme` from 0.11.2 to 0.12.5 ([#427](https://github.com/ansys/pymechanical/pull/427), [#463](https://github.com/ansys/pymechanical/pull/463), [#480](https://github.com/ansys/pymechanical/pull/480), [#493](https://github.com/ansys/pymechanical/pull/493))
- Bump `grpcio` from 1.58.0 to 1.60.0 ([#429](https://github.com/ansys/pymechanical/pull/429), [#485](https://github.com/ansys/pymechanical/pull/485), [#504](https://github.com/ansys/pymechanical/pull/504), [#527](https://github.com/ansys/pymechanical/pull/527))
- Bump `actions/checkout` from 3 to 4 ([#426](https://github.com/ansys/pymechanical/pull/426))
- Bump `pyvista` from 0.42.2 to 0.43.0 ([#446](https://github.com/ansys/pymechanical/pull/446), [#526](https://github.com/ansys/pymechanical/pull/526))
- Bump `ansys-sphinx-theme` from 0.12.1 to 0.12.2 ([#447](https://github.com/ansys/pymechanical/pull/447))
- Bump `stefanzweifel/git-auto-commit-action` from 4 to 5 ([#448](https://github.com/ansys/pymechanical/pull/448))
- Bump `numpy` from 1.26.0 to 1.26.2 ([#464](https://github.com/ansys/pymechanical/pull/464), [#495](https://github.com/ansys/pymechanical/pull/495))
- Bump `pypandoc` from 1.11 to 1.12 ([#470](https://github.com/ansys/pymechanical/pull/470))
- Bump `imageio` from 2.31.5 to 2.33.1 ([#469](https://github.com/ansys/pymechanical/pull/469), [#487](https://github.com/ansys/pymechanical/pull/487), [#503](https://github.com/ansys/pymechanical/pull/503), [#524](https://github.com/ansys/pymechanical/pull/524))
- Bump `add-license-headers` from v0.1.3 to v0.2.0 ([#472](https://github.com/ansys/pymechanical/pull/472))
- Bump `panel` from 1.2.3 to 1.3.4 ([#479](https://github.com/ansys/pymechanical/pull/479), [#486](https://github.com/ansys/pymechanical/pull/486), [#510](https://github.com/ansys/pymechanical/pull/510), [#518](https://github.com/ansys/pymechanical/pull/518))
- Bump `pytest` from 7.4.2 to 7.4.3 ([#482](https://github.com/ansys/pymechanical/pull/482))
- Bump `tj-actions/changed-files` from 39 to 40 ([#477](https://github.com/ansys/pymechanical/pull/477))
- Bump `plotly` from 5.17.0 to 5.18.0 ([#478](https://github.com/ansys/pymechanical/pull/478))
- Bump `pandas` from 2.1.1 to 2.1.4 ([#481](https://github.com/ansys/pymechanical/pull/481), [#494](https://github.com/ansys/pymechanical/pull/494), [#525](https://github.com/ansys/pymechanical/pull/525))
- Bump `matplotlib` from 3.8.0 to 3.8.2 ([#488](https://github.com/ansys/pymechanical/pull/488), [#502](https://github.com/ansys/pymechanical/pull/502))
- Bump `sphinx-gallery` from 0.14.0 to 0.15.0 ([#509](https://github.com/ansys/pymechanical/pull/509))
- Bump `actions/labeler` from 4 to 5 ([#517](https://github.com/ansys/pymechanical/pull/517))
- Bump `actions/setup-python` from 4 to 5 ([#523](https://github.com/ansys/pymechanical/pull/523))

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
