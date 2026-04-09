import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.data_ingestion.pdf_reader import PDFReader
from tests.conf_log_test import BaseTestCase


class TestPDFReader(BaseTestCase):
    """Unit tests for PDFReader class."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        """Set up test fixtures before each test method."""
        pass

    def tearDown(self):
        """Clean up after each test method."""
        pass

    @patch("src.data_ingestion.pdf_reader.PdfReader")
    def test_read_pdf_valid(self, mock_pdf_reader):
        """Test reading a valid PDF file."""
        # Mock the PDF reader and pages
        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = "Page 1 content."
        mock_page2 = MagicMock()
        mock_page2.extract_text.return_value = "Page 2 content."
        mock_pdf_reader.return_value.pages = [mock_page1, mock_page2]

        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False, dir="input") as f:
            temp_file = f.name

        try:
            filename = Path(temp_file).name
            result = PDFReader.read(filename)
            expected = "Page 1 content.Page 2 content."
            self.assertEqual(result, expected)
        finally:
            Path(temp_file).unlink()

    @patch("src.data_ingestion.pdf_reader.PdfReader")
    def test_read_pdf_single_page(self, mock_pdf_reader):
        """Test reading a PDF with a single page."""
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Single page content."
        mock_pdf_reader.return_value.pages = [mock_page]

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False, dir="input") as f:
            temp_file = f.name

        try:
            filename = Path(temp_file).name
            result = PDFReader.read(filename)
            self.assertEqual(result, "Single page content.")
        finally:
            Path(temp_file).unlink()

    @patch("src.data_ingestion.pdf_reader.PdfReader")
    def test_read_pdf_empty(self, mock_pdf_reader):
        """Test reading an empty PDF."""
        mock_pdf_reader.return_value.pages = []

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False, dir="input") as f:
            temp_file = f.name

        try:
            filename = Path(temp_file).name
            result = PDFReader.read(filename)
            self.assertEqual(result, "")
        finally:
            Path(temp_file).unlink()


if __name__ == "__main__":
    unittest.main()
