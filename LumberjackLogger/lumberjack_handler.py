import json
import os
import traceback
from datetime import datetime
from logging import LogRecord, StreamHandler
from typing import Optional

import requests
from requests import HTTPError, Response

from LumberjackLogger.models.log import Log


class LumberjackHandler(StreamHandler):
    """
    A custom log handler class that formats log messages and sends them to a logging endpoint.
    """

    application_name: str = None
    """
    The name of the application.
    """

    def __init__(self, url: str, application_name: str = None) -> None:
        """
        Initializes the Lumberjack log handler.

        Args:
            url (str): The URL of the logging endpoint.
            application_name (str, optional): The name of the application. Defaults to None.

        """
        super().__init__()
        self.__url: str = url
        LumberjackHandler.application_name: str = application_name

    def emit(self, record: LogRecord):
        """
        Emits the log record to the Lumberjack logging endpoint.

        Args:
            record (LogRecord): The log record to be emitted.
        """

        # Emit the record to console or wherever StreamHandler is set to output
        super().emit(record)

        log: Log = self.build_log(record)

        payload = json.loads(log.json())

        try:
            headers: dict = {'Content-Type': 'application/json'}
            request: Response = requests.post(self.__url, json=payload, headers=headers)
            request.raise_for_status()
        except HTTPError as e:
            print(e)

    @staticmethod
    def build_log(record: LogRecord) -> Log:
        """
        Builds a Log object from a log record.

        Args:
            record (LogRecord): The log record used to build the Log object.

        Returns:
            Log: The built Log object.

        """

        stack_trace: Optional[str] = None

        try:
            if record.exc_info is not None:
                stack_trace = traceback.format_exc()

            log = Log(
                logLevel=record.levelno,
                logLevelName=record.levelname,
                logMessage=record.getMessage(),
                loggerName=record.filename,
                environment=os.environ.get("ENV"),
                applicationName=LumberjackHandler.application_name,
                timestamp=datetime.now(),
                stackTrace=stack_trace,
                filename=record.filename,
                pathname=record.pathname
            )
        except Exception as e:
            print(f"Failed to build log: {e}")
        else:
            return log
