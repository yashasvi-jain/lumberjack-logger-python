import logging

from colorama import Fore, Style, init

# Initialize Colorama
init()


class ConsoleFormatter(logging.Formatter):
    """
    Custom logging formatter to colorize the log level part of log messages based on severity level.

    This formatter extends the standard logging.Formatter class and applies
    different colors to the log level part of messages depending on their severity level.
    It supports DEBUG, INFO, WARNING, ERROR, and CRITICAL levels. Other levels
    will use the default formatting style.
    """

    # Calculate max length once
    MAX_LEVEL_LENGTH = max(len(logging.getLevelName(lvl)) for lvl in [
                           logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL])

    # Base format with time only (hours, minutes, seconds)
    BASE_FORMAT = "%(asctime)s [%(levelname)s]: %(message)s"

    def __init__(self) -> None:
        super().__init__(fmt=self.BASE_FORMAT, datefmt="%H:%M:%S")

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified record as text.

        Overrides the format method of logging.Formatter to apply color based
        on the logging level of the record and dynamically adjust padding after the level name.
        This method is called automatically by the logging system.
        """

        # Adjust padding dynamically
        padding = self.MAX_LEVEL_LENGTH - len(record.levelname)

        # Create a dynamic format for levelname
        levelname_format = f"[%(levelname)s]{' ' * padding}"

        # Apply color only to levelname
        match record.levelno:
            case logging.DEBUG:
                colored_levelname = Fore.CYAN + levelname_format + Style.RESET_ALL
            case logging.INFO:
                colored_levelname = Fore.GREEN + levelname_format + Style.RESET_ALL
            case logging.WARNING:
                colored_levelname = Fore.YELLOW + levelname_format + Style.RESET_ALL
            case logging.ERROR:
                colored_levelname = Fore.RED + levelname_format + Style.RESET_ALL
            case logging.CRITICAL:
                colored_levelname = Fore.RED + Style.BRIGHT + levelname_format + Style.RESET_ALL
            case _:
                colored_levelname = levelname_format  # Default format

        # Set the dynamic format
        self._style._fmt = f"%(asctime)s {colored_levelname}: %(message)s"

        # Format the record
        formatted_record = super().format(record)
        return formatted_record
