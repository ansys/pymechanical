# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
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
import warnings

import ansys.tools.path as atp
import click

from ansys.mechanical.core.embedding.appdata import UniqueUserProfile

# TODO - add logging options (reuse env var based logging initialization)
# TODO - add timeout


async def _read_and_display(cmd, env):
    """Read command's stdout and stderr and display them as they are processed."""
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


def _run(args, env):
    if os.name == "nt":
        loop = asyncio.ProactorEventLoop()  # for subprocess' pipes on Windows
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()
    try:
        rc, *output = loop.run_until_complete(_read_and_display(args, env))
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
    "-i",
    "--input-script",
    default=None,
    help="Name of the input Python script. Cannot be mixed with -p",
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
    private_appdata: bool,
    exit: bool,
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

    if (not graphical) and input_script:
        exit = True
        if version < 241:
            warnings.warn(
                "Please ensure ExtAPI.Application.Close() is at the end of your script. "
                "Without this command, Batch mode will not terminate.",
                stacklevel=2,
            )

    if exit and input_script and version >= 241:
        args.append("-x")

    profile: UniqueUserProfile = None
    env: typing.Dict[str, str] = None
    if private_appdata:
        env = os.environ.copy()
        new_profile_name = f"Mechanical-{os.getpid()}"
        profile = UniqueUserProfile(new_profile_name)
        profile.update_environment(env)

    print(f"Starting Ansys Mechanical version {version_name} in {mode} mode...")
    if port:
        # TODO - Mechanical doesn't write anything to the stdout in grpc mode
        #        when logging is off.. Ideally we let Mechanical write it, so
        #        the user only sees the message when the server is ready.
        print(f"Serving on port {port}")

    _run(args, env)

    if private_appdata:
        profile.cleanup()


class EnvironmentUpdater:
    """Updates the Environment with default and custom provided values to run in linux."""

    def __init__(self, revision):
        """Initialize Environment Updater Instance.

        Parameters
        ----------
        revision : int
            The Ansys Revision number.
        """
        self.revision = revision
        self._default_env = {
            "DS_INSTALL_DIR": "$(dirname `realpath $0`)",
            "ANSISMAINWINLITEMODE": 1,
            "MWCONFIG_NAME": "amd64_linux",
            "MWDEBUG_LEVEL": 0,
            "MWOS": "linux",
            "MWRT_MODE": "classic",
            "MWRUNTIME": 1,
            "MWDONT_XCLOSEDISPLAY": 1,
            "LD_PRELOAD": "libstdc++.so.6.0.28",
        }
        self.update_revision()

    @property
    def default_env(self):
        """Get the default environment variables."""
        return self._default_env

    def update_revision(self):
        """Update the default environment based on the provided revision."""
        try:
            self._default_env[f"AWP_ROOT{self.revision}"] = f"$DS_INSTALL_DIR/.."
            self._default_env[f"AWP_LOCALE{self.revision}"] = "en-us"
            self.default_env[
                f"CADOE_LIBDIR{self.revision}"
            ] = f"${{AWP_ROOT241}}/commonfiles/language/${{AWP_LOCALE241}}"
            self.default_env[
                "ANSYSLIC_DIR"
            ] = f"${{AWP_ROOT{self.revision}}}/../shared_files/licensing"
            self._default_env["ANSYSCOMMON_DIR"] = f"${{AWP_ROOT{self.revision}}}/commonfiles"
            self._default_env[
                f"ANSYSCL{self.revision}_DIR"
            ] = f"${{AWP_ROOT{self.revision}}}/licensingclient"
            self._default_env[
                "MWHOME"
            ] = f"${{AWP_ROOT{self.revision}}}/commonfiles/MainWin/linx64/mw"
            self._default_env[
                "MWREGISTRY"
            ] = f"${{DS_INSTALL_DIR}}/WBMWRegistry/hklm_${{MWCONFIG_NAME}}.bin"
            self._default_env["MWUSER_DIRECTORY"] = f"${{HOME}}/.mw"
            self._default_env["LD_LIBRARY_PATH"] = (
                f"${{AWP_ROOT{self.revision}}}/tp/stdc++:"
                f"${{AWP_ROOT{self.revision}}}/tp/openssl/1.1.1/linx64/lib:"
                f"${{MWHOME}}/lib-amd64_linux:"
                f"${{MWHOME}}/lib-amd64_linux_optimized:"
                f"${{LD_LIBRARY_PATH}}:"
                f"${{AWP_ROOT{self.revision}}}/Tools/mono/Linux64/lib:"
                f"${{DS_INSTALL_DIR}}/lib/linx64:"
                f"${{DS_INSTALL_DIR}}/dll/linx64:"
                f"${{DS_INSTALL_DIR}}/libshared/linx64:"
                f"${{AWP_ROOT{self.revision}}}/tp/IntelCompiler/2019.3.199/linx64/lib/intel64:"
                f"${{AWP_ROOT{self.revision}}}/tp/IntelMKL/2020.0.166/linx64/lib/intel64:"
                f"${{AWP_ROOT{self.revision}}}/tp/qt_fw/5.9.6/Linux64/lib:"
                f"${{AWP_ROOT{self.revision}}}/commonfiles/CAD/Acis/linx64:"
                f"${{AWP_ROOT{self.revision}}}/commonfiles/fluids/lib/linx64:"
                f"${{AWP_ROOT{self.revision}}}/Framework/bin/Linux64"
            )
            self._default_env["PATH"] = (
                f"${{MWHOME}}/bin-amd64_linux_optimized:"
                f"${{DS_INSTALL_DIR}}/CommonFiles/linx64:"
                f"${{DS_INSTALL_DIR}}/CADIntegration/linx64:"
                f"${{AWP_ROOT{self.revision}}}/Tools/mono/Linux64/bin:"
                f"${{PATH}}"
            )
        except:
            raise Exception("Could not set the Environment variables.")
        # Rest of the environment updates...

    def update_custom_environment(self, custom_env=None):
        """Update based on the custom provided environment variables."""
        if "=" not in custom_env:
            raise ValueError(f"Invalid custom environment variable format: {custom_env}")
        var_name, var_value = custom_env.split("=", 1)
        try:
            if "=" in var_value:
                warnings.warn(
                    f"Warning: '=' character in custom environment variable value: {var_value}",
                    stacklevel=2,
                )
            self._default_env[var_name] = var_value
        except:
            raise ValueError("Could not add custom Environment variables.")


