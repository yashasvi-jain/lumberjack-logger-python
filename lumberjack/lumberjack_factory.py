import logging
from typing import Optional, Union

from lumberjack.lumberjack_handler import LumberjackHandler
from lumberjack.utils.console_formatter import ConsoleFormatter


class LumberjackFactory:
    """
    A factory class for creating loggers with Lumberjack handlers.
    """

    @staticmethod
    def CreateInstance(logger_name: Optional[str] = None,
                       url: Optional[str] = None,
                       application_name: Optional[str] = None,
                       log_level: Union[str, int] = logging.DEBUG,
                       emit: bool = False) -> logging.Logger:
        """
        Creates a new logger instance with optional Lumberjack handlers.

        Args:
            - `logger_name` (Optional[str], default=None): Name of the logger instance to be created.
            - `url` (Optional[str], default=None): URL for the Lumberjack handler to send log data to.
            - `application_name` (Optional[str], default=None): Name of the application using the logger.
            - `log_level` (Union[str, int], default=logging.DEBUG): Logging level for the logger.
            - `emit` (bool, default=False): Whether to add a Lumberjack handler to the logger.

        Returns:
            logging.Logger: Configured logger instance.

        Example:
            >>> logger = LumberjackFactory.CreateInstance(logger_name="MyLogger", log_level=logging.INFO, handler=True)
        """

        # Logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
        logger = LumberjackFactory._addConsoleHandler(logger, log_level)

        # Handler
        if emit:
            logger = LumberjackFactory._add_handler(
                logger,
                LumberjackHandler(url, application_name)
            )

        return logger

    @staticmethod
    def _add_handler(logger: logging.Logger, handler: logging.Handler) -> logging.Logger:
        """
        Adds a specified handler to a logger instance.

        Args:
            logger (logging.Logger): Logger instance to which the handler will be added.
            handler (logging.Handler): Logging handler to add to the logger.

        Returns:
            logging.Logger: Logger instance with the added handler.

        Example:
            >>> handler = LumberjackHandler("http://example.com", "MyApp")
            >>> LumberjackFactory.add_handler(logger, handler)
        """

        logger.addHandler(handler)
        return logger

    @staticmethod
    def _addConsoleHandler(logger: logging.Logger, level: int | str) -> logging.Logger:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(ConsoleFormatter())
        logger.addHandler(handler)
        return logger
