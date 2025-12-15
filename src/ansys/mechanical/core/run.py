# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Convenience CLI to run mechanical."""

import asyncio
from asyncio.subprocess import PIPE
import os
import sys
import typing

import ansys.tools.common.path as atp
import click

from ansys.mechanical.core.embedding.appdata import UniqueUserProfile
from ansys.mechanical.core.feature_flags import get_command_line_arguments, get_feature_flag_names
from ansys.mechanical.core.misc import has_grpc_service_pack

DRY_RUN = False
"""Dry run constant."""

# TODO : add logging options (reuse env var based logging initialization)
# TODO : add timeout


async def _read_and_display(cmd, env, do_display: bool):
    """Read command's stdout and stderr and display them as they are processed."""
    # start process
    process = await asyncio.create_subprocess_exec(*cmd, stdout=PIPE, stderr=PIPE, env=env)
    # read child's stdout/stderr concurrently
    stdout, stderr = [], []  # stderr, stdout buffers
    tasks = {
        asyncio.Task(process.stdout.readline()): (stdout, process.stdout, sys.stdout.buffer),
        asyncio.Task(process.stderr.readline()): (stderr, process.stderr, sys.stderr.buffer),
    }
    while tasks:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        if not done:
            raise RuntimeError("Subprocess read failed: No tasks completed.")
        for future in done:
            buf, stream, display = tasks.pop(future)
            line = future.result()
            if line:  # not EOF
                buf.append(line)  # save for later
                if do_display:
                    display.write(line)  # display in terminal
                # schedule to read the next line
                tasks[asyncio.Task(stream.readline())] = buf, stream, display

    # wait for the process to exit
    rc = await process.wait()
    return rc, process, b"".join(stdout), b"".join(stderr)


def _run(args, env, check=False, display=False):
    if os.name == "nt":
        loop = asyncio.ProactorEventLoop()  # for subprocess' pipes on Windows
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()
    try:
        rc, process, *output = loop.run_until_complete(_read_and_display(args, env, display))
        if rc and check:
            sys.exit("child failed with '{}' exit code".format(rc))
    finally:
        if os.name == "nt":
            loop.close()
    return process, output


