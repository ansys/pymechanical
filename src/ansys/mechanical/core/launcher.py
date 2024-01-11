# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
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
import subprocess

from ansys.mechanical.core import LOG
from ansys.mechanical.core.misc import is_windows


class MechanicalLauncher:
    """Launches Mechanical in batch or UI mode."""

    def __init__(
        self, batch, port, exe_path, additional_args=None, additional_envs=None, verbose=False
    ):
        """Initialize the Mechanical launcher.

        Parameters
        ----------
        batch : bool, optional
            Whether to launch Mechanical in batch mode. The default is ``True``. When ``False``,
            Mechanical is launched in UI mode.
        port : int, optional
            Port to connect to the Mechanical gRPC server. Default - find a free port
        exe_path : str
            Path to where the executable file for Mechanical is located.
        additional_args : list, optional
            List of additional arguments to pass. The default is ``None``.
        additional_envs : dict, optional
            List of additional environment variables to pass. The default is ``None``.
        verbose : bool, optional
            Whether to print all output when launching and running Mechanical. The
            default is ``False``. Only set this parameter to ``True`` if you are
            debugging the startup of Mechanical.
        """
        self.batch = batch
        self.port = port
        self.exe_path = exe_path
        self.additional_args = additional_args
        self.additional_envs = additional_envs
        self.verbose = verbose
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

        shell_value = False

        if is_windows():
            shell_value = True

        LOG.info(f"Starting the process using {args_list}.")
        if self.verbose:
            command = " ".join(args_list)
            print(f"Running {command}.")

        process = subprocess.Popen(args_list, shell=shell_value, env=env_variables)
        LOG.info(f"Started the process:{process} using {args_list}.")

    @staticmethod
    def verify_path_exists(exe_path):
        """Throw an exception if the given exe_path does not exist.

        Parameters
        ----------
        exe_path : str
            Path to verify.
        """
        if not os.path.exists(exe_path):
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
        if self.exe_path is not None and isinstance(self.exe_path, str):
            exe_path = self.exe_path

        return exe_path
