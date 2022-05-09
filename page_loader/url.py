import os
import re
from urllib.parse import urlparse


def url_to_name(url: str) -> str:
    parsed_url = urlparse(url)
    raw = parsed_url.netloc + parsed_url.path
    return re.sub(r'[^0-9a-zA-Z_]', '-', raw)


def url_to_filename(url: str, default_ext: str = '.html') -> str:
    _, ext = os.path.splitext(url)
    if not ext:
        url_without_ext = url
        ext = default_ext
    else:
        url_without_ext = url[:-len(ext)]
    return url_to_name(url_without_ext) + ext


def url_to_dirname(url: str, postfix: str = '_files') -> str:
    url = url.rstrip('/')
    return url_to_name(url) + postfix


def get_root_url(url: str) -> str:
    parsed_url = urlparse(url)
    return '://'.join((parsed_url.scheme, parsed_url.hostname))
