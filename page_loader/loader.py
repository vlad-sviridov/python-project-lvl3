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
        src_dir, _ = os.path.split(info['download_path'])
        try:
            resp = requests.get(info['url'])
            resp.raise_for_status()
            create_dir(directory + '/' + src_dir)
            save_file(resp.content, directory + '/' + info['download_path'])
        except (RequestException, OSError) as e:
            logging.error('Failed downloaded resource %s. Message: %s',
                          info['url'], e)

        bar.next()
        logging.debug('Downloaded resource %s', info['url'])

    bar.finish()


def download(url: str, output_dir: str) -> str:
    """Download a web page to a directory

    Args:
        url (str): Web page address.
        output_dir: Path to directory where the web page will be saved.

    Retruns:
        str: Path to saved the web page.
    """

    resp = requests.get(url)
    resp.raise_for_status()

    logging.info('requested url: %s', url)
    logging.info('output path: %s', output_dir)

    file_name = url_to_filename(url, '.html')
    path_to_file = os.path.join(output_dir, file_name)

    modified_html, res_of_page = get_and_replace(resp.text, url)
    download_resources(res_of_page, output_dir)
    save_file(modified_html, path_to_file)

    return path_to_file
