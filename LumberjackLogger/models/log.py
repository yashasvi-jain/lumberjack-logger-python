import getpass
import platform
import socket

from pydantic import BaseModel, Field


class Log(BaseModel):
    """
    A Pydantic model class representing a Lumberjack log.

    Attributes:
    -----------
    logLevel : int
        The log level of the log.
    logLevelName : str
        The log level name of the log.
    logMessage : str
        The message of the log.
    loggerName : str
        The logger name of the log.
    language : str
        The name of the language.
    languageVersion : str
        The version of the language.
    applicationName : str, optional
        The name of the application.
    applicationSuite : str, optional
        The name of the application suite.
    environment : str, optional
        The name of the environment.
    username : str
        The username of the user who emitted the log.
    machineName : str
        The machine name where the log was emitted.
    timestamp : str
        The timestamp when the log was emitted.
    stackTrace : str, optional
        The stack trace of the log.
    """

    logLevel: int = Field(..., description="The log level of the log.")
    logLevelName: str = Field(..., description="The log level name of the log.")
    logMessage: str = Field(..., description="The message of the log.")
    loggerName: str = Field(..., description=" The logger name of the log.")
    language: str = Field(None, description="The name of the language.")
    languageVersion: str = Field(None, description="The version of the language.")
    applicationName: str = Field(None, description="The name of the application.")
    applicationSuite: str = Field(None, description="The name of the application suite.")
    environment: str = Field(None, description="The name of the environment.")
    username: str = Field(None, description="The username of the user who emitted the log.")
    machineName: str = Field(None, description="The machine name where the log was emitted.")
    timestamp: str = Field(..., description="The timestamp when the log was emitted.")
    stackTrace: str = Field(None, description="The stack trace of the log.")

    class Config:
        validate_assignment = True

    def __init__(self, **data):
        super().__init__(**data)
        self.language = platform.python_implementation()
        self.languageVersion = platform.python_version()
        self.username = getpass.getuser()
        self.machineName = socket.gethostname()

    def __str__(self):
        """
        Returns a formatted string representation of the Log object.
        """
        log_info = []
        for key, value in self.__dict__.items():
            log_info.append(f"{key}: {value}")
        return "\n".join(log_info)