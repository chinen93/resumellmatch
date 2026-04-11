import json

from src.data_ingestion.file_reader import FileReader
from src.llm.client.ollama import OllamaLocalClient
from src.logging_config import get_logger, setup_logging
from src.storage.repositories.job_repo import (
    JobDescriptionParsedRepo,
    JobDescriptionRepo,
)
from src.utils.hash import compute_hash


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

    parsed_repo = JobDescriptionParsedRepo(isTest=False)
    job_repo = JobDescriptionRepo(isTest=False)

    input_hash = compute_hash(job_description)

    existing = parsed_repo.get_by_input_hash(input_hash)
    if existing:
        _log.info("Using cached parsed job description from DB")
        job_parsed = str(existing.full_response)
    else:
        job_parsed = client.extract_job_description_keywords(job_description)

        if job_parsed:
            # persist job description and parsed response
            try:
                job_id = job_repo.create(url="", title="", raw_text=job_description)

                # attempt to extract fields from the LLM response JSON
                parsed_obj = json.loads(job_parsed)
                summary = parsed_obj.get("summary", "")
                required_skills = json.dumps(parsed_obj.get("technical_skills", []))
                prefered_skills = json.dumps(parsed_obj.get("soft_skills", []))
                keywords = json.dumps(parsed_obj.get("keywords", []))

                parsed_repo.create(
                    job_description_id=job_id,
                    summary=summary,
                    required_skills=required_skills,
                    prefered_skills=prefered_skills,
                    keywords=keywords,
                    input_hash=input_hash,
                    full_response=job_parsed,
                )
            except Exception:
                _log.exception("Failed to persist parsed job description")

    if job_parsed:
        # Load STAR info
        star = FileReader.read_json_file("star/star_2.json")

        match_job_star = client.match_job_with_star(job_parsed, star)

        if match_job_star:
            client.rewrite_star_to_bullet_point(star, job_parsed, match_job_star)
