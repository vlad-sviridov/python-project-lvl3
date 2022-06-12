import logging


FORMAT = '%(levelname)s: %(message)s'


def setup() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=FORMAT
    )
