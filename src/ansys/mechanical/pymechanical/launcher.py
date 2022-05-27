"""Launch Mechanical in batch or UI mode."""
import errno
import logging
import os
import subprocess

from ansys.mechanical.pymechanical.platform_helper import PlatformHelper

log = logging.getLogger(__name__)


class MechanicalLauncher:
    """Launch Mechanical in batch or UI mode."""

    def __init__(self, batch, port, exe_path, additional_args, additional_envs):
        """Initialize the MechanicalLauncher.

        Parameters
        ----------
        batch : bool, optional
            Launches mechanical in batch or UI mode. Default is True
        port : int, optional
            Port to connect to the Mechanical grpc server.  Default - find a free port
        exe_path :
            Path of the Mechanical application
        additional_args : list, optional
            List of additional arguments to pass. Default - None
        additional_envs : list, optional
            List of additional environment variables to pass. Default - None
        """
        self.batch = batch
        self.port = port
        self.exe_path = exe_path
        self.additional_args = additional_args
        self.additional_envs = additional_envs
        self.__ui_arg_list = ["-DSApplet", "-nosplash", "-notabctrl", "-AppModeMech"]
        self.__batch_arg_list = ["-DSApplet", "-b", "-AppModeMech"]

    def launch(self):
        """Launch Mechanical with grpc server."""
        exe_path = self.__get_exe_path()
        if not os.path.exists(exe_path):
            print(f"startup file:{exe_path} doesn't exist")
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), exe_path)

        env_variables = self.__get_env_variables()
        args_list = self.__get_commandline_args()

        shell_value = False

        if PlatformHelper.is_windows():
            shell_value = True

        log.info(f"starting the process using {args_list}")
        process = subprocess.Popen(args_list, shell=shell_value, env=env_variables)
        log.info(f"started the process:{process} using {args_list}")

    def __get_env_variables(self):
        """Return the dictionary of environment variable used while launching Mechanical.

        Returns
        -------
        dict
            dictionary of environment variables
        """
        default_env = dict(WB1_STANDALONE="1")
        if self.additional_envs is not None and isinstance(self.additional_envs, dict):
            log.info(f"using these additional env: {self.additional_envs}")
            ansyswbu_env = {**os.environ, **default_env, **self.additional_envs}
        else:
            ansyswbu_env = {**os.environ, **default_env}

        return ansyswbu_env

    def __get_commandline_args(self):
        """Return the list of commandline arguments used while launching Mechanical.

        Returns
        -------
        list
            list of commandline arguments
        """
        args_list = []

        exe_path = self.__get_exe_path()
        args_list.append(exe_path)

        if self.batch:
            args_list.extend(self.__batch_arg_list)
        else:
            args_list.extend(self.__ui_arg_list)

        args_list.append("-grpc")
        args_list.append(str(self.port))

        if self.additional_args is not None and isinstance(self.additional_args, list):
            log.info(f"using these additional args: {self.additional_args}")
            args_list.extend(self.additional_args)

        return args_list

    def __get_exe_path(self):
        """Return the exe path used while launching Mechanical.

        Returns
        -------
        str
            exe path of the Mechanical application
        """
        if self.exe_path is not None and isinstance(self.exe_path, str):
            exe_path = self.exe_path

        return exe_path
