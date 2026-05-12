from pypdf import PdfReader

from src.data_ingestion.utils import get_filepath
from config.logging import get_logger


class PDFReader:

    @classmethod
    def read(cls, filename: str) -> str:

        filepath = get_filepath(filename)

        _log = get_logger("PDFReader")
        _log.debug(filepath)

        ret = ""
        reader = PdfReader(filepath)

        for page in reader.pages:
            ret += page.extract_text()

        return ret
