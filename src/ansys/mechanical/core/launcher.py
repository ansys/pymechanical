import os
import subprocess
import logging

from ansys.mechanical.core.config_reader import MechanicalConfigReader
from ansys.mechanical.core.platform_helper import PlatformHelper


log = logging.getLogger(__name__)


class MechanicalLauncher:
    def __init__(self, batch, port, options_file_path):
        self.batch = batch
        self.port = port
        self.options_file_path = options_file_path
        self.config = MechanicalConfigReader(self.options_file_path)

    def launch(self):
        self.config.read()

        env_variables = self.__get_env_variables()
        args_list = self.__get_commandline_args()

        shell_value = False

        if PlatformHelper.is_windows():
            shell_value = True

        log.debug(f"starting the process using {args_list}")
        process = subprocess.Popen(args_list, shell=shell_value, env=env_variables)
        log.debug(f"started the process:{process} using {args_list}")

    def __get_env_variables(self):
        custom_env = self.config.env_variables
        log.debug(f"using these custom env: {custom_env}")
        ansyswbu_env = {**os.environ, **custom_env}
        return ansyswbu_env

    def __get_commandline_args(self):
        args_list = []

        exe_path = self.__get_exe_path()
        args_list.append(exe_path)

        if self.batch:
            args_list.extend(self.config.batch_arg_list)
        else:
            args_list.extend(self.config.ui_arg_list)

        args_list.append("-grpc")
        args_list.append(str(self.port))

        return args_list

    def __get_exe_path(self):
        exe_path = self.config.exe_path
        return exe_path
