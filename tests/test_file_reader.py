import os
import tempfile
import unittest

from src.data_ingestion.file_reader import FileReader
from tests.conf_log_test import BaseTestCase


class TestFileReader(BaseTestCase):
    """Unit tests for FileReader class."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.reader = FileReader()

    def tearDown(self):
        """Clean up after each test method."""
        pass

    def test_read_txt_file_valid(self):
        """Test reading a valid .txt file."""
        content = "This is a test file content."
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, dir="input"
        ) as f:
            f.write(content)
            temp_file = f.name

        try:
            filename = os.path.basename(temp_file)
            result = FileReader.read_txt_file(filename)
            self.assertEqual(result, content)
        finally:
            os.unlink(temp_file)

    def test_read_txt_file_not_found(self):
        """Test reading a non-existent file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            FileReader.read_txt_file("nonexistent.txt")

    def test_read_txt_file_encoding(self):
        """Test reading a file with UTF-8 encoding."""
        content = "Test content with special chars: àáâãäå"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, dir="input", encoding="utf-8"
        ) as f:
            f.write(content)
            temp_file = f.name

        try:
            filename = os.path.basename(temp_file)
            result = FileReader.read_txt_file(filename)
            self.assertEqual(result, content)
        finally:
            os.unlink(temp_file)


if __name__ == "__main__":
    unittest.main()
