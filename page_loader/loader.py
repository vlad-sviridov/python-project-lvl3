import os
import requests
from page_loader.resources import get_and_replace
from page_loader.storage import create_dir, save_file
from page_loader.url import url_to_filename


def download_resoures(sources: dict, parent_node: str = ''):
    for info in sources:
        content = requests.get(info['url']).content
        src_dir, _ = os.path.split(info['download_path'])
        create_dir(parent_node + '/' + src_dir)
        save_file(content, parent_node + '/' + info['download_path'])


def download(url: str, output_dir: str) -> str:
    """Download a web page to a directory

    Args:
        url (str): Web page address.
        output_dir: Path to directory where the web page will be saved.

    Retruns:
        str: Path to saved the web page.
    """

    page_orig_content = requests.get(url).text
    page_file_name = url_to_filename(url)
    path_to_page_file = os.path.join(output_dir, page_file_name)

    page_mod_cnt, res_of_page = get_and_replace(page_orig_content, url)
    download_resoures(res_of_page, output_dir)
    save_file(page_mod_cnt, path_to_page_file)

    return path_to_page_file
