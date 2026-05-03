import unittest
from unittest.mock import patch

from src.storage.connection import DatabaseConnection
from tests.conf_log_test import BaseTestCase


class TestDatabaseConnection(BaseTestCase):
    """Unit tests for DatabaseConnection class."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Reset singleton instance before each test
        DatabaseConnection._instance = None
        DatabaseConnection.engine = None

    def tearDown(self):
        """Clean up after each test method."""
        DatabaseConnection._instance = None
        DatabaseConnection.engine = None

    @patch("src.storage.connection.create_engine")
    def test_singleton_production(self, mock_create_engine):
        """Test that DatabaseConnection is a singleton in production mode."""
        conn1 = DatabaseConnection(isTest=False)
        conn2 = DatabaseConnection(isTest=False)

        self.assertIs(conn1, conn2)
        mock_create_engine.assert_called_once_with(
            "sqlite:///./example/output/storage.db", echo=False
        )

    @patch("src.storage.connection.create_engine")
    def test_singleton_test(self, mock_create_engine):
        """Test that DatabaseConnection creates new instance for test mode."""
        conn1 = DatabaseConnection(isTest=True)
        conn2 = DatabaseConnection(isTest=True)

        # In test mode, each call should create a new instance
        self.assertIsNot(conn1, conn2)
        self.assertEqual(mock_create_engine.call_count, 2)
        mock_create_engine.assert_called_with(
            "sqlite:///./example/output/test_storage.db", echo=False
        )

    @patch("src.storage.connection.create_engine")
    def test_get_session(self, mock_create_engine):
        """Test getting a session from the connection."""
        conn = DatabaseConnection(isTest=True)
        session = conn.get_session()

        self.assertIsNotNone(session)
        # Session should be from sqlalchemy.orm.Session
        from sqlalchemy.orm import Session

        self.assertIsInstance(session, Session)


if __name__ == "__main__":
    unittest.main()
