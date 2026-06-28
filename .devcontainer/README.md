# Welcome to PyMechanical Codespaces for developers

## Disclaimer

**Use this Codespace only for developing, contributing, documenting, and
writing examples for PyMechanical.**

## What is pre-installed

- **Ansys Mechanical 26.1** at `/install/ansys_inc/v261/`
- **Python 3.12** with a virtual environment at `.venv`
- **PyMechanical** (editable install with all extras: `tests`, `graphics`,
  `doc`, `rpc`, `pim`)
- **uv** package manager
- **pre-commit** hooks (installed automatically)
- **VS Code extensions**: Python, Ruff, mypy

## How to start a Codespace

1. Go to the [pymechanical](https://github.com/ansys/pymechanical) repository
2. Click **Code → Codespaces → Create codespace on main** (or your branch)
3. Wait for the build and `postCreateCommand` to finish

## Running Mechanical

Mechanical requires the `mechanical-env` wrapper to set library paths:

```bash
mechanical-env python
```

## Running tests

```bash
# Embedding tests (headless display via xvfb)
xvfb-run mechanical-env pytest -m embedding -s

# Embedding script tests
mechanical-env pytest -m embedding_scripts -s

# CLI tests (no mechanical-env needed)
pytest -m cli -s
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `find-mechanical: command not found` | Run `. .venv/bin/activate` |
| `Error: cannot connect to X server` | Prefix with `xvfb-run` |
| `docker pull` fails (local only) | Run `docker login ghcr.io` |

## See also

- [PyMechanical documentation](https://mechanical.docs.pyansys.com)
- [Contributing guide](https://mechanical.docs.pyansys.com/version/stable/contribute.html)
- [PyMechanical Issues](https://github.com/ansys/pymechanical/issues)
- [PyMechanical Discussions](https://github.com/ansys/pymechanical/discussions)

Happy coding!
