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
def main(job: bool, star: bool, resume: bool) -> None:
    """CLI entrypoint: parse flags and dispatch to the correct function."""

    if job:
        handle_job()
        return

    if star:
        handle_star()
        return

    if resume:
        handle_resume()
        return


if __name__ == "__main__":
    setup_logging(testing=False)
    main()
