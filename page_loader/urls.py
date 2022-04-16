import re
import requests
from urllib import parse


def get_response(url: str) -> requests.Response:
    return requests.get(url)


def url_to_name(url: str, ext: str = '.html') -> str:
    parsed_url = parse.urlparse(url)
    raw = parsed_url.netloc + parsed_url.path
    return re.sub(r'[^0-9a-zA-Z]', '-', raw) + ext


def get_root_url(url: str) -> str:
    parsed_url = parse.urlparse(url)
    return parsed_url.scheme + '://' + parsed_url.netloc
