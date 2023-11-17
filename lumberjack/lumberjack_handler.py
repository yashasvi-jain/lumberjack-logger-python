import json
from logging import LogRecord, StreamHandler
from typing import Dict, Optional

import requests
from requests import HTTPError, Response

from lumberjack.utils import buildLog


class LumberjackHandler(StreamHandler):
    """
    A custom log handler class that formats log messages and sends them to a logging endpoint.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        application_name: Optional[str] = None,
    ) -> None:
        """
        Initializes the Lumberjack log handler.

        Args:
            url (str): The URL of the logging endpoint.
            application_name (str, optional): The name of the application. Defaults to None.
        """

        super().__init__()
        self.__url: Optional[str] = url
        self.__application_name = application_name

    def emit(self, record: LogRecord) -> None:
        """
        Emits the log record to the Lumberjack logging endpoint.

        Args:
            record (LogRecord): The log record to be emitted.
        """

        log = buildLog(record, self.__application_name)

        if log and self.__url:
            payload = json.loads(log.model_dump_json())
            try:
                headers: Dict = {"Content-Type": "application/json"}
                request: Response = requests.post(
                    self.__url, json=payload, headers=headers
                )
                request.raise_for_status()
            except HTTPError as e:
                print(e)
