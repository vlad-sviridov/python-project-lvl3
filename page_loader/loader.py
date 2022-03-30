import os
import re
from urllib import parse

import requests
from requests.api import request


def get_response(url: str) -> requests.Response:
    return requests.get(url)


def create_file_name(url: str, ext='.html') -> str:
    parsed_url = parse.urlparse(url)
    raw_file_name = parsed_url.netloc + parsed_url.path

    return re.sub(r'[^0-9a-zA-Z]', '-', raw_file_name) + ext


def save_web_page(content: str, path: str) -> None:
    with open(path, 'w') as file:
        file.write(content)


def download(url: str, output_dir: str) -> str:
    """Download a web page to a directory

    Args:
        url (str): Web page address.
        output_dir: Path to directory where the web page will be saved.

    Retruns:
        str: Path to saved the web page.
    """

    page_content = get_response(url).text
    file_name = create_file_name(url)
    path_to_file = os.path.join(output_dir, file_name)
    save_web_page(page_content, path_to_file)

    return path_to_file
