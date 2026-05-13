"""Resume import module.

Handles importing and processing of resume documents from PDF files with
detection and reuse of previously cached results based on content hash.
"""

from typing import Optional

from config.logging import get_logger
from src.core.processor import ResumeProcessor
from src.data_ingestion import PDFReader
from src.utils.hash import compute_hash


class ResumeImporter:
    """Imports resumes from PDF files and processes them.

    Extracts text from PDF resume files, computes content hash for deduplication,
    checks cache, and processes new resumes through the resume processor.

    Attributes:
        processor: ResumeProcessor instance for handling processing.
        _log: Logger instance.
    """

    processor: ResumeProcessor

    def __init__(self, processor: ResumeProcessor):
        self.processor = processor
        self._log = get_logger("ResumeImporter")

    def run(self, filename: str) -> Optional[str]:
        """Import and process a resume from a PDF file.

        Reads the resume from a PDF file, extracts text, computes a hash
        of the content, checks if this resume has been previously processed,
        and either returns the cached result or processes it anew.

        Args:
            filename: Name of the PDF file containing the resume.

        Returns:
            The processed resume or cached result. None if an error occurs.
        """

        resume = PDFReader.read(filename)

        input_hash = compute_hash(resume)

        existing = self.processor.exist_resume(input_hash)
        if existing is not None:
            self._log.info("Using cached resume from DB")
            return existing

        return self.processor.new_item(resume, input_hash)
