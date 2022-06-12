import os
from typing import Tuple, Optional

from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from page_loader.url import url_to_dirname, url_to_filename


TAG_ATTRIBUTES = {
    'img': 'src',
    'script': 'src',
    'link': 'href',
}


def is_local_url(url: str, base_hostname: Optional[str] = None) -> bool:
    hostname = urlparse(url).hostname
    return hostname is None or hostname == base_hostname


def get_and_replace(html: str, url: str) -> Tuple:
    soup = BeautifulSoup(html, 'html.parser')
    parsed_url = urlparse(url)
    base_hostname = parsed_url.hostname
    root_dir_name = url_to_dirname(url)
    resources_info = []

    for tag in soup(TAG_ATTRIBUTES.keys()):
        tag_attribute = TAG_ATTRIBUTES[tag.name]
        resource = tag.get(tag_attribute)

        if resource is None:
            continue

        if not is_local_url(resource, base_hostname):
            continue

        full_resource_url = urljoin(url, resource)
        filename_of_resource = url_to_filename(full_resource_url)
        download_path = os.path.join(root_dir_name, filename_of_resource)

        tag[tag_attribute] = download_path

        resources_info.append({
            'download_path': download_path,
            'url': full_resource_url
        })

    return soup.prettify(), resources_info
