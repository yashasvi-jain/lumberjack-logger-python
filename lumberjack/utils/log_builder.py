import os
import traceback
from datetime import datetime
from logging import LogRecord
from typing import Optional

from lumberjack.models import Log
from lumberjack.utils import getCode


def buildLog(
    record: LogRecord, application_name: Optional[str] = None
) -> Optional[Log]:
    """
    Builds a Log object from a log record.

    Args:
        record (LogRecord): The log record used to build the Log object.
        application_name: The name of the application using the logger. Defaults to None.

    Returns:
        Log: The built Log object.
    """

    stack_trace: Optional[str] = None

    try:
        if record.exc_info is not None:
            stack_trace = traceback.format_exc()

        log = Log(
            logLevel=record.levelno,
            logLevelName=record.levelname,
            logMessage=record.getMessage(),
            loggerName=record.name,
            environment=os.environ.get("ENV"),
            applicationName=application_name,
            timestamp=datetime.now(),
            stackTrace=stack_trace,
            filename=record.filename,
            filepath=record.pathname,
            lineno=record.lineno,
            code=getCode(record.pathname),
        )
        return log
    except Exception as e:
        print(f"Failed to build log: {e}")
        return None
