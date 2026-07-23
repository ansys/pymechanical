# Copyright (C) 2022 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""CLI tool for managing PyMechanical marimo notebooks.

The ``ansys-mechanical-notebook`` entry point provides subcommands to list,
copy, and launch the marimo example notebooks that are bundled with this
package.

Examples
--------
List available notebooks::

    ansys-mechanical-notebook list

Copy the valve notebook to the current directory::

    ansys-mechanical-notebook copy valve

Open the valve notebook in the marimo interactive editor::

    ansys-mechanical-notebook edit valve

Run the valve notebook as a read-only web app::

    ansys-mechanical-notebook run valve
"""

from __future__ import annotations

import importlib.resources
from pathlib import Path
import shutil
import subprocess  # nosec B404
import sys

import click

# ---------------------------------------------------------------------------
# Registry of bundled marimo notebooks
# ---------------------------------------------------------------------------

#: Maps short notebook names to their file names inside the
#: ``ansys.mechanical.core.examples.marimo`` package.
NOTEBOOKS: dict[str, str] = {
    "valve": "valve.py",
}

_NOTEBOOK_DESCRIPTIONS: dict[str, str] = {
    "valve": "Static structural analysis of a valve (embedding mode)",
}


def _notebooks_dir() -> Path:
    """Return the directory that contains the bundled marimo notebooks."""
    pkg = importlib.resources.files("ansys.mechanical.core.examples.marimo")
    return Path(str(pkg))


def _resolve_notebook(name: str) -> Path:
    """Return the absolute path to a bundled notebook by short name."""
    return _notebooks_dir() / NOTEBOOKS[name]


# ---------------------------------------------------------------------------
# CLI group
# ---------------------------------------------------------------------------


@click.group()
@click.help_option("--help", "-h")
def cli() -> None:
    r"""Manage PyMechanical marimo notebooks.

    USAGE:

    The following examples demonstrate the main use of this tool:

    \b
        $ ansys-mechanical-notebook list
        $ ansys-mechanical-notebook copy valve
        $ ansys-mechanical-notebook edit valve
        $ ansys-mechanical-notebook run  valve
    """


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------


@cli.command(name="list")
def list_notebooks() -> None:
    """List the marimo notebooks bundled with PyMechanical."""
    click.echo("Available PyMechanical marimo notebooks:\n")
    for name, filename in NOTEBOOKS.items():
        desc = _NOTEBOOK_DESCRIPTIONS.get(name, "")
        click.echo(f"  {name:<20}  {filename:<15}  {desc}")
    click.echo(
        "\nUse 'ansys-mechanical-notebook copy <name>' to copy a notebook"
        " to your working directory."
    )


@cli.command(name="copy")
@click.argument("name", type=click.Choice(list(NOTEBOOKS.keys())))
@click.option(
    "--dest",
    "-d",
    default=".",
    show_default=True,
    type=click.Path(file_okay=False, writable=True),
    help="Destination directory.",
)
def copy_notebook(name: str, dest: str) -> None:
    """Copy NAME to a local directory so you can edit and run it.

    NAME is the short notebook name (use 'list' to see all options).
    """
    src = _resolve_notebook(name)
    dst_dir = Path(dest)
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / NOTEBOOKS[name]
    shutil.copy2(src, dst)
    click.echo(f"Copied '{name}' to: {dst.resolve()}")
    click.echo("\nNext steps:")
    click.echo(f"  marimo edit {dst.resolve()}")
    click.echo(f"  marimo run  {dst.resolve()}")
    click.echo(f"  python      {dst.resolve()}")


@cli.command(name="edit")
@click.argument("name", type=click.Choice(list(NOTEBOOKS.keys())))
@click.option(
    "--dest",
    "-d",
    default=".",
    show_default=True,
    type=click.Path(file_okay=False, writable=True),
    help="Directory to copy the notebook to before opening it.",
)
def edit_notebook(name: str, dest: str) -> None:
    """Open NAME in the marimo interactive editor.

    If the notebook does not yet exist in DEST, it is copied there first.
    Requires marimo to be installed (``pip install marimo``).
    """
    _require_marimo()
    dst = _copy_if_missing(name, Path(dest))
    click.echo(f"Opening '{dst}' in the marimo editor…")
    subprocess.run([sys.executable, "-m", "marimo", "edit", str(dst)], check=False)  # nosec B603


@cli.command(name="run")
@click.argument("name", type=click.Choice(list(NOTEBOOKS.keys())))
@click.option(
    "--dest",
    "-d",
    default=".",
    show_default=True,
    type=click.Path(file_okay=False, writable=True),
    help="Directory to copy the notebook to before running it.",
)
def run_notebook(name: str, dest: str) -> None:
    """Run NAME as a read-only interactive web app.

    If the notebook does not yet exist in DEST, it is copied there first.
    Requires marimo to be installed (``pip install marimo``).
    """
    _require_marimo()
    dst = _copy_if_missing(name, Path(dest))
    click.echo(f"Running '{dst}' as a marimo web app…")
    subprocess.run([sys.executable, "-m", "marimo", "run", str(dst)], check=False)  # nosec B603


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _require_marimo() -> None:
    """Raise a :class:`click.ClickException` if marimo is not importable."""
    try:
        import marimo  # noqa: F401
    except ImportError:
        raise click.ClickException(
            "marimo is not installed.\n"
            "Install it with:  pip install 'ansys-mechanical-core[marimo]'\n"
            "  or simply:       pip install marimo"
        )


def _copy_if_missing(name: str, dest_dir: Path) -> Path:
    """Copy the notebook to *dest_dir* if it is not already there.

    Returns the destination path.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    dst = dest_dir / NOTEBOOKS[name]
    if not dst.exists():
        src = _resolve_notebook(name)
        shutil.copy2(src, dst)
        click.echo(f"Copied '{name}' to: {dst.resolve()}")
    return dst
