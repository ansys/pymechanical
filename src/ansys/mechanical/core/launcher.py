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

"""Launch Mechanical in batch or UI mode."""

import errno
import os
from pathlib import Path

# Subprocess is needed to start the backend. Excluding bandit check.
import subprocess  # nosec: B404

import ansys.tools.common.path as atp

from ansys.mechanical.core import LOG
from ansys.mechanical.core.misc import has_grpc_service_pack, is_linux


class MechanicalLauncher:
    """Launches Mechanical in batch or UI mode."""

    def __init__(
        self,
        batch,
        port,
        exe_file,
        additional_args=None,
        additional_envs=None,
        verbose=False,
        host="127.0.0.1",
        transport_mode=None,
        certs_dir="certs",
    ):
        """Initialize the Mechanical launcher.

        Parameters
        ----------
        batch : bool
            Whether to launch Mechanical in batch mode. The default is ``True``. When ``False``,
            Mechanical launches in UI mode.
        port : int
            Port to connect to the Mechanical gRPC server. Default - find a free port
        exe_file : str
            Path to the Mechanical executable file.
        additional_args : list, optional
            List of additional arguments to pass. The default is ``None``.
        additional_envs : dict, optional
            List of additional environment variables to pass. The default is ``None``.
        verbose : bool, optional
            Whether to print launch output. The default is ``False``. Only set this parameter to
            ``True`` if you are having trouble launching Mechanical.
        host : str, optional
            Default is ``127.0.0.1``.
        transport_mode : str, optional
            Use the transport mode to connect. The default is ``WNUA`` on Windows and
            ``MTLS`` on Linux.
        certs_dir : str, optional
            - The default is ``certs``.
        """
        # Store parameters
        self.batch = batch
        self.port = port
        self.exe_file = exe_file
        self.additional_args = additional_args or []
        self.additional_envs = additional_envs or {}
        self.verbose = verbose
        self.host = host
        # Store transport_mode, preserving case (will be normalized later if needed)
        self.transport_mode = transport_mode
        self.certs_dir = certs_dir

        # Get version from executable path
        self.version = atp.version_from_path("mechanical", exe_file) if exe_file else None

        # Check if version supports advanced gRPC features
        supports_grpc = has_grpc_service_pack(self.version) if self.version else False

        # For versions without service pack, validate transport mode
        if not supports_grpc and self.transport_mode.upper() != "INSECURE":
            if not exe_file:
                raise Exception("No executable path specified for Mechanical launcher")
            raise Exception(
                f"Mechanical version {self.version} does not support {self.transport_mode} "
                f"transport mode. Use transport_mode='insecure' or update to Service Pack 04+."
            )

        # Set default values for backward compatibility (only if not already set)
        if self.port is None:
            self.port = 10000
        if self.certs_dir is None:
            self.certs_dir = "certs"
        self.__ui_arg_list = ["-DSApplet", "-nosplash", "-notabctrl"]
        self.__batch_arg_list = ["-DSApplet", "-b"]

        app_mode_mech_exits = MechanicalLauncher._mode_exists(None, "-AppModeMech")
        app_mode_mesh_exits = MechanicalLauncher._mode_exists(None, "-AppModeMesh")
        app_mode_rest_exits = MechanicalLauncher._mode_exists(None, "-AppModeRest")

        # if we don't have -AppModeMesh or -AppModeRest or -AppModeMech in the additional args
        # then we want to start with -AppModeMech
        if not (app_mode_mesh_exits or app_mode_rest_exits or app_mode_mech_exits):
            self.__ui_arg_list.append("-AppModeMech")
            self.__batch_arg_list.append("-AppModeMech")

    @staticmethod
    def _mode_exists(additional_args, mode):
        if additional_args is not None and isinstance(additional_args, list):
            if mode.upper() in (mode_temp.upper() for mode_temp in additional_args):
                return True

        return False

    def launch(self):
        """Launch Mechanical with the gRPC server."""
        exe_path = self.__get_exe_path()
        MechanicalLauncher.verify_path_exists(exe_path)

        # Display minimal startup information only in verbose mode
        if self.verbose:
            print(f"Starting Mechanical on {self.host}:{self.port} ({self.transport_mode})")

        env_variables = self.__get_env_variables()
        args_list = self.__get_commandline_args()

        LOG.info(f"Starting the process using {args_list}.")
        if self.verbose:
            command = " ".join(args_list)
            print(f"Command: {command}")

        if is_linux():
            # In verbose mode, capture output to help debug issues
            if self.verbose:
                process = subprocess.Popen(
                    args_list,
                    start_new_session=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    env=env_variables,
                    text=True,
                    bufsize=1,
                )  # nosec: B603
            else:
                process = subprocess.Popen(
                    args_list,
                    start_new_session=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    env=env_variables,
                )  # nosec: B603
        else:
            process = subprocess.Popen(
                args_list,
                env=env_variables,
            )

        LOG.info(f"Started the process:{process} using {args_list}.")

    @staticmethod
    def verify_path_exists(exe_path):
        """Throw an exception if the given exe_path does not exist.

        Parameters
        ----------
        exe_path : str
            Path to verify.
        """
        if exe_path is None:
            raise ValueError("Executable path cannot be None")
        if not Path(exe_path).exists():
            LOG.info(f"Startup file:{exe_path} doesn't exist.")
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), exe_path)

    def __get_env_variables(self):
        """Get the dictionary of environment variables used while launching Mechanical.

        Returns
        -------
        dict
            Dictionary of environment variables.
        """
        default_env = dict(WB1_STANDALONE="1")
        if self.additional_envs is not None and isinstance(self.additional_envs, dict):
            LOG.info(f"Using these additional env: {self.additional_envs}.")
            ansyswbu_env = {**os.environ, **default_env, **self.additional_envs}
        else:
            ansyswbu_env = {**os.environ, **default_env}

        return ansyswbu_env

    def __get_commandline_args(self):
        """Get command line arguments for launching Mechanical."""
        args = [self.exe_file]

        # Extract version from executable path for service pack detection
        version = None
        if self.exe_file:
            import re

            version_match = re.search(r"v(\d{3})", str(self.exe_file))
            if version_match:
                version = int(version_match.group(1))

        # Check if version supports advanced gRPC features
        supports_grpc = has_grpc_service_pack(version) if version else False

        if self.port:
            # For versions without service pack, validate transport mode
            if not supports_grpc:
                if not self.transport_mode:
                    raise Exception(
                        f"Mechanical {version or 'unknown'} does not support secure gRPC. "
                        "Use transport_mode='insecure' or update to Service Pack 04+."
                    )
                elif self.transport_mode != "insecure":
                    raise Exception(
                        f"Mechanical {version or 'unknown'} only supports insecure mode. "
                        "Use transport_mode='insecure' or update to Service Pack 04+."
                    )

                # For older versions, use simple port argument (legacy behavior)

                # Add batch or UI mode arguments first
                if self.batch:
                    args.extend(self.__batch_arg_list)
                else:
                    args.extend(self.__ui_arg_list)

                # Add gRPC port argument
                args.extend(["-grpc", str(self.port)])

                # Note: Legacy versions (without SP04) do not support --grpc-host flag
                # They bind to 0.0.0.0 (all interfaces) by default

                return args

            # For versions with service pack support
            # Set default transport mode
            if not self.transport_mode:
                self.transport_mode = "wnua" if os.name == "nt" else "mtls"

            # Set default host only if None
            if self.host is None:
                self.host = "localhost"

            # Validate requirements for secure transport modes (skip for insecure mode)
            if self.transport_mode.lower() == "mtls":
                if not self.certs_dir:
                    raise Exception("Certificate directory is required for mtls transport mode.")
                # Certificate validation will be handled by ansys.tools.common.cyberchannel

            elif self.transport_mode.lower() == "wnua":
                # WNUA mode validation (Windows only)
                if is_linux():
                    raise Exception("WNUA transport mode is only supported on Windows.")

            # Add batch or UI mode arguments first
            if self.batch:
                args.extend(self.__batch_arg_list)
            else:
                args.extend(self.__ui_arg_list)

            # Add gRPC arguments
            args.extend(["-grpc", str(self.port)])
            args.extend(["--transport-mode", self.transport_mode])

            if self.host != "localhost":
                args.extend(["--grpc-host", self.host])

            # Only add certs_dir for secure transport modes
            if self.certs_dir and self.transport_mode.lower() != "insecure":
                args.extend(["--certs-dir", self.certs_dir])

        if self.additional_args is not None and isinstance(self.additional_args, list):
            LOG.info(f"Using these additional args: {self.additional_args}.")
            args.extend(self.additional_args)

        return args

    def __get_exe_path(self):
        """Get the path to the executable file used to launch Mechanical.

        Returns
        -------
        str
            Path to the executable file for launching Mechanical.
        """
        if self.exe_file is not None and isinstance(self.exe_file, str):
            return self.exe_file
        else:
            raise ValueError("No executable path specified for Mechanical launcher")
