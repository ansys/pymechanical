# Welcome to PyMechanical Codespaces for developers

## Disclaimer

> **For Ansys internal use only.**
> This Codespace requires write access to the repository. External contributors
> cannot pull the private Mechanical image and the environment will not be functional.

**Use this Codespace only for developing, contributing, documenting, and
writing examples for PyMechanical.**

## What is pre-installed

- **Ansys Mechanical** at `/install/ansys_inc/v<version>/` (depends on the config you selected)
- **Python 3.12** with a virtual environment at `.venv`
- **PyMechanical** (editable install with all extras: `tests`, `graphics`,
  `doc`, `rpc`, `pim`)
- **uv** package manager
- **pre-commit** hooks (installed automatically)
- **VS Code extensions**: Python, Ruff, mypy

## How to start a Codespace

There is **no default configuration** — this is intentional. The Mechanical image is ~25 GB
and should only be pulled when you actually need it. Always use **New with options** to
consciously choose what you want:

| When you want to... | Pick |
|---|---|
| Work on PyMechanical source, tests, or docs (no Mechanical) | Any standard GitHub Codespace without a dev container config |
| Run embedding tests against a specific Mechanical version | Select the matching config below |

Six Mechanical configurations are available:

| Config | Image |
|--------|-------|
| `242` | `ghcr.io/ansys/mechanical:24.2.0` |
| `251` | `ghcr.io/ansys/mechanical:25.1.0` |
| `252` | `ghcr.io/ansys/mechanical:25.2.0` |
| `261` | `ghcr.io/ansys/mechanical:26.1.0` |
| `271` | `ghcr.io/ansys/mechanical:27.1.0` |
| `271-candidate` | `ghcr.io/ansys/mechanical:27.1_Candidate` |

1. Go to the [pymechanical](https://github.com/ansys/pymechanical) repository
2. Click **Code → Codespaces → New with options**
3. Under **Dev container configuration**, select the Mechanical version you need
4. Click **Create codespace** and wait for the build and `postCreateCommand` to finish

> **Note:** The **+** (quick-create) button has no default config and will show the
> picker automatically. Always use **New with options** for clarity.

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
