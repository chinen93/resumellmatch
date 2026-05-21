"""Resume-LLM Match CLI entry point.

This module provides the command-line interface for the resume-LLM matching system,
allowing users to initiate various workflows including job description processing,
resume analysis, and STAR entry importation.
"""

import click

from config.logging import setup_logging
from src.main import handle_job, handle_resume, handle_star


@click.command(no_args_is_help=True)
@click.option(
    "--job",
    is_flag=True,
    help="Flag to create resume for job",
)
@click.option(
    "--star",
    is_flag=True,
    help="Flag to import STAR interview reponses",
)
@click.option(
    "--resume",
    is_flag=True,
    help="Flag to import resume",
)
@click.option(
    "--no-llm-cache",
    is_flag=True,
    default=False,
    help="Disable LLM cache so all requests are sent to the LLM client",
)
def main(job: bool, star: bool, resume: bool, no_llm_cache: bool) -> None:
    """CLI entrypoint: parse flags and dispatch to the correct function."""

    use_llm_cache = not no_llm_cache

    if job:
        handle_job(use_llm_cache=use_llm_cache)
        return

    if star:
        handle_star(use_llm_cache=use_llm_cache)
        return

    if resume:
        handle_resume(use_llm_cache=use_llm_cache)
        return


if __name__ == "__main__":
    setup_logging(testing=False)
    main()