def _cli_impl(
    project_file: str = None,
    port: int = 0,
    debug: bool = False,
    input_script: str = None,
    script_args: str = None,
    exe: str = None,
    version: int = None,
    graphical: bool = False,
    show_welcome_screen: bool = False,
    private_appdata: bool = False,
    exit: bool = False,
    features: str = None,
    enginetype: str = None,
    transport_mode: str = None,
    grpc_host: str = None,
    certs_dir: str = None,
):
    if project_file and input_script:
        raise click.ClickException("Cannot open a project file *and* run a script.")

    if (not graphical) and project_file:
        raise click.ClickException("Cannot open a project file in batch mode.")

    if port:
        if project_file:
            raise click.ClickException("Cannot open in server mode with a project file.")
        if input_script:
            raise click.ClickException("Cannot open in server mode with an input script.")

    if not input_script and script_args:
        raise click.ClickException("Cannot add script arguments without an input script.")

    if enginetype and not input_script:
        raise click.ClickException("Cannot specify engine type without an input script (-i).")

    if enginetype and enginetype not in ["ironpython", "cpython"]:
        raise click.ClickException(
            f"Invalid engine type '{enginetype}'. Valid options are: ironpython, cpython"
        )

    # Validate and set defaults for gRPC options
    if port:
        # Get version for service pack detection
        detected_version = version
        supports_grpc = has_grpc_service_pack(detected_version) if detected_version else False

        # Check if version supports advanced gRPC features
        if not supports_grpc:
            if transport_mode and transport_mode != "insecure":
                raise click.ClickException(
                    f"Version {detected_version} does not support {transport_mode} transport mode. "
                    "Use --transport-mode insecure or update to Service Pack 04+."
                )
            elif not transport_mode:
                raise click.ClickException(
                    f"Version {detected_version} does not support secure gRPC options. "
                    "Use --transport-mode insecure or update to Service Pack 04+."
                )
            # Force insecure mode and show warning
            transport_mode = "insecure"
            print(f"Warning: Version {detected_version} using basic insecure connection")

        # Set defaults for supported versions
        if supports_grpc and not transport_mode:
            transport_mode = "wnua" if os.name == "nt" else "mtls"

            # Validate transport mode availability per OS
            if os.name != "nt" and transport_mode == "wnua":
                raise click.ClickException(
                    "'wnua' transport mode is not available on Linux. "
                    "Available options: 'mtls', 'insecure'"
                )

            # Set default host for all transport modes
            if not grpc_host:
                grpc_host = "localhost"

            # Validate transport mode requirements
            if transport_mode == "mtls" and not certs_dir:
                raise click.ClickException(
                    "--certs-dir is required when using 'mtls' transport mode. "
                )

    # Validate that gRPC options are only used with port
    if not port and (transport_mode or grpc_host or certs_dir):
        raise click.ClickException(
            "gRPC options (--transport-mode, --grpc-host, --certs-dir) "
            "can only be used with --port."
        )

    if script_args:
        if '"' in script_args:
            raise click.ClickException(
                "Cannot have double quotes around individual arguments in the --script-args string."
            )

    # If the input_script and port are missing in batch mode, raise an exception
    if (not graphical) and (input_script is None) and (not port):
        raise click.ClickException(
            "An input script, -i, or port, --port, are required in batch mode."
        )

    args = [exe, "-DSApplet"]
    if (not graphical) or (not show_welcome_screen):
        args.append("-AppModeMech")

    if not graphical:
        args.append("-b")

    env: typing.Dict[str, str] = os.environ.copy()
    if debug:
        env["WBDEBUG_STOP"] = "1"

    if port:
        args.append("-grpc")
        args.append(str(port))

        # Only add advanced gRPC options if version supports them
        if has_grpc_service_pack(version):
            # Add transport mode
            args.append("--transport-mode")
            args.append(transport_mode)

            # Add gRPC host
            args.append("--grpc-host")
            args.append(grpc_host)

            # Add certs directory if provided (required for mtls)
            if certs_dir:
                args.append("--certs-dir")
                args.append(certs_dir)

    if project_file:
        args.append("-file")
        args.append(project_file)

    if input_script:
        args.append("-script")
        args.append(input_script)

    if script_args:
        args.append("-ScriptArgs")
        args.append(f'"{script_args}"')

    if (not graphical) and input_script:
        exit = True

    if exit and input_script:
        args.append("-x")

    profile: UniqueUserProfile = None
    if private_appdata:
        new_profile_name = f"Mechanical-{os.getpid()}"
        profile = UniqueUserProfile(new_profile_name, dry_run=DRY_RUN)
        profile.update_environment(env)

    if not DRY_RUN:
        version_name = atp.SUPPORTED_ANSYS_VERSIONS.get(version, version)
        if graphical:
            mode = "Graphical"
        else:
            mode = "Batch"
        print(f"Starting Ansys Mechanical version {version_name} in {mode} mode...")
        if port:
            # TODO : Mechanical doesn't write anything to the stdout in grpc mode
            #        when logging is off.. Ideally we let Mechanical write it, so
            #        the user only sees the message when the server is ready.
            print(f"Serving on port {port}")

            has_sp4 = has_grpc_service_pack(version)
            if not has_sp4:
                print("Transport mode: insecure (legacy - no advanced gRPC support)")
                print("Using insecure connection - no authentication or encryption")
            else:
                print(f"Transport mode: {transport_mode}")
                print(f"gRPC host: {grpc_host}")
                if certs_dir:
                    print(f"Certificates directory: {certs_dir}")
                elif transport_mode == "mtls":
                    print("Warning: mtls mode requires --certs-dir to be specified")

                # Provide helpful information about the configuration
                if transport_mode == "wnua":
                    print(
                        "Using Windows Named User Authentication (wnua) - certificates not required"
                    )
                elif transport_mode == "insecure":
                    print("Using insecure connection - no authentication or encryption")
                elif transport_mode == "mtls":
                    if certs_dir:
                        print("Using mutual TLS (mtls) with certificate-based authentication")
                    else:
                        print("ERROR: mtls mode requires certificate directory to be specified")

                # Show OS-specific information
                if os.name != "nt":
                    print(
                        "Note: On Linux, only 'mtls' and 'insecure' transport modes are available"
                    )

    if features is not None:
        args.extend(get_command_line_arguments(features.split(";")))

    if enginetype and input_script:
        args.append("-engineType")
        args.append(enginetype)

    if DRY_RUN:
        return args, env
    else:
        _run(args, env, False, True)

    if private_appdata:
        profile.cleanup()


