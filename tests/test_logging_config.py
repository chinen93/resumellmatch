import unittest
from pathlib import Path
from unittest.mock import patch

from src.logging_config import get_config_path, get_logger
from tests.conf_log_test import BaseTestCase


class TestLoggingConfig(BaseTestCase):
    """Unit tests for logging configuration functions."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        """Set up test fixtures before each test method."""
        pass

    def tearDown(self):
        """Clean up after each test method."""
        pass

    def test_get_config_path_production(self):
        """Test getting production config path."""
        path = get_config_path(testing=False)
        expected = str(Path(__file__).parent.parent / "config" / "logging.conf")
        self.assertEqual(path, expected)

    def test_get_config_path_testing(self):
        """Test getting test config path."""
        path = get_config_path(testing=True)
        expected = str(Path(__file__).parent.parent / "config" / "logging_test.conf")
        self.assertEqual(path, expected)

    def test_get_config_path_file_not_found(self):
        """Test that FileNotFoundError is raised when config file doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False):
            with self.assertRaises(FileNotFoundError):
                get_config_path(testing=False)

    # def test_ensure_logs_directory(self):
    #     """Test that logs directory is created if it doesn't exist."""
    #     with tempfile.TemporaryDirectory() as temp_dir:
    #         with patch("src.logging_config.Path") as mock_path:
    #             mock_path.return_value.parent.parent = Path(temp_dir)
    #             mock_path.return_value.mkdir = MagicMock()
    #             ensure_logs_directory()
    #             mock_path.return_value.mkdir.assert_called_once_with(exist_ok=True)

    def test_get_logger(self):
        """Test getting a logger instance."""
        logger = get_logger("test_logger")
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "test_logger")


if __name__ == "__main__":
    unittest.main()
