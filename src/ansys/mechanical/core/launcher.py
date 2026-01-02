# Copyright (C) 2022 - 2026 ANSYS, Inc. and/or its affiliates.
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
            Whether to print all output when launching and running Mechanical. The
            default is ``False``. Only set this parameter to ``True`` if you are
            debugging the startup of Mechanical.
        host : str, optional
            Default is ``127.0.0.1``.
        transport_mode : str, optional
            Use the transport mode to connect. The default is ``wnua`` on Windows and
            ``mtls`` on Linux.
            - ``insecure`` use the insecure mode.
            - ``mtls`` use the mtls mode.
            - ``wnua`` use the windows named security mode - only valid on windows.
        certs_dir : str, optional
            when the transport_mode is ``mtls``, the certificate directory must be specified
            - The default is ``certs``.
            - this directory should have ``client.cert``, ``client.key`` and ``ca.cert`` files
        """
        self.batch = batch
        self.port = port
        self.exe_file = exe_file
        self.additional_args = additional_args
        self.additional_envs = additional_envs
        self.verbose = verbose
        self.host = host
        self.certs_dir = certs_dir
        if transport_mode is None:
            if is_linux():
                transport_mode = "mtls"
            else:
                transport_mode = "wnua"
        self.transport_mode = transport_mode
        self.__ui_arg_list = ["-DSApplet", "-nosplash", "-notabctrl"]
        self.__batch_arg_list = ["-DSApplet", "-b"]

        app_mode_mech_exits = MechanicalLauncher._mode_exists(additional_args, "-AppModeMech")
        app_mode_mesh_exits = MechanicalLauncher._mode_exists(additional_args, "-AppModeMesh")
        app_mode_rest_exits = MechanicalLauncher._mode_exists(additional_args, "-AppModeRest")

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

        env_variables = self.__get_env_variables()
        args_list = self.__get_commandline_args()

        LOG.info(f"Starting the process using {args_list}.")
        if self.verbose:
            command = " ".join(args_list)
            print(f"Running {command}.")

        if is_linux():
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
            )  # nosec: B603

        LOG.info(f"Started the process:{process} using {args_list}.")

    @staticmethod
    def verify_path_exists(exe_path):
        """Throw an exception if the given exe_path does not exist.

        Parameters
        ----------
        exe_path : str
            Path to verify.
        """
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
        """Get the list of command-line arguments used while launching Mechanical.

        Returns
        -------
        list
            List of command-line arguments.
        """
        args_list = []

        exe_path = self.__get_exe_path()
        args_list.append(exe_path)

        if self.batch:
            args_list.extend(self.__batch_arg_list)
        else:  # pragma: no cover
            args_list.extend(self.__ui_arg_list)

        args_list.append("-grpc")
        args_list.append(str(self.port))

        # Check if version supports advanced gRPC features (SP04+)
        version = atp.version_from_path("mechanical", exe_path) if exe_path else None
        supports_grpc = has_grpc_service_pack(version) if version else True

        # Validate transport mode requirements
        if not supports_grpc and self.transport_mode.lower() != "insecure":
            raise Exception(
                f"Mechanical version {version} does not support secure transport modes. "
                f"Please update to Service Pack 04 or later, or use transport_mode='insecure'."
            )

        # Only add new flags if version supports them
        if supports_grpc:
            args_list.append("--grpc-host")
            args_list.append(str(self.host))

            args_list.append("--transport-mode")
            args_list.append(self.transport_mode.lower())

            args_list.append("--certs-dir")
            args_list.append(str(self.certs_dir))

        if self.additional_args is not None and isinstance(self.additional_args, list):
            LOG.info(f"Using these additional args: {self.additional_args}.")
            args_list.extend(self.additional_args)

        return args_list

    def __get_exe_path(self):
        """Get the path to the executable file used to launch Mechanical.

        Returns
        -------
        str
            Path to the executable file for launching Mechanical.
        """
        exe_path = None
        if self.exe_file is not None and isinstance(self.exe_file, str):
            exe_path = self.exe_file

        return exe_path
