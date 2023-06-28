import logging
import os
from typing import Optional

from LumberjackLogger.lumberjack_handler import LumberjackHandler


class LumberjackFactory:
    """
    A factory class for creating loggers with Lumberjack handlers.
    """

    @staticmethod
    def CreateInstance(logger_name: Optional[str], url: Optional[str], application_name: Optional[str], log_level: str | int = logging.DEBUG) -> logging.Logger:
        """
        Creates a new logger with the specified name and returns it.

        Args:
            logger_name (str, optional): The name of the logger being returned.
            log_level (str | int): The log level of the logger. It can be specified using either a string name or an integer value.
            url (str, optional): The URL to be used by the Lumberjack handler.
            application_name (str, optional): The name of the application. Defaults to None.

        Returns:
            logging.Logger: The logger with the Lumberjack handler.

        """

        # Logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)

        # Handler
        handler = LumberjackHandler(url, application_name)

        # Add filter to handler to modify pathname
        handler.addFilter(PathnameFilter())

        # Formatting
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger


class PathnameFilter(logging.Filter):
    """
    This filter will modify the pathname of a record.
    """

    def filter(self, record):
        record.pathname = os.path.abspath(record.pathname)
        return True
