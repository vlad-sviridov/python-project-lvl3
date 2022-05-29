import logging
import os
from typing import Union

DIR_MODE = 0o744


def save_file(content: Union[str, bytes], path: str) -> None:
    write_mode = 'wb' if isinstance(content, bytes) else 'w'
    try:
        with open(path, write_mode) as file:
            file.write(content)
        logging.debug('Created file %s', path)
    except PermissionError:
        logging.error('Failed to create file. Perimission denied')
        raise
    except OSError as e:
        logging.error('Failed to create file %s. Error: %s', path, e)
        raise


def create_dir(path: str) -> None:
    try:
        if not os.path.exists(path):
            os.mkdir(path, mode=DIR_MODE)
        logging.debug('Created directory %s', path)
    except PermissionError:
        logging.error('Failed to create direcotry. Perimission denied')
        raise
    except OSError as e:
        logging.error('Failed to create directory %s. Error: %s', path, e)
        raise
