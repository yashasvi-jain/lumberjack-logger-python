import getpass
import platform
import socket
from datetime import datetime

from pydantic import BaseModel, Field, root_validator


class Log(BaseModel):
    """
    A Lumberjack log.
    """

    logLevel: int = Field(..., description='The numerical representation of the log level.')
    """
    The numerical representation of the log level.
    """

    logLevelName: str = Field(..., description='The name of the log level.')
    """
    The name of the log level.
    """

    logMessage: str = Field(..., description='The message of the log entry.')
    """
    The message of the log entry.
    """

    loggerName: str = Field(..., description='The name of the logger.')
    """
    The name of the logger.
    """

    language: str = Field(None, description='The name of the language.')
    """
    The name of the language.
    """

    languageVersion: str = Field(None, description='The version of the language.')
    """
    The version of the language.
    """

    applicationName: str = Field(None, description='The name of the application.')
    """
    The name of the application associated with the log entry.
    """

    applicationId: str = Field(None, description='The ID of the application.')
    """
    The ID of the application associated with the log entry.
    """

    applicationSuite: str = Field(None, description='The name of the application suite.')
    """
    The name of the application suite associated with the log entry.
    """

    applicationSuiteId: str = Field(None, description='The ID of the application suite.')
    """
    The ID of the application suite associated with the log entry.
    """

    environment: str = Field(None, description='The name of the environment.')
    """
    The name of the environment in which the log entry was generated.
    """

    username: str = Field(..., description='The username of the user who emitted the log.')
    """
    The username of the user who emitted the log entry.
    """

    machineName: str = Field(..., description='The machine name where the log was emitted.')
    """
    The name of the machine where the log entry was emitted.
    """

    timestamp: datetime = Field(..., description='The timestamp when the log was emitted.')
    """
    The timestamp when the log entry was emitted.
    """

    stackTrace: str = Field(None, description='The stack trace of the log.')
    """
    The stack trace associated with the log entry, if available.
    """

    filename: str = Field(None, description='The filename where the logger was invoked.')
    """
    The filename where the logger was invoked.
    """

    pathname: str = Field(None, description='The absolute file path for the file the logger was invoked.')
    """
    The absolute file path for the file the logger was invoked.
    """


    @root_validator(pre=True)
    def set_defaults(cls, values: dict):
        """
        Sets default values for certain fields if they are not provided.

        Args:
            values (dict): The values of the fields.

        Returns:
            dict: The modified values dictionary with default values set.

        """
        values.setdefault('language', platform.python_implementation())
        values.setdefault('languageVersion', platform.python_version())
        values.setdefault('username', getpass.getuser())
        values.setdefault('machineName', socket.gethostname())
        return values

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the Log object.
        """
        log_info = []
        for key, value in self.__dict__.items():
            log_info.append(f"{key}: {value}")
        return "\n".join(log_info)