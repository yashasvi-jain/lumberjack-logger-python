import logging
from typing import Optional

from lumberjack.lumberjack_handler import LumberjackHandler
from lumberjack.utils.console_formatter import ConsoleFormatter


class LumberjackFactory:
    """
    A factory class for creating loggers with Lumberjack handlers.
    """

    @staticmethod
    def CreateInstance(
        logger_name: Optional[str] = None,
        url: Optional[str] = None,
        application_name: Optional[str] = None,
        log_level: str | int = logging.DEBUG,
        emit: bool = False,
    ) -> logging.Logger:
        """
        Creates a new logger instance with optional Lumberjack handlers.

        Args:
            logger_name (Optional[str]): Name of the logger instance to be created. Defaults to None.
            url (Optional[str]): URL for the Lumberjack handler to send log data to. Defaults to None.
            application_name (Optional[str]): Name of the application using the logger. Defaults to None.
            log_level (str | int): Logging level for the logger. Defaults to logging.DEBUG.
            emit (bool): Whether to add a Lumberjack handler to the logger. Defaults to False.

        Returns:
            logging.Logger: Configured logger instance.

        Example:
            >>> logger = LumberjackFactory.CreateInstance(logger_name="MyLogger", log_level=logging.INFO, emit=True)
        """

        # Logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
        logger = LumberjackFactory._addConsoleHandler(logger, log_level)

        if emit:
            logger.addHandler(LumberjackHandler(url, application_name))

        return logger

    @staticmethod
    def _addConsoleHandler(logger: logging.Logger, level: int | str) -> logging.Logger:
        """
        Adds a console handler to a logger instance.

        Args:
            logger (logging.Logger): Logger instance to which the console handler will be added.
            level (Union[int, str]): Logging level for the console handler.

        Returns:
            logging.Logger: Logger instance with the added console handler.
        """
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(ConsoleFormatter())
        logger.addHandler(handler)
        return logger
