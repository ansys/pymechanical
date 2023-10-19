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

"""Create environment in Linux similar to workbench and run a command."""
import argparse
import os
import subprocess
import sys

from ansys.tools.path import find_mechanical


def create_env(revn, aisol_path):
    """
    Set up the environment to run an embedded instance or embedding tests.

    Parameters
    ----------
    revn: int
        Ansys revision number for the Mechanical installation.
    aisol_path: str
        Path to the Mechanical installation's aisol directory given the revn.

    Returns
    -------
    os.environ
        Environment for subprocess to use when running the command.
    """
    proc_env = os.environ.copy()

    # /install/ansys_inc/v241/aisol
    proc_env["DS_INSTALL_DIR"] = str(aisol_path)
    ds_install_dir = proc_env.get("DS_INSTALL_DIR")
    # /install/ansys_inc/v241
    proc_env[f"AWP_ROOT{revn}"] = f"{ds_install_dir}/.."
    awp_root = proc_env.get(f"AWP_ROOT{revn}")

    # Environment variables used by workbench (mechanical) code
    proc_env[f"AWP_LOCALE{revn}"] = "en-us"
    awp_locale = proc_env.get(f"AWP_LOCALE{revn}")
    # /install/ansys_inc/v241/commonfiles/language/en-us
    proc_env[f"CADOE_LIBDIR{revn}"] = f"{awp_root}/commonfiles/language/{awp_locale}"
    # /install/ansys_inc/shared_files/licensing
    proc_env["ANSYSLIC_DIR"] = f"{awp_root}/../shared_files/licensing"
    # /install/ansys_inc/v241/commonfiles
    proc_env["ANSYSCOMMON_DIR"] = f"{awp_root}/commonfiles"
    # /install/ansys_inc/v241/licensingclient
    proc_env[f"ANSYSCL{revn}_DIR"] = f"{awp_root}/licensingclient"

    # MainWin variables
    home = proc_env.get("HOME")
    proc_env["ANSISMAINWINLITEMODE"] = "1"
    proc_env["MWCONFIG_NAME"] = "amd64_linux"
    mwconfig_name = proc_env.get("MWCONFIG_NAME")
    proc_env["MWDEBUG_LEVEL"] = "0"
    # /install/ansys_inc/v241/commonfiles/MainWin/linx64/mw
    proc_env["MWHOME"] = f"{awp_root}/commonfiles/MainWin/linx64/mw"
    mwhome = proc_env.get("MWHOME")
    proc_env["MWOS"] = "linux"
    # /install/ansys_inc/v241/aisol/WBMWRegistry/hklm_amd64_linux.bin
    proc_env["MWREGISTRY"] = f"{ds_install_dir}/WBMWRegistry/hklm_{mwconfig_name}.bin"
    proc_env["MWRT_MODE"] = "classic"
    proc_env["MWRUNTIME"] = "1"
    proc_env["MWUSER_DIRECTORY"] = f"{home}/.mw"
    proc_env["MWDONT_XCLOSEDISPLAY"] = "1"

    # Dynamic library preload
    proc_env["LD_PRELOAD"] = "libstdc++.so.6.0.28"

    # Dynamic library load path
    ld_library_path = proc_env.get("LD_LIBRARY_PATH")
    proc_env[
        "LD_LIBRARY_PATH"
    ] = f"""{awp_root}/tp/stdc++:\
{awp_root}/tp/openssl/1.1.1/linx64/lib:\
{mwhome}/lib-amd64_linux:\
{mwhome}/lib-amd64_linux_optimized:\
{ld_library_path}\
{awp_root}/Tools/mono/Linux64/lib:\
{ds_install_dir}/lib/linx64:\
{ds_install_dir}/dll/linx64:\
{ds_install_dir}/libshared/linx64:\
{awp_root}/tp/IntelCompiler/2019.3.199/linx64/lib/intel64:\
{awp_root}/tp/IntelMKL/2020.0.166/linx64/lib/intel64:\
{awp_root}/tp/qt_fw/5.9.6/Linux64/lib:\
{awp_root}/commonfiles/CAD/Acis/linx64:\
{awp_root}/tp/nss/3.89/lib:\
{awp_root}/commonfiles/fluids/lib/linx64:\
{awp_root}/Framework/bin/Linux64"""

    # System path
    path = proc_env.get("PATH")
    proc_env[
        "PATH"
    ] = f"""{mwhome}/bin-amd64_linux_optimized:\
{ds_install_dir}/CommonFiles/linx64:\
{ds_install_dir}/CADIntegration/linx64:\
{awp_root}/Tools/mono/Linux64/bin:\
{path}"""

    return proc_env


