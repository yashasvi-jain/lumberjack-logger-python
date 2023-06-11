import getpass
import logging
import os
import socket
import traceback
from datetime import datetime

import requests
from .models.log import Log


class Lumberjack(logging.StreamHandler):
    """
    A custom log handler class that formats log messages and sends them to a logging endpoint.

    Attributes:
    -----------
    url : str
        The URL of the logging endpoint.
    """

    def __init__(self, url: str) -> None:
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

        requests.post('http://localhost:8080/logs', json=log.dict())

    @staticmethod
    def build_log(record: logging.LogRecord) -> Log:

        stack_trace = None

        if record.exc_info is not None:
            stack_trace = traceback.format_exc()

        return Log(
            logLevel = record.levelno,
            logLevelName = record.levelno,
            logMessage = record.getMessage(),
            loggerName = record.filename,
            environment = os.environ.get('ENV'),
            username = getpass.getuser(),
            machineName = socket.gethostname(),
            timestamp = datetime.now().isoformat(),
            stackTrace = stack_trace
        )