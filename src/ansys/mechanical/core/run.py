"""Convenience CLI to run mechanical."""

import asyncio
from asyncio.subprocess import PIPE
import os
import sys
import warnings

import ansys.tools.path as atp
import click

# TODO - add logging options (reuse env var based logging initialization)
# TODO - add timeout
# TODO - close mechanical automatically after script exits


async def _read_and_display(cmd):
    """Read cmd's stdout, stderr while displaying them as they arrive."""
    # start process
    process = await asyncio.create_subprocess_exec(*cmd, stdout=PIPE, stderr=PIPE)

    # read child's stdout/stderr concurrently
    stdout, stderr = [], []  # stderr, stdout buffers
    tasks = {
        asyncio.Task(process.stdout.readline()): (stdout, process.stdout, sys.stdout.buffer),
        asyncio.Task(process.stderr.readline()): (stderr, process.stderr, sys.stderr.buffer),
    }
    while tasks:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        assert done
        for future in done:
            buf, stream, display = tasks.pop(future)
            line = future.result()
            if line:  # not EOF
                buf.append(line)  # save for later
                display.write(line)  # display in terminal
                # schedule to read the next line
                tasks[asyncio.Task(stream.readline())] = buf, stream, display

    # wait for the process to exit
    rc = await process.wait()
    return rc, b"".join(stdout), b"".join(stderr)


def _run(args):
    if os.name == "nt":
        loop = asyncio.ProactorEventLoop()  # for subprocess' pipes on Windows
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()
    try:
        rc, *output = loop.run_until_complete(_read_and_display(args))
        if rc:
            sys.exit("child failed with '{}' exit code".format(rc))
    finally:
        loop.close()


@click.command()
@click.help_option("--help", "-h")
@click.option(
    "-p",
    "--project-file",
    default=None,
    help="Opens Mechanical project file (.mechdb). Cannot be mixed with -i",
)
@click.option(
    "--port",
    type=int,
    help="Start mechanical in server mode with the given port number",
)
@click.option(
    "-i",
    "--input-script",
    default=None,
    help="Name of the input Python script. Cannot be mixed with -p",
)
@click.option(
    "-s",
    "--show-welcome-screen",
    is_flag=True,
    default=False,
    help="Show the welcome screen, where you can select the file to open.\
        Only affects graphical mode",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Show a debug dialog right when the process starts.",
)
@click.option(
    "-r",
    "--revision",
    default=None,
    type=int,
    help='Ansys Revision number, e.g. "241" or "232". If none is specified\
, uses the default from ansys-tools-path',
)
@click.option(
    "-g",
    "--graphical",
    is_flag=True,
    default=False,
    help="Graphical mode",
)
def cli(
    project_file: str,
    port: int,
    debug: bool,
    input_script: str,
    revision: int,
    graphical: bool,
    show_welcome_screen: bool,
):
    """CLI tool to run mechanical.

    USAGE:

    The following example demonstrates the main use of this tool:

        $ ansys-mechanical -r 232 -g

        Starting Ansys Mechanical version 2023R2 in graphical mode...
    """
    if project_file and input_script:
        raise Exception("Cannot open a project file *and* run a script.")

    if (not graphical) and project_file:
        raise Exception("Cannot open a project file in batch mode.")

    if port:
        if project_file:
            raise Exception("Cannot open in server mode with a project file.")
        if input_script:
            raise Exception("Cannot open in server mode with an input script.")

    if not revision:
        exe, version = atp.find_mechanical()
    else:
        exe, version = atp.find_mechanical(version=revision)

    version = int(version * 10)
    version_name = atp.SUPPORTED_ANSYS_VERSIONS[version]

    args = [exe, "-DSApplet"]
    if (not graphical) or (not show_welcome_screen):
        args.append("-AppModeMech")

    if version < 232:
        args.append("-nosplash")
        args.append("-notabctrl")

    if graphical:
        mode = "Graphical"
    else:
        mode = "Batch"
        args.append("-b")

    if debug:
        os.environ["WBDEBUG_STOP"] = "1"

    if port:
        args.append("-grpc")
        args.append(str(port))

    if project_file:
        args.append("-file")
        args.append(project_file)

    if input_script:
        args.append("-script")
        args.append(input_script)

    if (not graphical) and input_script and (version < 241):
        warnings.warn(
            "Please ensure ExtAPI.Application.Close() is at the end of your script. "
            "Without this command, Batch mode will not terminate.",
            stacklevel=2,
        )

        if version < 241:
            warnings.warn(
                "Please ensure ExtAPI.Application.Close() is at the end of your script. "
                "Without this command, Batch mode will not terminate.",
                stacklevel=2,
            )

    print(f"Starting Ansys Mechanical version {version_name} in {mode} mode...")
    if port:
        # TODO - Mechanical doesn't write anything to the stdout in grpc mode
        #        when logging is off.. Ideally we les Mechanical write it, so
        #        the user only sees the message when the server is ready.
        print(f"Serving on port {port}")
    _run(args)
