import unittest
from logging import CRITICAL, LogRecord
from unittest.mock import MagicMock, patch

from lumberjack import LumberjackHandler
from lumberjack.models.log import Log


class LumberjackHandlerTests(unittest.TestCase):
    """
    Test cases for the LumberjackHandler class.
    """

    URL = "http://example.com"
    APP_NAME = "lumberjack-logger-python"
    TEST_ENV = "test_env"
    RECORD = LogRecord(
        name="test",
        level=CRITICAL,
        pathname=__file__,
        lineno=0,
        msg="message",
        args=(),
        exc_info=(ValueError, ValueError("test error"), None),
        func=None,
    )

    def setUp(self) -> None:
        self.mock_log = MagicMock(spec=Log)
        self.mock_log.dict.return_value = MagicMock()

        LumberjackHandler.application_name = None

    @patch("requests.post")
    def test_emit(self, mock_post: MagicMock) -> None:
        """
        Sets up mock objects used in the tests.
        """
        with patch("lumberjack.models.log.Log", self.mock_log):
            lumberjack = LumberjackHandler(self.URL)
            lumberjack.emit(self.RECORD)

        mock_post.assert_called_once()

        (args, kwargs) = mock_post.call_args_list[0]
        self.assertEqual(args[0], self.URL)
        self.assertIsInstance(kwargs["json"], dict)
        log = Log(**kwargs["json"])

        self.assertIsInstance(log, Log)


if __name__ == "__main__":
    unittest.main()
