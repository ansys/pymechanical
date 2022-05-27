"""Connect to Mechanical grpc server and issues commands."""
from contextlib import closing
import datetime
import logging.config
import os
import platform
import socket
import time

import ansys.platform.instancemanagement as pypim
import grpc

from ansys.mechanical.pymechanical.launcher import MechanicalLauncher
import ansys.mechanical.pymechanical.mechanical_pb2 as mechanical_pb2
import ansys.mechanical.pymechanical.mechanical_pb2_grpc as mechanical_pb2_grpc
from ansys.mechanical.pymechanical.platform_helper import PlatformHelper

"""
# typical logging.ini
[loggers]
keys=root

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
;level=DEBUG
level=INFO
handlers=consoleHandler

[handler_consoleHandler]
class=StreamHandler
formatter=simpleFormatter

[formatter_simpleFormatter]
format=%(asctime)s %(levelname)-8s %(name)-10s: %(message)s
"""
# to use the logging from the python client code that uses this package
# logging_file_path = r"c:\mechanical\logging.ini"
# logging.config.fileConfig(logging_file_path, disable_existing_loggers=False)

log = logging.getLogger(__name__)


class Mechanical(object):
    """Connect to Mechanical grpc server and issues commands."""

    # default port
    default_port = 10000

    # default version
    default_version = "222"

    def __init__(self):
        """Initialize the member variable to default values."""
        self.ip_address = None
        self.port = None
        self.channel = None
        self.stub = None
        self.batch = False
        self.wait_time = -1
        self.exe_path = None
        self.additional_args = None
        self.additional_envs = None
        self.version = None
        self.pypim_instance = None

    def __construct_exe_path(self):
        """Construct the exe path based on the environment variable."""
        if self.version is None:
            raise ValueError("version information is needed for constructing the exe path")

        env_name = f"AWP_ROOT{self.version}"
        awp_root_path = os.environ[env_name]
        if awp_root_path == "":
            raise ValueError(f"AWP_ROOT{self.version} is not defined in the environment variable")

        if PlatformHelper.is_windows():
            exe_path = os.path.join(awp_root_path, r"aisol\bin\winx64\AnsysWBU.exe")
            if not os.path.exists(exe_path):
                raise ValueError(f"{exe_path} doesn't exist")
        else:
            exe_path = os.path.join(awp_root_path, r"aisol/.workbench")
            if not os.path.exists(exe_path):
                raise ValueError(f"{exe_path} doesn't exist")

        log.info(f"constructed exe_path is {exe_path}")

        self.exe_path = exe_path

    @staticmethod
    def find_free_port():
        """Find the free open port on the host."""
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(("", 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def __launch_using_pypim(self):
        """Launch using pypim."""
        pim = pypim.connect()
        instance = pim.create_instance(product_name="mechanical", product_version=self.version)
        self.pypim_instance = instance
        log.debug("pypim wait for ready started")
        instance.wait_for_ready()
        log.debug("pypim wait for ready done")
        channel = instance.build_grpc_channel(
            options=[("grpc.max_receive_message_length", 8 * 1024**2)]
        )
        self.channel = channel
        self.stub = mechanical_pb2_grpc.MechanicalServiceStub(self.channel)
        self.wait_till_mechanical_is_ready(self.wait_time)
        log.info("mechanical is ready to accept grpc calls")

    def connect(self, port=None, ip_address="127.0.0.1"):
        """Connect to the grpc server running inside Mechanical.

        Parameters
        ----------
        port :
            Port number to connect to the Mechanical grpc server, default is 10000
        ip_address :
            IP address where Mechanical grpc server is running, default is loopback address
        """
        if self.stub is not None:
            raise RuntimeError("Mechanical already connected. Exit first and then connect.")

        if pypim.is_configured():
            log.debug("launch using pypim started")
            self.__launch_using_pypim()
            log.debug("launch using pypim done")
            return

        if port is None:
            self.port = Mechanical.default_port

        self.ip_address = ip_address
        self.port = port
        self.__connect()

    def launch(
        self,
        batch=True,
        port=None,
        wait_time=-1,
        exe_path=None,
        additional_args=None,
        additional_envs=None,
        version=None,
        use_loopback_address=False,
    ):
        """Launch the Mechanical in batch or UI mode.

        Parameters
        ----------
        batch : bool, optional
            Launches mechanical in batch or UI mode. Default is True
        port : int, optional
            Port to connect to the Mechanical grpc server.  Default - find a free port
        wait_time : int , optional
            Maximum time to wait to connect to the Mechanical grpc server. Default - no limit
        exe_path :
            Path of the Mechanical application
        additional_args : list, optional
            List of additional arguments to pass. Default - None
        additional_envs : list, optional
            List of additional environment variables to pass. Default - None
        version : string, optional
            Version number of the Mechanical product to use. Default: 222
        use_loopback_address : bool, optional
            Use loopback address 127.0.0.1 or not - Default - False
        """
        if self.stub is not None:
            raise RuntimeError("Mechanical already launched. Exit first and then launch.")

        if version is None:
            self.version = Mechanical.default_version
        else:
            if isinstance(version, str):
                self.version = version
            else:
                raise ValueError("'version' should be a string. Example is '222'.")

        self.wait_time = wait_time

        if pypim.is_configured():
            self.__launch_using_pypim()
            return

        log.debug(f"launch started with batch={batch}")
        self.batch = batch
        if port is None:
            self.port = Mechanical.find_free_port()
            log.info(f"using the next available port: {self.port}")
        else:
            self.port = port

        self.exe_path = exe_path
        self.additional_args = additional_args
        self.additional_envs = additional_envs
        self.use_loopback_address = use_loopback_address

        self.ip_address = self.__get_ip()

        if self.exe_path is None:
            self.__construct_exe_path()

        log.debug(f"version number used: {version}")

        self.__launch()
        log.debug(f"launch done with batch={batch}")

    def wait_till_mechanical_is_ready(self, wait_time=-1):
        """Wait till mechanical is ready.

        Parameters
        ----------
        wait_time : int, optional
            Maximum allowable time to connect to the Mechanical grpc server
        """
        time_1 = datetime.datetime.now()

        sleep_time = 0.5
        if wait_time == -1:
            log.info("going to try until the mechanical grpc server is ready")
        else:
            log.info(f"going to try for {wait_time} seconds to connect to mechanical grpc server")

        while not self.__isMechanicalReady():
            time_2 = datetime.datetime.now()
            time_interval = time_2 - time_1
            time_interval_seconds = int(time_interval.total_seconds())

            log.debug(f"mechanical is not ready. waiting so far {time_interval_seconds}")
            if self.wait_time != -1:
                if time_interval_seconds > wait_time:
                    log.debug(
                        f"allowed wait time {wait_time} seconds. "
                        f"waited for {time_interval_seconds} seconds,"
                        f" before throwing error"
                    )
                    raise RuntimeError(
                        f"Couldn't connect to mechanical. "
                        f"waited for {time_interval_seconds} seconds"
                    )

            time.sleep(sleep_time)

        time_2 = datetime.datetime.now()
        time_interval = time_2 - time_1
        time_interval_seconds = int(time_interval.total_seconds())

        log.info(f"mechanical is ready. took {time_interval_seconds} seconds to verify")

    def __launch(self):
        """Launch Mechanical."""
        mechanical_launcher = MechanicalLauncher(
            self.batch, self.port, self.exe_path, self.additional_args, self.additional_envs
        )

        mechanical_launcher.launch()

        self.connect(self.port, self.ip_address)

        self.wait_till_mechanical_is_ready(self.wait_time)
        log.info("mechanical is ready to accept grpc calls")

    @staticmethod
    def __get_host_name():
        """Return the host name of machine.

        Returns
        -------
            host name
        """
        hostname = platform.uname().node
        return hostname

    def __get_ip(self):
        """Return the ip address of the host machine.

        Returns
        -------
            ip address used to connect to the Mechanical grpc server
        """
        if self.use_loopback_address:
            return "127.0.0.1"
        else:
            return Mechanical.__get_host_name()

    def __isMechanicalReady(self):
        """Return whether the Mechanical grpc server is ready or not.

        Returns
        -------
            Return True if Mechanical is ready otherwise False
        """
        try:
            jscript_block = "DS.Script.isDistributed()"
            self.run_jscript(jscript_block)
        except grpc.RpcError as error:
            log.debug(f"mechanical is not ready. error: {error.details()}")
            return False

        return True

    def __del__(self):
        """Close Mechanical grpc connection."""
        self.__close()

    def __enter__(self):
        """Support 'with' pattern.

        Returns
        -------
            Mechanical object
        """
        if self.channel is None:
            self.__connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support 'with' pattern.

        Parameters
        ----------
        exc_type
        exc_val
        exc_tb
        """
        self.__close()

    def __repr__(self):
        """Return the repr implementation.

        Returns
        -------
            repr string
        """
        return f"Mechanical(ip_address='{self.ip_address}'," f"port={self.port})"

    def __connect(self):
        """Connect to Mechanical grpc server."""
        address_ip = f"{self.ip_address}:{self.port}"
        log.info(f"connecting to {address_ip}")
        self.channel = grpc.insecure_channel(address_ip)
        self.stub = mechanical_pb2_grpc.MechanicalServiceStub(self.channel)
        log.info(f"connected to {address_ip}")

    def __close(self):
        """Close the grpc connection."""
        if self.channel is not None:
            self.channel.close()
            self.channel = None
            self.stub = None

    def run_jscript(self, script_block: str):
        """Run jscript block inside Mechanical.

        Parameters
        ----------
        script_block :
            script block (one or more lines) to run. I

        Returns
        -------
        str
            Return value in the string form.
        """
        self.verify_valid_connection()
        response = self.__call_run_jscript(script_block)
        return response.scriptResult

    def run_python_script(self, script_block: str):
        """Run python script block inside Mechanical.

        Parameters
        ----------
        script_block :
            script block (one or more lines) to run. I

        Returns
        -------
        str
            Return value in the string form.
        """
        self.verify_valid_connection()
        response = self.__call_run_python_script(script_block)
        return response.scriptResult

    def run_jscript_from_file(self, file_path):
        """Run the jscript file inside Mechanical.

        Parameters
        ----------
        file_path :
            This file contains jscript

        Returns
        -------
        str
            Return value in the string form.
        """
        self.verify_valid_connection()
        log.debug(f"run_jscript_from_file started")
        script_code = Mechanical.__readfile(file_path)
        log.debug(f"run_jscript_from_file done")
        return self.run_jscript(script_code)

    def run_python_script_from_file(self, file_path):
        """Run the python file inside Mechanical.

        Parameters
        ----------
        file_path :
            This file contains python script

        Returns
        -------
        str
            Return value in the string form.
        """
        self.verify_valid_connection()
        log.debug(f"run_python_script_from_file started")
        script_code = Mechanical.__readfile(file_path)
        log.debug(f"run_python_script_from_file started")
        return self.run_python_script(script_code)

    def exit(self):
        """Exit Mechanical."""
        self.verify_valid_connection()
        log.debug("In shutdown")
        request = mechanical_pb2.ShutdowntRequest()
        log.info("shutdown running")
        response = self.stub.Shutdown(request)

        if self.pypim_instance is not None:
            log.debug("pypim delete started")
            self.pypim_instance.delete()
            log.debug("pypim delete done")
            self.pypim_instance = None

        self.__init__()

        log.info("shutdown done")

    @staticmethod
    def __readfile(file_path):
        """Return the contents of the file as a string."""
        # open text file in read mode
        text_file = open(file_path, "r")
        # read whole file to a string
        data = text_file.read()
        # close file
        text_file.close()

        return data

    def __call_run_jscript(self, script_code: str):
        """Run the jscript block on the server."""
        log.debug("In __call_run_jscript")
        request = mechanical_pb2.RunScriptRequest()
        request.scriptCode = script_code
        log.debug("__call_run_jscript: running: ")
        log.debug(script_code)
        response = self.stub.RunJScript(request)
        log.debug("__call_run_jscript: got " + response.scriptResult)
        return response

    def __call_run_python_script(self, script_code: str):
        """Run the python script block on the server."""
        log.debug("In __call_run_python_script")
        request = mechanical_pb2.RunScriptRequest()
        request.scriptCode = script_code
        log.debug("__call_run_python_script: running: ")
        log.debug(script_code)
        response = self.stub.RunPythonScript(request)
        log.debug("__call_run_python_script: got " + response.scriptResult)
        return response

    def verify_valid_connection(self):
        """Verify whether we have any valid connection to Mechanical."""
        if self.stub is None:
            raise ValueError(
                "Don't have a valid connection to mechanical. Use either launch or connect first."
            )
