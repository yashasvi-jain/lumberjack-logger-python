import logging
import unittest
from unittest.mock import patch

from LumberjackLogger.lumberjack import Lumberjack
from LumberjackLogger.models.log import Log


class LumberjackTests(unittest.TestCase):

    @patch('requests.post')
    def test_emit(self, mock_post):
        url = 'http://example.com'
        lumberjack = Lumberjack(url)
        record = logging.LogRecord('test', 1, '', 0, 'message', '', '')
        lumberjack.emit(record)

        mock_post.assert_called_once()

        (args, kwargs) = mock_post.call_args_list[0]
        self.assertEqual(args[0], url)
        self.assertIsInstance(kwargs['json'], dict)
        log = Log(**kwargs['json'])
        self.assertEqual(log.logLevel, record.levelno)
        self.assertEqual(log.logMessage, record.getMessage())

    def test_build_log(self):
        record = logging.LogRecord('test', 1, '', 0, 'message', '', '')
        log = Lumberjack.build_log(record)

        self.assertIsInstance(log, Log)
        self.assertEqual(log.logLevel, record.levelno)
        self.assertEqual(log.logMessage, record.getMessage())
        self.assertEqual(log.loggerName, record.filename)

if __name__ == '__main__':
    unittest.main()