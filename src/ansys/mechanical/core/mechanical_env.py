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

"""Create environment in Linux similar to workbench and run command."""
import argparse
import os
import subprocess
import sys

from ansys.tools.path import find_mechanical


def create_env(version, aisol_path):
    """Set up the environment in Linux."""
    proc_env = os.environ.copy()

    # /install/ansys_inc/v241/aisol
    proc_env["DS_INSTALL_DIR"] = str(aisol_path)
    ds_install_dir = proc_env.get("DS_INSTALL_DIR")
    # /install/ansys_inc/v241
    proc_env[f"AWP_ROOT{version}"] = f"{ds_install_dir}/../"

    awp_root = proc_env.get(f"AWP_ROOT{version}")

    # Environment variables used by workbench (mechanical) code
    proc_env[f"AWP_LOCALE{version}"] = "en-us"
    awp_locale = proc_env.get(f"AWP_LOCALE{version}")
    # /install/ansys_inc/v241/commonfiles/language/en-us
    proc_env[f"CADOE_LIBDIR{version}"] = f"{awp_root}/commonfiles/language/{awp_locale}"
    # /install/ansys_inc/shared_files/licensing
    proc_env["ANSYSLIC_DIR"] = f"{awp_root}/../shared_files/licensing"
    # /install/ansys_inc/v241/commonfiles
    proc_env["ANSYSCOMMON_DIR"] = f"{awp_root}/commonfiles"
    # /install/ansys_inc/v241/licensingclient
    proc_env[f"ANSYSCL{version}_DIR"] = f"{awp_root}/licensingclient"

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
    ] = f"""
{awp_root}/tp/stdc++:\
{awp_root}/tp/openssl/1.1.1/linx64/lib:\
{mwhome}/lib-amd64_linux:\
{mwhome}/lib-amd64_linux_optimized:\
{ld_library_path}:\
{awp_root}/Tools/mono/Linux64/lib:\
{ds_install_dir}/lib/linx64:\
{ds_install_dir}/dll/linx64:\
{ds_install_dir}/libshared/linx64:\
{awp_root}/tp/IntelCompiler/2019.3.199/linx64/lib/intel64:\
{awp_root}/tp/IntelMKL/2020.0.166/linx64/lib/intel64:\
{awp_root}/tp/qt_fw/5.9.6/Linux64/lib:\
{awp_root}/commonfiles/CAD/Acis/linx64:\
{awp_root}/commonfiles/fluids/lib/linx64:\
{awp_root}/Framework/bin/Linux64"""

    # System path
    path = proc_env.get("PATH")
    proc_env[
        "PATH"
    ] = f"""
{mwhome}/bin-amd64_linux_optimized:\
{ds_install_dir}/CommonFiles/linx64:\
{ds_install_dir}/CADIntegration/linx64:\
{awp_root}/Tools/mono/Linux64/bin:\
{path}"""

    print(f"proc_env: {proc_env}")

    return proc_env


def run_command(proc_env, cmd):
    """Run command from user."""
    # Run the command in a subprocess and print stdout as process is running
    popen = subprocess.Popen(
        cmd,
        env=proc_env,
        stdout=subprocess.PIPE,
    )
    for line in popen.stdout:
        print(line.decode(), end="")
    popen.stdout.close()
    retcode = popen.wait()

    # Return non-zero codes
    if retcode:
        raise subprocess.CalledProcessError(retcode, cmd)


def main():
    """Run mechanical-env."""
    if "win" in sys.platform:
        print("mechanical-env is only available for Linux.")
    else:
        # Get revision number
        exe, version = find_mechanical()
        default_revn = int(version * 10)

        parser = argparse.ArgumentParser()
        # Get command from stdin
        parser.add_argument("command", nargs="*")
        parser.add_argument(
            "--revision",
            type=str,
            help='Ansys Revision number, e.g. "241" or "232".\
            If a revision number is not specified, it uses the default from \
            ansys-tools-path.',
            default=default_revn,
        )

        args = parser.parse_args()

        # If the user chooses a revision number, find the mechanical install of the given revision
        if int(args.revision) != default_revn:
            try:
                exe, version = find_mechanical(version=int(args.revision))
                version = int(version * 10)
            except ValueError as e:
                print(f"There was a ValueError for version {args.revision}.")
                exit(1)

        # Get aisol_path for Linux system
        aisol_path = os.path.dirname(exe)

        # Set command list for subprocess
        if len(args.command) == 1:
            cmd = args.command[0].split()
        else:
            cmd = args.command

        before_env = os.environ

        # If the version and aisol_path exist, run the command
        if version and aisol_path:
            proc_env = create_env(version, aisol_path)
            # run_command(proc_env, cmd)
        else:
            print("There was a problem getting the version and aisol_path")

        after_env = os.environ

        print("is before_env the same as after_env?")
        print(before_env == after_env)


if __name__ == "__main__":
    main()
