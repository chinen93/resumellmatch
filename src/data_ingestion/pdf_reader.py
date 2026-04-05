from pathlib import Path

from pypdf import PdfReader


class PDFReader:

    @classmethod
    def read(cls, filename: str) -> str:

        filepath = Path(__file__).parent.parent.parent / "input" / filename
        print(filepath)

        ret = ""
        reader = PdfReader(filepath)

        for page in reader.pages:
            ret += page.extract_text()

        return ret
