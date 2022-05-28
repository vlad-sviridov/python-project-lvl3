import logging
import sys


def setup() -> None:
    logging.basicConfig(
        level=logging.WARNING,
        stream=sys.stderr,
        format='%(asctime)s - %(levelname)s - %(levelno)s - %(message)s'
    )
