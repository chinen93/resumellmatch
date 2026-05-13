"""PDF text extraction utilities.

Provides functionality to extract text content from PDF files.
"""

from pypdf import PdfReader

from config.logging import get_logger
from src.data_ingestion.utils import get_filepath


class PDFReader:
    """Static utility class for extracting text from PDF files."""

    @classmethod
    def read(cls, filename: str) -> str:
        """Extract all text from a PDF file.

        Reads a PDF file and extracts text from all pages.

        Args:
            filename: Name of the PDF file to read.

        Returns:
            The concatenated text content from all pages of the PDF.

        Raises:
            FileNotFoundError: If the PDF file doesn't exist.
            Exception: If there's an error reading or parsing the PDF.
        """

        filepath = get_filepath(filename)

        _log = get_logger("PDFReader")
        _log.debug(filepath)

        ret = ""
        reader = PdfReader(filepath)

        for page in reader.pages:
            ret += page.extract_text()

        return ret
