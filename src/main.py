from src.core.importer import (
    JobDescriptionImporter,
    StarEntryImporter,
    StarMetadataImporter,
)
from src.core.processor import (
    JobDescriptionProcessor,
    StarEntryProcessor,
    StarMetadataProcessor,
)
from src.data_ingestion import CSVLoader, FileReader
from src.llm.client import OllamaLocalClient
from src.logging_config import get_logger


class Handler:
    def __init__(self):
        self._log = get_logger("Handler")
        self.llm_client = OllamaLocalClient()


def handle_job():

    handler = Handler()
    handler._log.info("Handle Job Description")

    job_processor = JobDescriptionProcessor(handler.llm_client, isTest=False)
    job_importer = JobDescriptionImporter(job_processor)

    job_parsed = job_importer.run("job_description.txt")

    if job_parsed:
        # Load STAR info
        star = FileReader.read_json_file("star/star_2.json")

        match_job_star = handler.llm_client.match_job_with_star(job_parsed, star)

        if match_job_star:
            handler.llm_client.rewrite_star_to_bullet_point(
                star, job_parsed, match_job_star
            )


def handle_star():
    handler = Handler()
    handler._log.info("Handle STAR responses")

    csvLoader = CSVLoader()

    star_metadata_processor = StarMetadataProcessor(isTest=False)
    star_metadata_importer = StarMetadataImporter(
        loader=csvLoader, processor=star_metadata_processor
    )
    star_metadata_importer.run(filename="star/star_metadata.csv")

    star_entry_processor = StarEntryProcessor(isTest=False)
    star_entry_importer = StarEntryImporter(
        loader=csvLoader, processor=star_entry_processor
    )
    star_entry_importer.run(filename="star/star_entries.csv")

    handler._log.info("Finished handling STAR responses")


def handle_resume():
    handler = Handler()
    handler._log.info("Handle Resume")

    # resume = PDFReader.read("resume.pdf")
    # print(resume)

    # client = OllamaLocalClient()
    # client.extract_resume_keywords(resume)
