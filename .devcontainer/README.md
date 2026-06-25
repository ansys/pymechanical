# PyMechanical Dev Container

This directory defines a development container for
[PyMechanical](https://mechanical.docs.pyansys.com) that runs inside the Ansys
Mechanical Docker image. It mirrors the `embedding-tests` CI job exactly, so
anything that works here will work in CI.

## What you get

- **Base image**: `ghcr.io/ansys/mechanical:26.1.0` (Mechanical at
  `/install/ansys_inc/v261/`)
- **Python 3.12** managed by [uv](https://github.com/astral-sh/uv), venv at `/env`
- **Editable PyMechanical install** with all extras: `tests`, `graphics`, `doc`,
  `rpc`, `pim`
- **pre-commit hooks** installed automatically
- **VS Code** configured with Python + Ruff extensions and `/env/bin/python` as
  the interpreter

## Prerequisites

### 1. Access to the Mechanical GHCR image

The image `ghcr.io/ansys/mechanical:26.1.0` is private.

- **GitHub Codespaces**: your GitHub account must have `read:packages` access to
  the `ansys/mechanical` package. PyMechanical maintainers already have this.
- **Local Dev Containers**: run `docker login ghcr.io` with a Personal Access
  Token that has `read:packages` scope before opening VS Code.

### 2. Ansys license

The container needs `ANSYSLMD_LICENSE_FILE` set to point at a valid license
server (format: `1055@<hostname>`).

**GitHub Codespaces** — create a Codespaces secret:

1. Go to **GitHub → Settings → Secrets and variables → Codespaces**
2. Add a secret named `ANSYSLMD_LICENSE_FILE` with value `1055@my.license.server`
3. Ensure the secret is available to the `pymechanical` repository

**Local Dev Containers** — export the variable before opening VS Code:

```bash
export ANSYSLMD_LICENSE_FILE=1055@my.license.server
code .
```

## Opening the dev container

### GitHub Codespaces

Click **Code → Codespaces → Create codespace on main** (or your branch) from
the repository page. GitHub will build the image and run `postCreateCommand`
automatically.

### VS Code Dev Containers

1. Install the
   [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Open the repository folder in VS Code
3. Press `F1` → **Dev Containers: Reopen in Container**

## Running tests

After the container starts and `postCreateCommand` finishes, activate the venv
and run tests. The `mechanical-env` wrapper sets all the library paths that
Mechanical's Python embedding requires.

```bash
# Activate the venv (already active in new integrated terminals)
. /env/bin/activate

# Embedding tests (requires Xvfb for headless display, already in image)
xvfb-run mechanical-env pytest -m embedding -s

# Embedding script tests
mechanical-env pytest -m embedding_scripts -s

# CLI tests (no mechanical-env needed)
pytest -m cli -s

# All non-embedding tests
pytest -m "not embedding and not embedding_scripts and not remote_session_connect and not remote_session_launch" -s
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `ANSYSLMD_LICENSE_FILE` not set | Secret not configured | See Prerequisites section |
| `find-mechanical: command not found` | venv not active | `. /env/bin/activate` |
| `Error: cannot connect to X server` | Missing `xvfb-run` prefix | Prefix command with `xvfb-run` |
| `docker pull` fails | Not logged into GHCR | `docker login ghcr.io` |
