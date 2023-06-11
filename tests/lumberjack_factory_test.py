import logging
import unittest
from unittest.mock import Mock

from context import LumberjackFactory, Lumberjack


class LumberjackFactoryTests(unittest.TestCase):

    def test_create_instance(self):
        # Arrange
        logger_name = 'test_logger'
        url = 'http://example.com'
        expected_log_level = logging.DEBUG

        # Create a mock Lumberjack handler instance
        lumberjack_mock = Mock(spec=Lumberjack)

        # Create a mock logger
        logger_mock = Mock(spec=logging.Logger)
        logger_mock.name = logger_name
        logger_mock.level = expected_log_level
        logger_mock.handlers = lumberjack_mock

        # Create a mock getLogger function to return the mock logger
        logging_mock = Mock(spec=logging)
        logging_mock.getLogger.return_value = logger_mock

        # Create an instance of the LumberjackFactory
        logger = LumberjackFactory.CreateInstance(logger_name, url)

        # Assert
        self.assertEqual(logger.name, logger_name)
        self.assertEqual(logger.level, expected_log_level)

if __name__ == '__main__':
    unittest.main()