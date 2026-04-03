from src.llm.client.ollama import OllamaClient
from src.logging_config import get_logger, setup_logging


def main():

    setup_logging(testing=False)
    _log = get_logger("Main")
    _log.info("Hello World")

    client = OllamaClient()
    client.hello_world()
