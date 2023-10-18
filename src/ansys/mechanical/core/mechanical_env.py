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
import sys

# from ansys.tools.path import find_mechanical


def create_env(version, aisol_path):
    """Set up the environment in Linux."""
    # /install/ansys_inc/v241/aisol
    os.environ["DS_INSTALL_DIR"] = str(aisol_path)
    ds_install_dir = os.environ.get("DS_INSTALL_DIR")
    # /install/ansys_inc/v241
    os.environ[f"AWP_ROOT{version}"] = f"{ds_install_dir}/../"

    awp_root = os.environ.get(f"AWP_ROOT{version}")

    # Environment variables used by workbench (mechanical) code
    os.environ[f"AWP_LOCALE{version}"] = "en-us"
    awp_locale = os.environ.get(f"AWP_LOCALE{version}")
    # /install/ansys_inc/v241/commonfiles/language/en-us
    os.environ[f"CADOE_LIBDIR{version}"] = f"{awp_root}/commonfiles/language/{awp_locale}"
    # /install/ansys_inc/shared_files/licensing
    os.environ["ANSYSLIC_DIR"] = f"{awp_root}/../shared_files/licensing"
    # /install/ansys_inc/v241/commonfiles
    os.environ["ANSYSCOMMON_DIR"] = f"{awp_root}/commonfiles"
    # /install/ansys_inc/v241/licensingclient
    os.environ[f"ANSYSCL{version}_DIR"] = f"{awp_root}/licensingclient"

    # MainWin variables
    home = os.environ.get("HOME")
    os.environ["ANSISMAINWINLITEMODE"] = "1"
    os.environ["MWCONFIG_NAME"] = "amd64_linux"
    mwconfig_name = os.environ.get("MWCONFIG_NAME")
    os.environ["MWDEBUG_LEVEL"] = "0"
    # /install/ansys_inc/v241/commonfiles/MainWin/linx64/mw
    os.environ["MWHOME"] = f"{awp_root}/commonfiles/MainWin/linx64/mw"
    mwhome = os.environ.get("MWHOME")
    os.environ["MWOS"] = "linux"
    # /install/ansys_inc/v241/aisol/WBMWRegistry/hklm_amd64_linux.bin
    os.environ["MWREGISTRY"] = f"{ds_install_dir}/WBMWRegistry/hklm_{mwconfig_name}.bin"
    os.environ["MWRT_MODE"] = "classic"
    os.environ["MWRUNTIME"] = "1"
    os.environ["MWUSER_DIRECTORY"] = f"{home}/.mw"
    os.environ["MWDONT_XCLOSEDISPLAY"] = "1"

    # Dynamic library preload
    os.environ["LD_PRELOAD"] = "libstdc++.so.6.0.28"

    # Dynamic library load path
    ld_library_path = os.environ.get("LD_LIBRARY_PATH")
    os.environ[
        "LD_LIBRARY_PATH"
    ] = f"""
    {awp_root}/tp/stdc++:
    {awp_root}/tp/openssl/1.1.1/linx64/lib:
    {mwhome}/lib-amd64_linux:
    {mwhome}/lib-amd64_linux_optimized:
    {ld_library_path}:
    {awp_root}/Tools/mono/Linux64/lib:
    {ds_install_dir}/lib/linx64:
    {ds_install_dir}/dll/linx64:
    {ds_install_dir}/libshared/linx64:
    {awp_root}/tp/IntelCompiler/2019.3.199/linx64/lib/intel64:
    {awp_root}/tp/IntelMKL/2020.0.166/linx64/lib/intel64:
    {awp_root}/tp/qt_fw/5.9.6/Linux64/lib:
    {awp_root}/commonfiles/CAD/Acis/linx64:
    {awp_root}/commonfiles/fluids/lib/linx64:
    {awp_root}/Framework/bin/Linux64"""

    # System path
    path = os.environ.get("PATH")
    os.environ[
        "PATH"
    ] = f"""
    {mwhome}/bin-amd64_linux_optimized:
    {ds_install_dir}/CommonFiles/linx64:
    {ds_install_dir}/CADIntegration/linx64:
    {awp_root}/Tools/mono/Linux64/bin:
    {path}
    """


def run_command(cmd):
    """Run command from user."""
    print(f"running {cmd}")


def main():
    """Run mechanical-env."""
    if "win" in sys.platform:
        print("mechanical-env is only available for Linux.")
    else:
        # Get revision number
        exe, version = (r"C:\Program Files\Ansys Inc\v232\aisol", 23.2)  # find_mechanical()
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

        if int(args.revision) != default_revn:
            exe, version = (
                rf"C:\Program Files\Ansys Inc\v{int(args.revision)}\aisol",
                int(args.revision) / 10,
            )  # find_mechanical(version=int(args.revision))
            version = int(version * 10)

        aisol_path = os.path.dirname(exe)
        # print(version)
        # print(aisol_path)

        create_env(version, aisol_path)
        run_command(args.command)


if __name__ == "__main__":
    main()
