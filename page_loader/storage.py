import logging
import os
from typing import Union

DIR_MODE = 0o744


def save_file(content: Union[str, bytes], path: str) -> None:
    write_mode = 'wb' if isinstance(content, bytes) else 'w'
    with open(path, write_mode) as file:
        file.write(content)
    logging.debug('Created file %s', path)


def create_dir(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path, mode=DIR_MODE)
    logging.debug('Created directory %s', path)
