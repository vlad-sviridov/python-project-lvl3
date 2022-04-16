from typing import Generator
from bs4 import BeautifulSoup
import urls
import storage


def create_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, 'html.parser')


def find_resources(soup: BeautifulSoup, tag: str,
                   tag_atr: str = None) -> Generator:
    if tag_atr is not None:
        for link in soup.find_all(tag):
            yield link[tag_atr]
    else:
        for link in soup.find_all(tag):
            yield link


def replace_src_path(root: str, src_path: str):
    path_to_file, ext = storage.split_path(src_path)
    new_root = urls.url_to_name(root, '_files')
    new_file_name = urls.url_to_name(path_to_file, ext)
    return '/'.join((new_root, new_file_name))


def modify_html(html: str, url: str, tag: str = 'img', tag_atr: str = 'src'):
    soup = create_soup(html)
    root = urls.get_root_url(url)

    src_for_download = {}

    for src in find_resources(soup, tag, tag_atr):
        atr_value = src[tag_atr]
        replaced_path = replace_src_path(root, atr_value)
        src[tag_atr] = replaced_path
        src_for_download[replaced_path] = '/'.join((root, atr_value))

    return soup.prettify(), src_for_download
