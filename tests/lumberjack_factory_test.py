import logging
import unittest
from unittest.mock import MagicMock, patch

from lumberjack.lumberjack_factory import LumberjackFactory
from lumberjack.lumberjack_handler import LumberjackHandler


class LumberjackFactoryTests(unittest.TestCase):
    """
    Test cases for the LumberjackFactory class.
    """

    def setUp(self) -> None:
        """
        Set up test environment.
        """

        self.logger_name = 'test logger'
        self.app_name = 'test app'
        self.url = 'test url'
        self.log_level = logging.INFO

        self.mock_getLogger = MagicMock()
        self.mock_logger = MagicMock(spec=logging.Logger)

    def tearDown(self) -> None:
        """
        Clean up after tests, setting shared attributes to None.
        """

        LumberjackHandler.application_name = None

    def test_create_instance(self) -> None:
        """
        Test the `CreateInstance` method for creating a logger instance.

        Given a logger name and expected log level, it should correctly configure the logger.
        """

        # ACT
        with patch('logging.getLogger', self.mock_getLogger):
            self.mock_getLogger.return_value = self.mock_logger

            # Create an instance of the LumberjackFactory
            logger = LumberjackFactory.CreateInstance(
                logger_name=self.logger_name,
                log_level=self.log_level,
                application_name='test app'
            )

        # ASSERT
        self.mock_getLogger.assert_called_with(self.logger_name)
        logger.setLevel.assert_called_with(self.log_level)

    def test_default_level_value(self) -> None:
        """
        Test the default log level setting in the `CreateInstance` method.

        The log level should default to DEBUG if not explicitly set.
        """

        with patch('logging.getLogger', return_value=MagicMock(spec=logging.Logger)):
            logger = LumberjackFactory.CreateInstance()

        logger.setLevel.assert_called_with(logging.DEBUG)

    def test_level_as_a_string(self) -> None:
        """
        Test that log level can be set as a string.
        """
        with patch('logging.getLogger', return_value=MagicMock(spec=logging.Logger)):
            logger = LumberjackFactory.CreateInstance(log_level='INFO')
        logger.setLevel.assert_called_with('INFO')

    def test_default_logger_name(self) -> None:
        """
        Test the default logger name in the `CreateInstance` method.

        The logger name should default to `None` if not explicitly set.
        """

        with patch('logging.getLogger', self.mock_getLogger):
            logger = LumberjackFactory.CreateInstance()

        self.mock_getLogger.assert_called_with(None)

    def test_handler(self) -> None:
        """
        Test if the logger is correctly associated with a LumberjackHandler instance.
        """

        # ACT
        logger = LumberjackFactory.CreateInstance(
            logger_name=self.logger_name,
            url=self.url,
            application_name=self.app_name,
            log_level=self.log_level,
            emit=True
        )
        handler: LumberjackHandler = logger.handlers.pop()

        # ASSERT
        self.assertEqual(handler.application_name, self.app_name)
        self.assertEqual(getattr(handler, '_LumberjackHandler__url'), self.url)

    @patch('lumberjack.lumberjack_handler.LumberjackHandler')
    def test_add_handler(self, mock_handler: MagicMock) -> None:
        """
        Test if a handler can be added to an existing logger.
        """

        logger = LumberjackFactory.CreateInstance(
            logger_name=self.logger_name,
            url=self.url,
            application_name=self.app_name,
            log_level=self.log_level,
            emit=False
        )

        self.assertFalse(logger.hasHandlers())

        LumberjackFactory._add_handler(logger, mock_handler)

        self.assertTrue(logger.hasHandlers())
        self.assertEqual(logger.handlers.pop(), mock_handler)
        self.assertFalse(logger.hasHandlers())


if __name__ == '__main__':
    unittest.main()
