import os
from typing import Union

import logging


DIRECTORY_PERMISSIONS = 0o744


def check_directory(directory_path: str) -> None:
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f'Not search a directory {directory_path}')
    if not os.access(directory_path, os.W_OK):
        raise PermissionError(f'No permission to write {directory_path}')
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f'{directory_path} is not a directory')


def save_file(content: Union[str, bytes], path: str) -> None:
    write_mode = 'wb' if isinstance(content, bytes) else 'w'
    with open(path, write_mode) as file:
        file.write(content)
    logging.debug('Created file %s', path)


def create_dir(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path, mode=DIRECTORY_PERMISSIONS)
    logging.debug('Created directory %s', path)