@click.command()
@click.help_option("--help", "-h")
@click.option(
    "-r",
    "--revision",
    default=None,
    type=int,
    help='Ansys Revision number, e.g. "241" or "232". If none is specified\
, uses the default from ansys-tools-path',
)
@click.argument("custom_env", nargs=-1)
def update_environment(revision: int, custom_env):
    """Update environment variables with default values and user-defined custom variables.

    Parameters
    ----------
    revision : int
        The Ansys Revision number.
    custom_env : list
        A list of custom environment variables in the format 'name=value'.

    USAGE:

    The following example demonstrates the main use of this tool:

        $ mechanical-env -r 232 HOME=/usr/home/ LOG=1
    """
    #  Should not update env variables in Windows
    if os.name == "nt":
        print("This feature is not available in Windows !")
        return True

    # Process the custom environment variables provided as arguments
    custom_env_args = [arg for arg in custom_env if "=" in arg]
    # Gets the revision number
    if not revision:
        exe, version = atp.find_mechanical()
    else:
        exe, version = atp.find_mechanical(version=revision)
    version = int(version * 10)

    env_updater = EnvironmentUpdater(version)

    if custom_env_args:
        for arg in custom_env_args:
            env_updater.update_custom_environment(arg)
    # Print all envirornment variables

    print("-" * 30)
    print("user env")
    for key, value in env_updater.default_env.items():
        print(f"{key}: {value}")
    print("-" * 30)
    print("Current env")
    env = os.environ.copy()
    for key, value in env.items():
        print(f"{key}: {value}")
    try:
        env.update(env_updater.default_env)
    except:
        raise Exception("Could not set the environment variables.")

    print("-" * 30)
    print("updated env")
    for key, value in env.items():
        print(f"{key}: {value}")
