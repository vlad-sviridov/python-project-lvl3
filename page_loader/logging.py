import logging


def setup() -> None:
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(levelno)s - %(message)s'
    )
