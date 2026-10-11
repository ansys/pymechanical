---
name: test
description: 'Write, review, or split PyMechanical tests. Use when writing pytest files under tests/ or tests/embedding/, reviewing existing tests for modularity, splitting monolithic tests, or adding test coverage for embedding, remote session, or CLI features. Covers test structure, assert style, fixture use, and pytest markers.'
---

# PyMechanical Test Scripts

Tests live under `tests/` (remote, CLI) and `tests/embedding/` (embedding). They use `pytest`
with custom markers and fixtures defined in `tests/conftest.py`.

---

## Test Categories

### Embedding — in-process (`@pytest.mark.embedding`)

Run inside the same Python process using a shared `embedded_app` fixture. Use for testing
`App` methods, API behaviour, and object manipulation.

```python
@pytest.mark.embedding
def test_feature_name(embedded_app):
    """Test brief description."""
    result = embedded_app.some_method()
    assert result == expected
```

### Embedding — subprocess (`@pytest.mark.embedding_scripts`)

Run a separate Python script via `subprocess`. Use for scenarios requiring process isolation
(pythonnet warnings, global importer edge cases, gallery building).

```python
@pytest.mark.embedding_scripts
def test_script_behavior(run_subprocess, rootdir, tmp_path):
    """Test brief description."""
    script = rootdir / "tests" / "scripts" / "my_script.py"
    result = run_subprocess(script)
    assert result.returncode == 0
```

### Remote session (`@pytest.mark.remote_session_connect`)

Validate the `ansys.mechanical.core.Mechanical` gRPC client against a running Mechanical server.

```python
@pytest.mark.remote_session_connect
def test_feature_name(mechanical):
    """Test brief description."""
    result = mechanical.run_python_script("2+3")
    assert result == "5"
```

---

## One Behaviour Per Test

Each test function must verify exactly one behaviour. If a test does more than one logical
thing, split it into separate functions.

**Wrong** — multiple concerns in one test:

```python
def test_license_manager(embedded_app):
    assert len(embedded_app.license_manager.get_all_licenses()) > 0
    embedded_app.license_manager.set_license_status("Ansys Mechanical Premium", False)
    assert embedded_app.license_manager.get_license_status(...) == ...Disabled
    embedded_app.license_manager.move_to_index("Ansys Mechanical Premium", 0)
    assert embedded_app.license_manager.get_all_licenses().index(...) == 0
```

**Right** — one concern per function:

```python
TEST_LICENSE = "Ansys Mechanical Premium"


def test_get_all_licenses(embedded_app):
    """Test that at least one license is available."""
    assert len(embedded_app.license_manager.get_all_licenses()) > 0


def test_set_license_status(embedded_app):
    """Test enabling and disabling a license."""
    lm = embedded_app.license_manager
    lm.set_license_status(TEST_LICENSE, False)
    assert lm.get_license_status(TEST_LICENSE) == lm._license_status.Disabled
    lm.set_license_status(TEST_LICENSE, True)
    assert lm.get_license_status(TEST_LICENSE) == lm._license_status.Enabled


def test_move_to_index(embedded_app):
    """Test moving a license to position zero."""
    lm = embedded_app.license_manager
    original_index = lm.get_all_licenses().index(TEST_LICENSE)
    assert original_index > 0
    lm.move_to_index(TEST_LICENSE, 0)
    assert lm.get_all_licenses().index(TEST_LICENSE) == 0
```

---

## Asserts

- **One assert concept per test** where possible. Multiple asserts are fine when they form a
  single logical check (for example, enable → assert enabled, disable → assert disabled).
- **No inline assert messages** unless the failure would be genuinely ambiguous without one.
  pytest already shows the values on failure.
- **Never assert against hardcoded environment-specific values** (list indices, version strings,
  file paths). Capture the value first and assert relative to it.

```python
# Wrong — hardcoded index
assert license_list.index(TEST_LICENSE) == 1

# Right — relative assertion
original = license_list.index(TEST_LICENSE)
assert original > 0
lm.move_to_index(TEST_LICENSE, 0)
assert lm.get_all_licenses().index(TEST_LICENSE) == 0
lm.reset_preference()
assert lm.get_all_licenses().index(TEST_LICENSE) != 0
```

---

## Comments

- **No inline comments** inside test bodies. The test name and docstring provide context.
- **No section dividers** (`# Enable and disable specific license`, etc.).
- A single one-line module docstring is sufficient for the file.
- Each test function has a one-line docstring describing what it verifies.

---

## Naming

- `test_<thing>_<condition>` — for example `test_session_license_invalid_type`.
- Use a module-level constant for repeated literal values:

```python
TEST_LICENSE = "Ansys Mechanical Premium"
```

---

## File Structure (in order)

