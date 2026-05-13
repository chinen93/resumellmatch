"""Job description import module.

Handles importing and processing of job descriptions from text files with
detection and reuse of previously cached results based on content hash.
"""

from typing import Optional

from config.logging import get_logger
from src.core.processor.job_processor import JobDescriptionProcessor
from src.data_ingestion.file_reader import FileReader
from src.utils.hash import compute_hash


class JobDescriptionImporter:
    """Imports job descriptions from text files and processes them.

    Reads job descriptions from files, computes content hash for deduplication,
    checks cache, and processes new descriptions through the job processor.

    Attributes:
        processor: JobDescriptionProcessor instance for handling processing.
        _log: Logger instance.
    """

    processor: JobDescriptionProcessor

    def __init__(self, processor: JobDescriptionProcessor):
        self.processor = processor
        self._log = get_logger("JobDescriptionImporter")

    def run(self, filename: str) -> Optional[str]:
        """Import and process a job description from a text file.

        Reads the job description file, computes a hash of its content,
        checks if this job description has been previously processed,
        and either returns the cached result or processes it new.

        Args:
            filename: Name of the text file containing the job description.

        Returns:
            The processed job description or cached result. None if an error occurs.
        """

        job_desc = FileReader.read_txt_file(filename)
        input_hash = compute_hash(job_desc)

        existing = self.processor.exist_job_description(input_hash)
        if existing is not None:
            self._log.info("Using cached parsed job description from DB")
            return existing

        return self.processor.new_item(job_desc, input_hash)
