import datetime
import platform
import time
import socket
from contextlib import closing
import logging.config
import grpc

import ansys.mechanical.core.mechanical_pb2 as mechanical_pb2
import ansys.mechanical.core.mechanical_pb2_grpc as mechanical_pb2_grpc

from ansys.mechanical.core.platform_helper import PlatformHelper
from ansys.mechanical.core.launcher import MechanicalLauncher


# logging_file_path = r"E:\ANSYSDev\Work\222\PyCharmProjects\src\mechanical\logging.ini"
# logging.config.fileConfig(logging_file_path, disable_existing_loggers=False)
log = logging.getLogger(__name__)


class Mechanical(object):
    def __init__(self, options_file_path="mechanical_options.ini"):
        self.options_file_path = options_file_path
        self.ip_address = None
        self.port = None
        self.channel = None
        self.stub = None
        self.batch = False
        self.wait_time = -1

    @staticmethod
    def find_free_port():
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def connect(self, port, ip_address="0.0.0.0"):
        self.ip_address = ip_address
        self.port = port
        self.__connect()
        # self.wait_till_mechanical_is_ready(wait_time)

    def launch(self, batch=False, port=-1, wait_time=-1):
        log.debug(f"launch started with batch={batch}")
        self.batch = batch
        if port == -1:
            self.port = Mechanical.find_free_port()
            log.debug(f"using the next available port: {self.port}")
        else:
            self.port = port
        self.ip_address = Mechanical.__get_host_name()
        self.wait_time = wait_time
        self.__launch()
        log.debug(f"launch done with batch={batch}")

    def wait_till_mechanical_is_ready(self, wait_time=-1):
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
                    log.debug(f"allowed wait time {wait_time} seconds. waited for {time_interval_seconds} seconds,"
                              f" before throwing error")
                    raise RuntimeError(f"Couldn't connect to mechanical. waited for {time_interval_seconds} seconds")

            time.sleep(sleep_time)

        time_2 = datetime.datetime.now()
        time_interval = time_2 - time_1
        time_interval_seconds = int(time_interval.total_seconds())

        log.info(f"mechanical is ready. took {time_interval_seconds} seconds to verify")

    def __launch(self):
        mechanical_launcher = MechanicalLauncher(self.batch, self.port, self.options_file_path)
        mechanical_launcher.launch()

        self.connect(self.port, self.ip_address)

        self.wait_till_mechanical_is_ready(self.wait_time)
        log.info("mechanical is ready to accept grpc calls")

    @staticmethod
    def __get_host_name():
        hostname = platform.uname().node
        return hostname

    def __isMechanicalReady(self):
        try:
            jscript_block = "DS.Script.isDistributed()"
            self.run_jscript(jscript_block)
        except grpc.RpcError as error:
            log.debug(f"mechanical is not ready. error: {error.details()}")
            return False

        return True

    def __del__(self):
        self.__close()

    def __enter__(self):
        if self.channel is None:
            self.__connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()

    def __repr__(self):
        return f"Mechanical(ip_address='{self.ip_address}'," \
               f"port={self.port})"

    def __connect(self):
        address_ip = f"{self.ip_address}:{self.port}"
        log.info(f"connecting to {address_ip}")
        self.channel = grpc.insecure_channel(address_ip)
        self.stub = mechanical_pb2_grpc.MechanicalServiceStub(self.channel)
        log.info(f"connected to {address_ip}")

    def __close(self):
        if self.channel is not None:
            self.channel.close()
            self.channel = None
            self.stub = None

    def run_jscript(self, script_block: str):
        response = self.__call_run_jscript(script_block)
        return response.scriptResult

    def run_python_script(self, script_block: str):
        response = self.__call_run_python_script(script_block)
        return response.scriptResult

    def run_jscript_from_file(self, file_path):
        log.debug(f"run_jscript_from_file started")
        script_code = Mechanical.__readfile(file_path)
        log.debug(f"run_jscript_from_file done")
        return self.run_jscript(script_code)

    def run_python_script_from_file(self, file_path):
        log.debug(f"run_python_script_from_file started")
        script_code = Mechanical.__readfile(file_path)
        log.debug(f"run_python_script_from_file started")
        return self.run_python_script(script_code)

    def shutdown(self):
        log.debug("In shutdown")
        request = mechanical_pb2.ShutdowntRequest()
        log.debug("shutdown running")
        response = self.stub.Shutdown(request)
        log.debug("shutdown done")


    @staticmethod
    def __readfile(file_path):
        # open text file in read mode
        text_file = open(file_path, "r")
        # read whole file to a string
        data = text_file.read()
        # close file
        text_file.close()

        return data

    def __call_run_jscript(self, script_code: str):
        log.debug("In __call_run_jscript")
        request = mechanical_pb2.RunScriptRequest()
        request.scriptCode = script_code
        log.debug("__call_run_jscript: running: ")
        log.debug(script_code)
        response = self.stub.RunJScript(request)
        log.debug("__call_run_jscript: got " + response.scriptResult)
        return response

    def __call_run_python_script(self, script_code: str):
        log.debug("In __call_run_python_script")
        request = mechanical_pb2.RunScriptRequest()
        request.scriptCode = script_code
        log.debug("__call_run_python_script: running: ")
        log.debug(script_code)
        response = self.stub.RunPythonScript(request)
        log.debug("__call_run_python_script: got " + response.scriptResult)
        return response
