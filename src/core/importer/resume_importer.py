from typing import Optional

from src.core.processor import ResumeProcessor
from src.data_ingestion import PDFReader
from config.logging import get_logger
from src.utils.hash import compute_hash


class ResumeImporter:

    processor: ResumeProcessor

    def __init__(self, processor: ResumeProcessor):
        self.processor = processor
        self._log = get_logger("ResumeImporter")

    def run(self, filename: str) -> Optional[str]:

        resume = PDFReader.read(filename)

        input_hash = compute_hash(resume)

        existing = self.processor.exist_resume(input_hash)
        if existing is not None:
            self._log.info("Using cached resume from DB")
            return existing

        return self.processor.new_item(resume, input_hash)
