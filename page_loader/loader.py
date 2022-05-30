import logging
import os

import requests
from page_loader.resources import get_and_replace
from page_loader.storage import create_dir, save_file
from page_loader.url import url_to_filename
from progress.bar import IncrementalBar
from requests.exceptions import RequestException


def download_resources(sources: dict, directory: str = '') -> None:
    bar = IncrementalBar(
        'Downloading the page resources:',
        max=len(sources),
        suffix='%(percent)d%%'
    )

    for info in sources:
        try:
            resp = requests.get(info['url'])
            resp.raise_for_status()
            content = resp.content
            src_dir, _ = os.path.split(info['download_path'])
            create_dir(directory + '/' + src_dir)
            save_file(content, directory + '/' + info['download_path'])
            logging.info('Downloaded resource %s', info['url'])
            bar.next()
        except (RequestException, OSError):
            logging.warning('Failed downloaded resource %s', info['url'])
    bar.finish()


def download(url: str, output_dir: str) -> str:
    """Download a web page to a directory

    Args:
        url (str): Web page address.
        output_dir: Path to directory where the web page will be saved.

    Retruns:
        str: Path to saved the web page.
    """

    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except RequestException as e:
        logging.error('Error request, Error Message: %s', str(e))
        raise

    file_name = url_to_filename(url)
    path_to_file = os.path.join(output_dir, file_name)

    logging.info('Started to downloading web page %s', url)
    modified_html, res_of_page = get_and_replace(resp.text, url)
    download_resources(res_of_page, output_dir)
    save_file(modified_html, path_to_file)

    return path_to_file
