import os
import re
from urllib import parse

import requests


def get_response(url: str, **kwargs) -> requests.Response:
    return requests.get(url, kwargs)


def url_to_name(url: str) -> str:
    parsed_url = parse.urlparse(url)
    raw = parsed_url.netloc + parsed_url.path
    return re.sub(r'[^0-9a-zA-Z]', '-', raw)


def url_to_filename(url: str, default_ext: str = '.html') -> str:
    url = url.rstrip('/')
    _, ext = os.path.splitext(parse.urlparse(url).path)
    if not ext:
        url_without_ext = url
        ext = default_ext
    else:
        url_without_ext = url[0:-len(ext)]
    return url_to_name(url_without_ext) + ext


def get_root_url(url: str) -> str:
    parsed_url = parse.urlparse(url)
    return '://'.join((parsed_url.scheme, parsed_url.hostname))


def is_local_url(url: str, root_url: str):
    url_hostname = parse.urlparse(url).hostname
    root_url_hostname = parse.urlparse(root_url).hostname
    return url_hostname is None or url_hostname == root_url_hostname
