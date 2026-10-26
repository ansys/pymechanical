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

"""Welcome screen shown by ``ansys-mechanical --info``."""

import platform
from typing import TextIO
import warnings

import click

_ANSYS_GOLD = "#FFB71B"
_ANSYS_GOLD_RGB = (255, 183, 27)
_PROMPT = ">>> "

_LOGO = r"""
 ___      __  __        _              _         _
| _ \_  _|  \/  |___ __| |_  __ _ _ _ (_)__ __ _| |
|  _/ || | |\/| / -_) _| ' \/ _` | ' \| / _/ _` | |
|_|  \_, |_|  |_\___\__|_||_\__,_|_||_|_\__\__,_|_|
     |__/
"""

_TAGLINE = "Python interface to Ansys Mechanical: simulation, automation, and beyond."

_LINKS = {
    "Documentation": "https://mechanical.docs.pyansys.com",
    "GitHub": "https://github.com/ansys/pymechanical",
    "Report issues": "https://github.com/ansys/pymechanical/issues",
    "Discussions": "https://github.com/ansys/pymechanical/discussions",
}


def _detect_mechanical() -> tuple[str, int] | None:
    from ansys.tools.common.path import find_mechanical

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        path, version = find_mechanical()
    if not path or not version:
        return None
    return path, int(round(float(version) * 10))


def _system_info(mechanical: tuple[str, int] | None) -> dict[str, str]:
    from ansys.mechanical.core._version import __version__

    return {
        "Package version": __version__,
        "Python": platform.python_version(),
        "Platform": f"{platform.system()} {platform.machine()}",
        "Mechanical": (
            f"{mechanical[1]} ({mechanical[0]})"
            if mechanical
            else "Not detected (install Ansys Mechanical to use embedding mode)"
        ),
    }


def get_system_info() -> dict[str, str]:
    """Get the system information shown on the welcome screen.

    Returns
    -------
    dict[str, str]
        Mapping of labels to values for the package version, Python version,
        platform, and detected Mechanical installation.

    Examples
    --------
    >>> from ansys.mechanical.core._welcome import get_system_info
    >>> sorted(get_system_info())
    ['Mechanical', 'Package version', 'Platform', 'Python']
    """
    return _system_info(_detect_mechanical())


def _quick_start(version: int | None) -> list[tuple[str, list[str]]]:
    version_arg = f"version={version}" if version else ""
    return [
        (
            "Embedding mode (run Mechanical in-process):",
            ["from ansys.mechanical.core import App", f"app = App({version_arg})"],
        ),
        (
            "Remote mode (connect to a running server):",
            [
                "from ansys.mechanical.core import launch_mechanical",
                "mechanical = launch_mechanical()",
            ],
        ),
    ]


def _footer() -> str:
    return "Run 'ansys-mechanical --info' to see this again."


def _render_rich(info: dict[str, str], version: int | None, file: TextIO | None) -> None:
    from rich.align import Align
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.table import Table
    from rich.text import Text

    console = Console(file=file, highlight=False)
    logo_lines = _LOGO.strip("\n").splitlines()
    logo_width = max(len(line) for line in logo_lines)
    logo = Text(
        "\n".join(line.ljust(logo_width) for line in logo_lines), style=f"bold {_ANSYS_GOLD}"
    )
    logo.no_wrap = True

    highlighter = Syntax("", "python", theme="monokai", background_color="default")
    quick_start = Text()
    for index, (heading, code_lines) in enumerate(_quick_start(version)):
        if index:
            quick_start.append("\n\n")
        quick_start.append(heading, style="bold")
        for line in code_lines:
            quick_start.append("\n  ")
            quick_start.append(_PROMPT, style=f"bold {_ANSYS_GOLD}")
            code = highlighter.highlight(line)
            code.rstrip()
            quick_start.append_text(code)

    info_table = Table.grid(padding=(0, 2))
    info_table.add_column(style="bold")
    info_table.add_column()
    for label, value in info.items():
        style = "yellow" if label == "Mechanical" and value.startswith("Not") else "green"
        info_table.add_row(f"{label}:", Text(value, style=style))

    links = Text(" | ").join(
        Text(name, style=f"link {url} underline cyan") for name, url in _LINKS.items()
    )

    console.print(
        Group(
            Align.center(logo),
            Align.center(Text("ansys-mechanical-core", style="bold")),
            Align.center(Text(_TAGLINE, style="italic")),
            Text(),
            Align.center(Panel(info_table, title="System info", border_style="cyan")),
            Align.center(Panel(quick_start, title="Quick start", border_style=_ANSYS_GOLD)),
            Align.center(links),
            Text(),
            Align.center(Text(_footer(), style="dim")),
            Align.center(Text("PyMechanical is ready. Happy simulating!", style="bold green")),
        )
    )


def _render_plain(info: dict[str, str], version: int | None, file: TextIO | None) -> None:
    def echo(text: str = "", **style) -> None:
        click.echo(click.style(text, **style) if style else text, file=file)

    echo(_LOGO.strip("\n"), fg=_ANSYS_GOLD_RGB, bold=True)
    echo("ansys-mechanical-core", bold=True)
    echo(_TAGLINE)
    echo()
    echo("System info", fg="cyan", bold=True)
    width = max(len(label) for label in info) + 2
    for label, value in info.items():
        echo(f"  {label + ':':<{width}}{value}")
    echo()
    echo("Quick start", fg=_ANSYS_GOLD_RGB, bold=True)
    for index, (heading, code_lines) in enumerate(_quick_start(version)):
        if index:
            echo()
        echo(f"  {heading}", bold=True)
        for line in code_lines:
            prompt = click.style(_PROMPT, fg=_ANSYS_GOLD_RGB, bold=True)
            click.echo(f"    {prompt}{line}", file=file)
    echo()
    for name, url in _LINKS.items():
        echo(f"  {name}: {url}")
    echo()
    echo(_footer(), dim=True)
    echo("PyMechanical is ready. Happy simulating!", fg="green", bold=True)


def render_welcome(file: TextIO | None = None) -> None:
    """Print the PyMechanical welcome screen.

    The screen uses ``rich`` when it is installed and falls back to plain
    ``click`` styling otherwise.

    Parameters
    ----------
    file : TextIO, optional
        Stream to write to. The default is ``None``, in which case the
        screen is written to standard output.

    Examples
    --------
    >>> from ansys.mechanical.core._welcome import render_welcome
    >>> render_welcome()
    """
    mechanical = _detect_mechanical()
    info = _system_info(mechanical)
    version = mechanical[1] if mechanical else None
    try:
        import rich  # noqa: F401
    except ImportError:
        _render_plain(info, version, file)
    else:
        _render_rich(info, version, file)
