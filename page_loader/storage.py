import os
from typing import Union


def save_file(content: Union[str, bytes], path: str) -> None:
    write_mode = 'wb' if isinstance(content, bytes) else 'w'
    with open(path, write_mode) as file:
        file.write(content)


def create_dir(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path, mode=744)
