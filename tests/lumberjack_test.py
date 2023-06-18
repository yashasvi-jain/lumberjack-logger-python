import getpass
import os
import platform
import socket
import traceback
import unittest
from logging import CRITICAL, LogRecord
from unittest.mock import patch

from LumberjackLogger.lumberjack import Lumberjack
from LumberjackLogger.models.log import Log


class LumberjackTests(unittest.TestCase):
    URL = 'http://example.com'
    APP_NAME = "lumberjack-logger-python"
    TEST_ENV = "test_env"
    RECORD = LogRecord(
        name='test',
        level=CRITICAL,
        pathname='',
        lineno=0,
        msg='message',
        args=(),
        exc_info=(ValueError, ValueError('test error'), None),
        func=None,
    )

    @patch('requests.post')
    def test_emit(self, mock_post):
        lumberjack = Lumberjack(self.URL)
        lumberjack.emit(self.RECORD)

        mock_post.assert_called_once()

        (args, kwargs) = mock_post.call_args_list[0]
        self.assertEqual(args[0], self.URL)
        self.assertIsInstance(kwargs['json'], dict)
        log = Log(**kwargs['json'])

        self.assertIsInstance(log, Log)

    def test_build_log(self):
        os.environ["ENV"] = self.TEST_ENV
        log = Lumberjack.build_log(self.RECORD)

        self.assertIsInstance(log, Log,
                              "Expected an instance of 'Log'.")
        self.assertEqual(log.logLevel, self.RECORD.levelno,
                         "The expected LogLevel is not equal to the actual LogLevel.")
        self.assertEqual(log.logLevelName, self.RECORD.levelname,
                         "The expected LogLevelName is not equal to the actual LogLevelName.")
        self.assertEqual(log.logMessage, self.RECORD.getMessage(),
                         "The expected LogMessage is not equal to the actual LogMessage.")
        self.assertEqual(log.loggerName, self.RECORD.filename,
                         "The expected LoggerName is not equal to the actual LoggerName.")
        self.assertEqual(log.language, platform.python_implementation(),
                         "The expected Language is not equal to the actual Language.")
        self.assertEqual(log.languageVersion, platform.python_version(),
                         "The expected LanguageVersion is not equal to the actual LanguageVersion.")
        self.assertEqual(log.applicationName, self.APP_NAME,
                         "The expected ApplicationName is not equal to the actual ApplicationName.")
        self.assertEqual(log.applicationSuite, None,
                         "The expected ApplicationSuite is not equal to the actual ApplicationSuite.")
        self.assertEqual(log.environment, self.TEST_ENV,
                         "The expected ApplicationName is not equal to the actual ApplicationName.")
        self.assertEqual(log.username, getpass.getuser(),
                         "The expected Username is not equal to the actual Username.")
        self.assertEqual(log.machineName, socket.gethostname(),
                         "The expected MachineName is not equal to the actual MachineName.")
        self.assertEqual(log.stackTrace, traceback.format_exc(),
                         "The expected StackTrace is not equal to the actual Stack.")


if __name__ == '__main__':
    unittest.main()
