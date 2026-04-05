from src.data_ingestion.pdf_reader import PDFReader
from src.llm.client.ollama import OllamaLocalClient
from src.logging_config import get_logger, setup_logging


def main():

    setup_logging(testing=False)
    _log = get_logger("Main")
    _log.info("Hello World")

    resume = PDFReader.read("resume.pdf")
    print(resume)

    client = OllamaLocalClient()
    client.extract_keywords(resume)