@click.command()
@click.help_option("--help", "-h")
@click.option(
    "-p",
    "--project-file",
    default=None,
    help="Opens Mechanical project file (.mechdb). Cannot be mixed with -i",
)
@click.option(
    "--private-appdata",
    default=None,
    is_flag=True,
    help="Make the appdata folder private.\
 This enables you to run parallel instances of Mechanical.",
)
@click.option(
    "--port",
    type=int,
    help="Start mechanical in server mode with the given port number",
)
@click.option(
    "--transport-mode",
    type=click.Choice(["wnua", "mtls", "insecure"], case_sensitive=False),
    default=None,
    help="Transport mode for gRPC connection. Default: 'wnua' on Windows, 'mtls' on Linux. "
    "Note: 'wnua' is only available on Windows; Linux supports 'mtls' and 'insecure' only",
)
@click.option(
    "--grpc-host",
    type=str,
    default=None,
    help="Host for gRPC connection. Defaults to 'localhost' for 'wnua' and 'insecure' modes",
)
@click.option(
    "--certs-dir",
    type=str,
    default=None,
    help="Directory containing certificates. Required for 'mtls' mode",
)
@click.option(
    "--features",
    type=str,
    default=None,
    help=f"Beta feature flags to set, as a semicolon delimited list.\
 Options: {get_feature_flag_names()}",
)
@click.option(
    "--enginetype",
    type=click.Choice(["ironpython", "cpython"], case_sensitive=False),
    default=None,
    help="Engine type to use with input scripts. Only applicable for version 261 "
    "when used with -i/--input-script."
    "Default is 'ironpython'.",
)
@click.option(
    "-i",
    "--input-script",
    default=None,
    help="Name of the input Python script. Cannot be mixed with -p",
)
@click.option(
    "--script-args",
    default=None,
    help='Arguments to pass into the --input-script, -i. \
Write the arguments as a string, with each argument \
separated by a comma. For example, --script-args "arg1,arg2" \
This can only be used with the --input-script argument.',
)
@click.option(
    "--exit",
    is_flag=True,
    default=None,
    help="Exit the application after running an input script. \
You can only use this command with --input-script argument (-i). \
The command defaults to true you are not running the application in graphical mode. \
The ``exit`` command is only supported in version 2024 R1 or later.",
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
    help='Ansys Revision number, e.g. "251" or "252". If none is specified\
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
    script_args: str,
    revision: int,
    graphical: bool,
    show_welcome_screen: bool,
    private_appdata: bool,
    exit: bool,
    features: str,
    enginetype: str,
    transport_mode: str,
    grpc_host: str,
    certs_dir: str,
):
    """CLI tool to run mechanical.

    USAGE:

    The following example demonstrates the main use of this tool:

        $ ansys-mechanical -r 252 -g

        Starting Ansys Mechanical version 2025R2 in graphical mode...
    """
    exe = atp.get_mechanical_path(allow_input=False, version=revision)
    version = atp.version_from_path("mechanical", exe)

    # Validate enginetype usage - must be used with input script and version 261
    if enginetype and enginetype != "ironpython" and version < 261:
        raise click.ClickException(
            "--enginetype option for cpython is only applicable for version 261 or later."
        )

    return _cli_impl(
        project_file,
        port,
        debug,
        input_script,
        script_args,
        exe,
        version,
        graphical,
        show_welcome_screen,
        private_appdata,
        exit,
        features,
        enginetype,
        transport_mode,
        grpc_host,
        certs_dir,
    )
