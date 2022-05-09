import os
from typing import Generator, Tuple
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from page_loader.url import get_root_url, url_to_filename, url_to_dirname


def find_resources(
        soup: BeautifulSoup, tags: list) -> Generator[str, None, None]:
    for link in soup.find_all(tags):
        yield link


def is_local_url(url: str, root_url: str):
    url_hostname = urlparse(url).hostname
    root_url_hostname = urlparse(root_url).hostname
    return url_hostname is None or url_hostname == root_url_hostname


def get_and_replace(html: str, url: str) -> Tuple:
    soup = BeautifulSoup(html, 'html.parser')
    root_url = get_root_url(url)
    root_dir_name = url_to_dirname(url)
    resources_info = []

    attributes = {
        'img': 'src',
        'script': 'src',
        'link': 'href',
    }

    for tag in find_resources(soup, ['img', 'link', 'script']):
        attribute = attributes[tag.name]
        src_url = tag.get(attribute)

        if not is_local_url(src_url, root_url):
            continue

        full_src_url = urljoin(root_url, src_url)
        src_filename = url_to_filename(full_src_url)
        download_path = os.path.join(root_dir_name, src_filename)

        tag[attribute] = download_path

        resources_info.append({
            'download_path': download_path,
            'url': full_src_url
        })

    return soup.prettify(), resources_info
