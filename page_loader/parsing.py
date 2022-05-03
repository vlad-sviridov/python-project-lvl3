import os
from typing import Generator, Tuple, Union
from urllib.parse import urljoin

from bs4 import BeautifulSoup, element
from page_loader import urls


def create_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, 'html.parser')


def find_resources(soup: BeautifulSoup, tags: list) -> Generator:
    for link in soup.find_all(tags):
        yield link


def modify_src_url(root: str, src_url: str) -> str:
    full_src_url = urljoin(root, src_url)
    return urls.url_to_filename(full_src_url)


def parse_and_modify_html(html: str, url: str) -> Tuple:
    soup = create_soup(html)
    root_url = urls.get_root_url(url)
    root_dir_name = urls.url_to_filename(root_url, '_files')

    resources_info = []

    for tag in find_resources(soup, ['img']):
        src_url = _get_src_url(tag)
        src_filename = modify_src_url(root_url, src_url)
        download_path = os.path.join(root_dir_name, src_filename)

        _replace_src_url_attr(tag, download_path)

        if urls.is_local_url(src_url, root_url):
            full_src_url = urljoin(root_url, src_url)
        else:
            full_src_url = src_url

        resources_info.append({
            'download_path': download_path,
            'url': full_src_url
        })

    return soup.prettify(), resources_info


def _get_src_url_attr(tag: element.Tag) -> Union[str, None]:
    if tag.name == 'img':
        return 'src'


def _get_src_url(tag: element.Tag) -> Union[str, None]:
    attr = _get_src_url_attr(tag)
    if attr:
        return tag.get(attr)


def _replace_src_url_attr(tag: element.Tag, url: str) -> None:
    attr = _get_src_url_attr(tag)
    if attr:
        tag[attr] = url
