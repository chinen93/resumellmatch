from src.logging_config import get_logger, setup_logging

_log = get_logger("Main")


def main():

    setup_logging(testing=False)
    _log.info("Hello World")