def run_command(proc_env, cmd):
    """
    Run command from user.

    Parameters
    ----------
    proc_env: os.environ
        Environment for the process to run in
    cmd: str
        Command the user wants to run in the ``proc_env``.

    Examples
    --------
    Runs the user specified command in the process environment created
    in the ``create_env(revn, aisol_path)`` function.

    This is for running an embedded instance of pymechanical, or the
    embedding tests in pytest. Double quotes are required around
    the command if it contains arguments or flags. Another option is
    to use double hyphens before the command instead of double quotes
    if the command contains arguments or flags:
    ``mechanical-env -- my_command``.

    >>> mechanical-env "pytest -m embedding -k appdata"
    Prints the stdout of the pytest process

    >>> mechanical-env -- pytest -m embedding -k appdata
    Prints the stdout of the pytest process

    >>> mechanical-env python
    Returns a python shell that user can interact with
    """
    # Run the command in a subprocess
    popen = subprocess.Popen(
        cmd,
        env=proc_env,
        stdout=subprocess.PIPE,
    )
    # Print the output of the subprocess as it runs
    for line in popen.stdout:
        print(line.decode(), end="")
        # Leave loop if the workflow doc-build message says, "make: Leaving directory"
        if "make: Leaving directory" in line.decode():
            break
    popen.stdout.close()

    # Wait for process to finish and get return code
    retcode = popen.wait()

    # Raise CalledProcessError for non-zero codes (other than 6)
    # Ignore retcode of 6 since Mechanical crashes on close for Linux
    if (retcode == 0) or (retcode == -6):
        pass
    else:
        raise subprocess.CalledProcessError(retcode, cmd)


def main():
    """Set arguments and run the command using mechanical-env."""
    if "win" in sys.platform:
        print("mechanical-env is only available for Linux.")
    else:
        # Get default revision number from system for args.revision
        exe, revn = find_mechanical()
        revn = int(revn * 10)

        parser = argparse.ArgumentParser()
        # Get command from stdin
        parser.add_argument("command", nargs="*")
        # Get user selected revision number, otherwise default to revn set above
        parser.add_argument(
            "--revision",
            type=str,
            help='Ansys Revision number, e.g. "241" or "232".\
            If a revision number is not specified, it uses the default from \
            ansys-tools-path.',
            default=revn,
        )

        # Parse arguments
        args = parser.parse_args()

        # If the user chooses a revision number that is not the default,
        # find the mechanical install of the user selected revision
        if int(args.revision) != revn:
            exe, revn = find_mechanical(version=int(args.revision))
            revn = int(revn * 10)

        # Get aisol_path for Linux system
        aisol_path = os.path.dirname(exe)

        # Set command list for subprocess
        if len(args.command) == 1:
            cmd = args.command[0].split()
        else:
            cmd = args.command

        # If the revision number and aisol_path exist, run the command
        if revn and aisol_path:
            proc_env = create_env(revn, aisol_path)
            run_command(proc_env, cmd)
        else:
            raise Exception(
                f"There was a problem getting the revn and/or aisol_path.\
                \nrevn: {revn}\naisol_path: {aisol_path}"
            )


if __name__ == "__main__":
    main()
