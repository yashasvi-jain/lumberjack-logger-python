import inspect
import os
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
            calling_module = inspect.stack()[1].filename
            project_name = Lumberjack.get_project_root(calling_module)

            log = Log(
                logLevel=record.levelno,
                logLevelName=record.levelname,
                logMessage=record.getMessage(),
                loggerName=record.filename,
                environment=os.environ.get("ENV"),
                applicationName=project_name,
                timestamp=datetime.now().isoformat(),
                stackTrace=stack_trace,
            )
        except Exception as e:
            print(f"Failed to build log: {e}")
        else:
            return log

    @staticmethod
    def get_project_root(file_path):
        """
        Get the root name of the project based on the provided file path.

        Args:
            file_path (str): The path of the file.

        Returns:
            str: The root name of the project.
        """
        # Get the directory containing the file
        file_directory = os.path.dirname(file_path)

        # Traverse up the directory tree until the root of the project is reached
        while True:
            # Check if a specific file or directory exists in the current directory
            if 'setup.py' in os.listdir(file_directory) or 'requirements.txt' in os.listdir(file_directory):
                # Return the name of the current directory as the project root
                return os.path.basename(file_directory)

            # Move up to the parent directory
            file_directory = os.path.dirname(file_directory)

            # Check if the root of the file system is reached
            if file_directory == os.path.dirname(file_directory):
                break

        # Return the name of the current directory as the project root
        return os.path.basename(file_directory)
