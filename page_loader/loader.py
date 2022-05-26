import logging
import os

import requests
from page_loader.resources import get_and_replace
from page_loader.storage import create_dir, save_file
from page_loader.url import url_to_filename
from requests.exceptions import RequestException


def download_resoures(sources: dict, directory: str = '') -> None:
    for info in sources:
        try:
            content = requests.get(info['url']).content
        except RequestException:
            logging.warning('Failed downloaded resource %s', info['url'])
        src_dir, _ = os.path.split(info['download_path'])
        create_dir(directory + '/' + src_dir)
        save_file(content, directory + '/' + info['download_path'])


def download(url: str, output_dir: str) -> str:
    """Download a web page to a directory

    Args:
        url (str): Web page address.
        output_dir: Path to directory where the web page will be saved.

    Retruns:
        str: Path to saved the web page.
    """

    try:
        html = requests.get(url).text
    except RequestException as e:
        logging.error('Error request, Error Message: %s', str(e))

    file_name = url_to_filename(url)
    path_to_file = os.path.join(output_dir, file_name)

    modified_html, res_of_page = get_and_replace(html, url)
    download_resoures(res_of_page, output_dir)
    save_file(modified_html, path_to_file)

    return path_to_file
