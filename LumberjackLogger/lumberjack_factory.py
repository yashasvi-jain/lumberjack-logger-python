import logging
import os

from .lumberjack_handler import LumberjackHandler


class LumberjackFactory:
    """
    A factory class for creating loggers with Lumberjack handlers.
    """

    @staticmethod
    def CreateInstance(logger_name: str, url: str, application_name: str = None) -> logging.Logger:
        """
        Creates a new logger with the specified name and returns it.

        Args:
            logger_name (str): The name of the logger being returned.
            url (str): The URL to be used by the Lumberjack handler.

        Returns:
            logging.Logger: The logger with the Lumberjack handler.

        """

        # Logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # Handler
        handler = LumberjackHandler(url, application_name)

        # Add filter to handler to modify pathname
        handler.addFilter(PathnameFilter())

        # Formatting
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
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