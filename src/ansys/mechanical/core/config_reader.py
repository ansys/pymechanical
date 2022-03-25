import configparser
import os
import errno
import logging

# from src.mechanical.platform_helper import PlatformHelper
from ansys.mechanical.core.platform_helper import PlatformHelper


log = logging.getLogger(__name__)

class MechanicalConfigReader:
    def __init__(self, config_file="mechanical_options.ini"):
        self.__read = False
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.optionxform = str

        self.__exe_path = None
        self.__ui_arg_list = []
        self.__batch_arg_list = []
        self.__env_variables = {}

    def __str__(self):
        print(f"exe_path:{self.__exe_path}, batch_arg_list:{self.__batch_arg_list},"
              f"ui_arg_list:{self.__ui_arg_list}, env_variables:{self.env_variables}")

    def read(self):
        log.debug(f"reading options file:{self.config_file} started")
        
        if not os.path.exists(self.config_file):
            print(f"options file:{self.config_file} doesn't exist")
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.config_file)

        self.config.read(self.config_file)

        self.__exe_path = self.__get_exe_path()

        batch_args_section = self.config['batch_args']
        for key in batch_args_section:
            self.__batch_arg_list.append(batch_args_section[key])

        ui_args_section = self.config['ui_args']
        for key in ui_args_section:
            self.__ui_arg_list.append(ui_args_section[key])

        env_variables_section = self.config["environment"]
        for key in env_variables_section:
            self.__env_variables[key] = env_variables_section[key]

        self.__read = True
        log.debug(f"reading options file:{self.config_file} done")

    @property
    def exe_path(self):
        if not self.__read:
            self.read()
        return self.__exe_path

    @property
    def batch_arg_list(self):
        if not self.__read:
            self.read()
        return self.__batch_arg_list

    @property
    def ui_arg_list(self):
        if not self.__read:
            self.read()

        return self.__ui_arg_list

    @property
    def env_variables(self):
        return self.__env_variables

    def __get_exe_path(self):

        if PlatformHelper.is_windows():
            exe_path = self.__get_exe_path_windows()
            log.debug(f"windows exe path:{exe_path}")
        else:
            exe_path = self.__get_exe_path_linux()
            log.debug(f"linux exe path:{exe_path}")

        return exe_path

    def __get_exe_path_windows(self):
        grpc_section = self.config['grpc']
        if "windows_exe_path" in grpc_section:
            exe_path = grpc_section['windows_exe_path']
        elif "workbench_version" in grpc_section:
            version = grpc_section['workbench_version']
            str_awp_root = "AWP_ROOT{}".format(version)
            path_sep = os.path.sep
            exe_path = str.format(f"{os.getenv(str_awp_root)}{path_sep}aisol{path_sep}bin{path_sep}winx64{path_sep}"
                                  f"AnsysWBU.exe")
        else:
            raise RuntimeError("'workbench_version' or 'windows_exe_path' should exist in the config file")

        if not os.path.exists(exe_path):
            raise RuntimeError(f"{exe_path} doesn't exist. Couldn't construct exe_path "
                           f"tried using 'workbench_version' or 'windows_exe_path'")
        return exe_path

    def __get_exe_path_linux(self):
        grpc_section = self.config['grpc']
        if "linux_exe_path" in grpc_section:
            exe_path = grpc_section['linux_exe_path']
        else:
            raise RuntimeError("'linux_exe_path' should exist in the config file for linux")

        if not os.path.exists(exe_path):
            raise RuntimeError(f"{exe_path} doesn't exist. Couldn't construct exe_path "
                           f"tried using 'linux_exe_path'")

        return exe_path
