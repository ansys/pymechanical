# PyMechanical Copilot Instructions

## Overview

PyMechanical is a Python interface for Ansys Mechanical with **two operational modes**:

### 1. Remote Session Mode (gRPC)
Connects to a running Mechanical instance via gRPC for client-server workflows.

```python
import ansys.mechanical.core as pymechanical

mechanical = pymechanical.launch_mechanical()
result = mechanical.run_python_script("2+3")
```

- **Implementation**: `src/ansys/mechanical/core/mechanical.py`
- **Tests**: Use markers `remote_session_launch` or `remote_session_connect`

### 2. Embedded Instance Mode
Embeds Mechanical directly in the Python process for local automation.

```python
import ansys.mechanical.core as pymechanical

app = pymechanical.App(globals=globals())
print(DataModel.Project.ProjectDirectory)
```

- **Implementation**: `src/ansys/mechanical/core/embedding/app.py`
- **Tests**: Use marker `embedding`

## Code Style

- **Line limit**: 100 characters
- **Formatter/Linter**: Ruff
- **Quote style**: Double quotes
- **Docstrings**: NumPy convention
- **Logging**: Use `logging` module, not `print()`. Add `logger = logging.getLogger(__name__)` to modules.

Always run `pre-commit run --all-files` before committing.

## Documentation Style

- **Format**: Sphinx RST
- **Linting**: Vale with PyAnsys vocabulary

For any documentation changes under the `doc/` folder, always run:
```bash
vale --config=doc/.vale.ini sync
vale --config=doc/.vale.ini doc
```

## Key Directories

| Path | Description |
|------|-------------|
| `src/ansys/mechanical/core/` | Main package source |
| `src/ansys/mechanical/core/embedding/` | Embedded mode implementation |
| `tests/` | Test suite |
| `tests/embedding/` | Embedding-specific tests |
| `examples/` | Example scripts |
| `doc/` | Sphinx documentation |

## Environment Variables

- `AWP_ROOT` — Ansys installation root
- `PYMECHANICAL_PORT` — Port for gRPC connection
- `PYMECHANICAL_START_INSTANCE` — Whether to start new instance
- `NUM_CORES` — Number of cores for solving

## AI Assistance Resources

### Custom Agents
Specialized agents for specific tasks (use `@agent-name` to invoke):
- **@Embedding Expert** — Expert in embedding mode development and helpers
- **@Remote Session Expert** — Expert in gRPC remote session workflows

### Agent Skills
Domain expertise automatically loaded when relevant:
- **Testing Strategy** — Test organization, markers, fixtures, and best practices
- **Documentation** — Docstring standards, Sphinx, and example documentation

### Reusable Prompts
Templates for common tasks (use `/prompt-name` to invoke):
- **/create-example** — Generate new example scripts with proper structure
- **/add-test** — Add tests with correct markers and patterns
- **/add-helper** — Create new helper methods in Helpers class

To use these resources:
```
# Invoke custom agent
@Embedding Expert help me create a new geometry import helper

# Use a reusable prompt
/create-example for topology optimization workflow

# Skills are automatically activated based on context
```
