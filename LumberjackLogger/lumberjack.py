import getpass
import os
import socket
import traceback
from datetime import datetime
from logging import LogRecord, StreamHandler

import requests
from requests import HTTPError

from .models.log import Log


class Lumberjack(StreamHandler):
    """A custom log handler class that formats log messages and sends them to a logging endpoint."""

    def __init__(self, url: str) -> None:
        """
        Initializes the Lumberjack log handler.

        Parameters:
        -----------
        url : str
            The URL of the logging endpoint.
        """

        self.__url = url
        super().__init__()

    def emit(self, record):
        """
        Emits the log record to the Lumberjack logging-endpoint.

        Parameters:
        -----------
        record : logging.LogRecord
            The log record to be emitted.
        """

        log = self.build_log(record)

        try:
            request = requests.post(self.__url, json=log.dict())
            request.raise_for_status()
        except HTTPError as e:
            print(f"HTTP error occured: {e}")

    @staticmethod
    def build_log(record: LogRecord) -> Log:
        """
        Builds a Log object from a log record.

        Parameters:
        -----------
        record : LogRecord
            The log record used to build the Log object.

        Returns:
        -----------
        Log
            The built Log object.
        """

        stack_trace = None

        try:
            if record.exc_info is not None:
                stack_trace = traceback.format_exc()

            # Get the applicaiton name
            root_folder = os.path.dirname(os.path.abspath(__file__))
            project_name = os.path.basename(root_folder)

            log = Log(
                logLevel=record.levelno,
                logLevelName=record.levelno,
                logMessage=record.getMessage(),
                loggerName=record.filename,
                environment=os.environ.get("ENV"),
                applicationName=project_name,
                username=getpass.getuser(),
                machineName=socket.gethostname(),
                timestamp=datetime.now().isoformat(),
                stackTrace=stack_trace,
            )
        except Exception as e:
            print(f"Failed to build log: {e}")
        else:
            return log
