from src.data_ingestion.file_reader import FileReader

# from src.data_ingestion.pdf_reader import PDFReader
from src.llm.client.ollama import OllamaLocalClient
from src.logging_config import get_logger, setup_logging


def main():

    setup_logging(testing=False)

    _log = get_logger("Main")
    _log.info("Hello World")

    # resume = PDFReader.read("resume.pdf")
    # print(resume)

    client = OllamaLocalClient()
    # client.extract_resume_keywords(resume)

    # Extract Job Description Information
    job_description = FileReader.read_txt_file("job_description.txt")

    # TODO: Store job_parsed
    # TODO: Hash job_description so it does can get job_parsed faster from the storage
    job_parsed = client.extract_job_description_keywords(job_description)

    if job_parsed:
        # Load STAR info
        star = FileReader.read_json_file("star/star_2.json")

        match_job_star = client.match_job_with_star(job_parsed, star)

        if match_job_star:
            client.rewrite_star_to_bullet_point(star, job_parsed, match_job_star)
