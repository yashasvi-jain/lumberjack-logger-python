import logging

from .lumberjack import Lumberjack


class LumberjackFactory:

    @staticmethod
    def CreateInstance(logger_name: str, url: str) -> logging.Logger:
        """
        Creates a new logger with the specified name and returns it.

        Args:
            logger_name (str): The name of the logger being returned

        Returns:
            Logger: Returns a Logger with the Lumberjack handler
        """

        # Logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # Handler
        handler = Lumberjack(url)

        # Formatting
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger
