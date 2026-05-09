from typing import Optional

from src.core.processor.job_processor import JobDescriptionProcessor
from src.data_ingestion.file_reader import FileReader
from src.logging_config import get_logger
from src.utils.hash import compute_hash


class JobDescriptionImporter:

    processor: JobDescriptionProcessor

    def __init__(self, processor: JobDescriptionProcessor):
        self.processor = processor
        self._log = get_logger("JobDescriptionImporter")

    def run(self, filename: str) -> Optional[str]:

        job_desc = FileReader.read_txt_file(filename)
        input_hash = compute_hash(job_desc)

        existing = self.processor.exist_job_description(input_hash)
        if existing is not None:
            self._log.info("Using cached parsed job description from DB")
            return existing

        return self.processor.new_item(job_desc, input_hash)
