import os

import requests
import logging
from progress.bar import IncrementalBar

from page_loader import resources, storage
from page_loader.url import url_to_filename


def get_response(url: str) -> requests.Response:
    resp = requests.get(url)
    resp.raise_for_status()
    return resp


def download_resources(resources: dict, directory: str) -> None:
    bar = IncrementalBar(
        'Downloading the page resources:',
        max=len(resources),
        suffix='%(percent)d%%')

    for resource_info in resources:
        resource_dir, _ = os.path.split(resource_info['download_path'])
        storage.create_dir(os.path.join(directory, resource_dir))
        try:
            response = get_response(resource_info['url'])
        except requests.exceptions.HTTPError as e:
            logging.warning('Failed downloaded resource %s. Message: %s',
                            resource_info['url'], e)
        else:
            storage.save_file(
                response.content,
                os.path.join(directory, resource_info['download_path'])
            )
        bar.next()
        logging.debug('Downloaded resource %s', resource_info['url'])

    bar.finish()


def download(url: str, output_dir: str) -> str:
    """Download a web page to a directory

    Args:
        url (str): Web page address.
        output_dir (str): Path to directory where the web page will be saved.

    Retruns:
        str: Path to saved the web page.
    """

    storage.check_directory(output_dir)
    response = get_response(url)
    page_file_name = url_to_filename(url)
    page_path_to_file = os.path.join(output_dir, page_file_name)
    modified_html, resources_of_page = resources.get_and_replace(
        response.text,
        url
    )
    storage.save_file(modified_html, page_path_to_file)
    download_resources(resources_of_page, output_dir)

    return page_path_to_file
