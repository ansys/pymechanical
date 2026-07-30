---
applyTo: "**"
---

# PyMechanical Copilot Instructions

## Python code (`src/`)

- Line length: 100 characters (ruff enforced).
- Double quotes for strings. Spaces for indentation.
- Imports: stdlib, then third-party, then `ansys.mechanical.core`. Use `isort` groups; no wildcard imports.
- Use `pathlib.Path` instead of `os.path`.
- Docstrings: NumPy style, triple double-quotes. Class summaries end in "s" (e.g. `"""Provides..."""`); method/function summaries do not (e.g. `"""Export..."""`). `@property` uses a noun phrase.
- Every public function, method, class, and property must have a docstring with an `Examples` section.
- Type hints required on all public APIs.
- Security: no `eval`/`exec` on untrusted input; use `subprocess` with explicit argument lists only.

## Tests (`tests/`)

- One behaviour per test function. Split if a test covers more than one logical thing.
- One of these markers is required: `@pytest.mark.embedding`, `@pytest.mark.remote_session_connect`, or `@pytest.mark.embedding_scripts`.
- Add `@pytest.mark.minimum_version(NNN)` when a feature requires a specific Mechanical version.
- Name tests `test_<thing>_<condition>`.
- No inline comments or assert messages (unless ambiguous without them).
- Never assert hardcoded environment-specific values. Capture the value first, then assert relative to it.
- Do not call `embedded_app.new()` inside tests. The `make_app_reset` autouse fixture handles it.
- File order: module docstring → imports → module-level constants → test functions.
- MIT license header is added automatically by the `add-license-headers` pre-commit hook. Do not write it manually.

## Documentation (`doc/`, `*.rst`, docstrings)

- Writing style follows the Google Developer Documentation Style Guide: active voice, present tense, second person ("you"), sentence-case headings, American English.
- RST heading order: `###`, `===`, `---`, `~~~`, `+++`.
- Code entities in double backticks (`` ``ClassName`` ``), never single.
- Use `.. code-block:: python` for Python, `.. code-block:: console` for shell.
- Cross-references: use `:func:`, `:class:`, `:meth:`, `:attr:` for API and `:ref:` for internal sections.
- Vale lints RST files using `doc/.vale.ini` (Google and ANSYS vocab, `warning` minimum level).
- Before running Vale, sync the styles from the repo root:
  ```console
  vale --config=doc/.vale.ini sync
  ```
- Then lint the documentation source, excluding auto-generated folders:
  ```console
  vale --config=doc/.vale.ini --ignore-glob="*/_build/**" --ignore-glob="*/api/**" doc/source
  ```

## Pre-commit (runs automatically; do not bypass)

- `ruff` for lint and format
- `mypy` for type checking (excludes `tests/`, `examples/`, `doc/`)
- `codespell` and `typos` for spell check
- `bandit` for security scan (excludes `tests/`, `examples/`)
- `add-license-headers` for MIT header (start year 2022)
- `pyupgrade --py310-plus` to modernise syntax