1. **Module docstring** — short one-line description, e.g. `"""License manager tests."""`
2. **Imports** — stdlib → pytest → `ansys.mechanical.core` modules
3. **Module-level constants** — repeated literal values
4. **Test functions** — each decorated with the appropriate marker

---

## Import Patterns

### Embedding tests

```python
import os
from pathlib import Path
import subprocess
import sys

import pytest

from ansys.mechanical.core.embedding.app import App
from ansys.mechanical.core.embedding.background import BackgroundApp
```

### Remote tests

```python
import json
import os
from pathlib import Path

import pytest

import ansys.mechanical.core as pymechanical
```

Import only what is needed. Group: stdlib → pytest → ansys modules.

---

## Available Fixtures

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `embedded_app` | session | Shared `App` instance (embedding tests) |
| `mechanical` | session | Shared remote `Mechanical` session instance |
| `tmp_path` | function | Temporary directory unique to each test |
| `assets` | session | Path to `tests/assets/` directory |
| `rootdir` | session | Path to repository root |
| `run_subprocess` | function | Helper to run scripts in isolated subprocess |
| `pytestconfig` | session | Access to pytest configuration and CLI options |
| `capsys` | function | Capture stdout/stderr — add only when needed |

- Prefer the narrowest fixture scope that still works.
- Do not call `embedded_app.new()` manually — the `make_app_reset` autouse fixture resets it.
- Add `capsys` only to tests that capture stdout.

---

## Markers

- `@pytest.mark.embedding` — all in-process embedding tests.
- `@pytest.mark.embedding_scripts` — subprocess-isolated embedding tests.
- `@pytest.mark.remote_session_connect` — remote gRPC session tests.
- `@pytest.mark.minimum_version(261)` — tests requiring a minimum Mechanical version.

---

## Common Assertion Patterns

### Embedding — App repr

```python
app_repr_lines = repr(embedded_app).splitlines()
assert app_repr_lines[0].startswith("Ansys Mechanical")
assert app_repr_lines[1].startswith("Product Version")
```

### Embedding — save and open

```python
from tempfile import NamedTemporaryFile

project_file = tmp_path / f"{NamedTemporaryFile().name}.mechdat"
embedded_app.save_as(str(project_file))
assert project_file.exists()
```

### Embedding — version check

```python
version = embedded_app.version
assert version is not None
```

### Embedding — tree output

```python
tree_output = embedded_app.print_tree()
assert "Project" in tree_output
```

### Embedding — deprecation warning

```python
with pytest.warns(UserWarning):
    deprecated_object.old_property
```

### Remote — run Python script

```python
result = mechanical.run_python_script("2+3")
assert result == "5"
```

### Remote — run Python script returning object

```python
result = mechanical.run_python_script("ExtAPI.DataModel.Project.Name")
assert result != ""
```

### Remote — upload file

```python
mechanical.upload(file_name=str(assets / "geometry.agdb"), file_location_destination=".")
```

### Remote — download file

```python
mechanical.download("file.mechdat", target_dir=str(tmp_path))
assert (tmp_path / "file.mechdat").exists()
```

### Remote — multi-line script

```python
script = """
import json
model = ExtAPI.DataModel.Project.Model
output = json.dumps({"name": model.Name, "bodies": model.Geometry.Bodies.Count})
output
"""
result = mechanical.run_python_script(script)
data = json.loads(result)
assert data["bodies"] > 0
```

---

## Background App Testing

For `BackgroundApp` tests use the subprocess pattern. Helper scripts go in `tests/scripts/`.

```python
@pytest.mark.embedding_scripts
def test_background_app(run_subprocess, rootdir):
    """Test background app lifecycle."""
    script = rootdir / "tests" / "scripts" / "background_app_test.py"
    result = run_subprocess(script)
    assert result.returncode == 0
    assert "error" not in result.stderr.lower()
```

---

## Pytest Custom Flags (embedding)

Pass `--log-embedding=<level>` to enable the Mechanical embedding logger without changing
any test code:

```bash
pytest -m embedding -k test_set_license_status --ansys-version=261 --log-embedding=debug
```

Accepted levels: `debug`, `info`, `warning`, `error`. Omitting the flag leaves the embedding
logger unconfigured.

---

## Anti-patterns to Avoid

| Anti-pattern | Fix |
|---|---|
| Monolithic test covering all public methods | One test per behaviour |
| `assert x == 1` where `1` is environment-specific | Capture value; assert relative |
| Inline comments explaining each step | Self-explaining test name + docstring |
| `assert condition, "message"` when pytest output is clear | Plain `assert condition` |
| Catching broad exceptions to avoid test failure | Let the exception propagate |
| Calling `embedded_app.new()` inside a test | Rely on `make_app_reset` autouse fixture |
