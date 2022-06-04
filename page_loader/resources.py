import os
from typing import Tuple, Union
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from page_loader.url import url_to_dirname, url_to_filename

TAG_ATTRIBUTES = {
    'img': 'src',
    'script': 'src',
    'link': 'href',
}
FILE_EXT = '.html'
DIRECTORY_EXT = '_files'


def is_local_url(url: str, root_url_hostname: Union[str, None]):
    url_hostname = urlparse(url).hostname
    return url_hostname is None or url_hostname == root_url_hostname


def get_and_replace(html: str, url: str) -> Tuple:
    soup = BeautifulSoup(html, 'html.parser')
    parsed_url = urlparse(url)
    url_scheme, url_hostname = parsed_url.scheme, parsed_url.hostname
    root_dir_name = url_to_dirname(url, DIRECTORY_EXT)
    resources_info = []

    for tag in soup(TAG_ATTRIBUTES.keys()):
        attribute = TAG_ATTRIBUTES[tag.name]
        src_url = tag.get(attribute)

        if src_url is None:
            continue

        if not is_local_url(src_url, url_hostname):
            continue

        full_src_url = urljoin(url_scheme + '://' + url_hostname, src_url)
        src_filename = url_to_filename(full_src_url, FILE_EXT)
        download_path = os.path.join(root_dir_name, src_filename)

        tag[attribute] = download_path

        resources_info.append({
            'download_path': download_path,
            'url': full_src_url
        })

    return soup.prettify(), resources_info
