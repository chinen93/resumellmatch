from pathlib import Path

from pypdf import PdfReader

from src.logging_config import get_logger


class PDFReader:

    @classmethod
    def read(cls, filename: str) -> str:

        _log = get_logger("PDFReader")

        filepath = Path(__file__).parent.parent.parent / "input" / filename

        _log.debug(filepath)

        ret = ""
        reader = PdfReader(filepath)

        for page in reader.pages:
            ret += page.extract_text()

        return ret
