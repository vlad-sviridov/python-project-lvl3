import logging
import os
import re
from urllib.parse import urlparse


def format_name(name: str) -> str:
    return re.sub(r'[^0-9a-zA-Z_]', '-', name)


def url_to_filename(url: str, default_ext: str = '.html') -> str:
    logging.debug('Get parameters url=%s, ext=%s', url, default_ext)
    parsed_url = urlparse(url)
    path, ext = os.path.splitext(parsed_url.path)
    if not ext:
        ext = default_ext
    return format_name(parsed_url.netloc + path.rstrip('/')) + ext


def url_to_dirname(url: str, postfix: str = '_files') -> str:
    logging.debug('Get parameters url=%s, postfix=%s', url, postfix)
    parsed_url = urlparse(url)
    path = parsed_url.path.rstrip('/')
    return format_name(parsed_url.netloc + path) + postfix


def get_root_url(url: str) -> str:
    parsed_url = urlparse(url)
    return '://'.join((parsed_url.scheme, parsed_url.hostname))
