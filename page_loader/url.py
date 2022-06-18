import os
import re

from urllib.parse import urlparse

ALLOWED_CHARS = re.compile(r'[^0-9a-zA-Z_]')
EXTENTION_FOR_FILENAME = '.html'
EXTENTION_FOR_DIRECTORY = '_files'


def format_name(name: str) -> str:
    return re.sub(ALLOWED_CHARS, '-', name)


def url_to_filename(url: str) -> str:
    parsed_url = urlparse(url)
    path, ext = os.path.splitext(parsed_url.path)
    if not ext:
        ext = EXTENTION_FOR_FILENAME
    return format_name(parsed_url.netloc + path.rstrip('/')) + ext


def url_to_dirname(url: str) -> str:
    parsed_url = urlparse(url)
    path = parsed_url.path.rstrip('/')
    return format_name(parsed_url.netloc + path) + EXTENTION_FOR_DIRECTORY
