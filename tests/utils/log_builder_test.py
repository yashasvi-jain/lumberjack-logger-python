import getpass
import logging
import os
import platform
import socket
import traceback
import unittest

from lumberjack.models import Log
from lumberjack.utils import buildLog


class LogBuilderTests(unittest.TestCase):
    """
    Test cases for the buildLog helper method.
    """

    URL = "http://example.com"
    APP_NAME = "lumberjack-logger-python"
    TEST_ENV = "test_env"
    RECORD = logging.LogRecord(
        name="test",
        level=logging.CRITICAL,
        pathname=__file__,
        lineno=0,
        msg="message",
        args=(),
        exc_info=(ValueError, ValueError("test error"), None),
        func=None,
    )

    def testBuildLog(self) -> None:
        """
        Test if the `buildLog` method correctly builds a log object from a LogRecord.
        """
        os.environ["ENV"] = self.TEST_ENV
        log: Log = buildLog(self.RECORD)

        with open(__file__, "r") as f:
            expected_code: str = f.read()

        self.assertIsInstance(log, Log, "Expected an instance of 'Log'.")
        self.assertEqual(
            log.logLevel,
            self.RECORD.levelno,
            "The expected LogLevel is not equal to the actual LogLevel.",
        )
        self.assertEqual(
            log.logLevelName,
            self.RECORD.levelname,
            "The expected LogLevelName is not equal to the actual LogLevelName.",
        )
        self.assertEqual(
            log.logMessage,
            self.RECORD.getMessage(),
            "The expected LogMessage is not equal to the actual LogMessage.",
        )
        self.assertEqual(
            log.loggerName,
            self.RECORD.name,
            "The expected LoggerName is not equal to the actual LoggerName.",
        )
        self.assertEqual(
            log.language,
            platform.python_implementation(),
            "The expected Language is not equal to the actual Language.",
        )
        self.assertEqual(
            log.languageVersion,
            platform.python_version(),
            "The expected LanguageVersion is not equal to the actual LanguageVersion.",
        )
        self.assertEqual(
            log.applicationName,
            None,
            "The expected ApplicationName is not equal to the actual ApplicationName.",
        )
        self.assertEqual(
            log.applicationSuite,
            None,
            "The expected ApplicationSuite is not equal to the actual ApplicationSuite.",
        )
        self.assertEqual(
            log.environment,
            self.TEST_ENV,
            "The expected ApplicationName is not equal to the actual ApplicationName.",
        )
        self.assertEqual(
            log.username,
            getpass.getuser(),
            "The expected Username is not equal to the actual Username.",
        )
        self.assertEqual(
            log.machineName,
            socket.gethostname(),
            "The expected MachineName is not equal to the actual MachineName.",
        )
        self.assertEqual(
            log.stackTrace,
            traceback.format_exc(),
            "The expected StackTrace is not equal to the actual Stack.",
        )
        self.assertEqual(
            log.lineno,
            self.RECORD.lineno,
            "The expected line number is not equal to the actual Stack.",
        )
        self.assertEqual(log.code, expected_code)


if __name__ == "__main__":
    unittest.main()
