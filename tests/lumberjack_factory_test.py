import logging
import unittest
from unittest.mock import MagicMock, Mock, patch

from lumberjack.lumberjack_factory import LumberjackFactory
from lumberjack.lumberjack_handler import LumberjackHandler


class LumberjackFactoryTests(unittest.TestCase):
    """
    Test cases for the LumberjackFactory class.
    """

    def test_create_instance(self) -> None:
        """
        Test the `CreateInstance` method for creating a logger instance.

        Given a logger name and expected log level, it should correctly configure the logger.
        """

        # Arrange
        logger_name = 'test_logger'
        expected_log_level = logging.INFO

        # Create a mock Lumberjack handler instance
        lumberjack_mock = Mock(spec=LumberjackHandler)

        # Create a mock logger
        mock_logger = MagicMock()
        mock_logger.name = logger_name
        mock_logger.level = expected_log_level

        with patch('logging.getLogger', return_value=mock_logger):
            # Create an instance of the LumberjackFactory
            logger = LumberjackFactory.CreateInstance(
                logger_name=logger_name,
                log_level=logging.INFO,
                application_name='test app'
            )

        # Assert
        self.assertEqual(logger.name, logger_name)
        self.assertEqual(logger.level, expected_log_level)

    def test_default_level_value(self) -> None:
        """
        Test the default log level setting in the `CreateInstance` method.

        The log level should default to DEBUG if not explicitly set.
        """

        with patch('logging.getLogger', return_value=Mock()):
            logger = LumberjackFactory.CreateInstance()

        logger.setLevel.assert_called_with(logging.DEBUG)


if __name__ == '__main__':
    unittest.main()
