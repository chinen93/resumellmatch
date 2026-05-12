import unittest
from pathlib import Path
from unittest.mock import patch

from config.logging import get_logger
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

    def test_get_logger(self):
        """Test getting a logger instance."""
        logger = get_logger("test_logger")
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "test_logger")


if __name__ == "__main__":
    unittest.main()
