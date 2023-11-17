import getpass
import platform
import socket
from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, model_validator


class Log(BaseModel):
    """
    A Lumberjack log.
    """

    logLevel: int
    """
    The numerical representation of the log level.
    """

    logLevelName: str
    """
    The name of the log level.
    """

    logMessage: str
    """
    The message of the log entry.
    """

    loggerName: Optional[str] = None
    """
    The name of the logger.
    """

    language: Optional[str] = None
    """
    The name of the language.
    """

    languageVersion: Optional[str] = None
    """
    The version of the language.
    """

    applicationName: Optional[str] = None
    """
    The name of the application associated with the log entry.
    """

    applicationId: Optional[str] = None
    """
    The ID of the application associated with the log entry.
    """

    applicationSuite: Optional[str] = None
    """
    The name of the application suite associated with the log entry.
    """

    applicationSuiteId: Optional[str] = None
    """
    The ID of the application suite associated with the log entry.
    """

    environment: Optional[str] = None
    """
    The name of the environment in which the log entry was generated.
    """

    username: str
    """
    The username of the user who emitted the log entry.
    """

    machineName: str
    """
    The name of the machine where the log entry was emitted.
    """

    timestamp: datetime
    """
    The timestamp when the log entry was emitted.
    """

    stackTrace: Optional[str] = None
    """
    The stack trace associated with the log entry, if available.
    """

    filename: Optional[str] = None
    """
    The filename where the logger was invoked.
    """

    filepath: Optional[str] = None
    """
    The absolute file path for the file the logger was invoked.
    """

    lineno: Optional[int] = None
    """
    The line number in the file where the logger was invoked.
    """

    code: Optional[str] = None
    """
    The source code where the logger was invoked.
    """

    @model_validator(mode="before")
    @classmethod
    def set_defaults(cls, values: dict) -> Dict:
        """
        Sets default values for certain fields if they are not provided.

        Args:
            values (dict): The values of the fields.

        Returns:
            dict: The modified values dictionary with default values set.

        """
        values.setdefault("language", platform.python_implementation())
        values.setdefault("languageVersion", platform.python_version())
        values.setdefault("username", getpass.getuser())
        values.setdefault("machineName", socket.gethostname())
        return values

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the Log object.
        """
        log_info = []
        for key, value in self.__dict__.items():
            log_info.append(f"{key}: {value}")
        return "\n".join(log_info)
