import os
import re

from urllib.parse import urlparse

PATTERN = re.compile(r'[^0-9a-zA-Z_]')
FILE_EXT = '.html'
DIRECTORY_EXT = '_files'


def format_name(name: str) -> str:
    return re.sub(PATTERN, '-', name)


def url_to_filename(url: str) -> str:
    parsed_url = urlparse(url)
    path, ext = os.path.splitext(parsed_url.path)
    if not ext:
        ext = FILE_EXT
    return format_name(parsed_url.netloc + path.rstrip('/')) + ext


def url_to_dirname(url: str) -> str:
    parsed_url = urlparse(url)
    path = parsed_url.path.rstrip('/')
    return format_name(parsed_url.netloc + path) + DIRECTORY_EXT
