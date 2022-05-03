import os
import tempfile

import requests_mock
from page_loader.loader import download
from tests.utils import load_fixture


def test_download():
    path_to_orig_page = './tests/fixtures/page.html'
    page_url = 'https://ru.hexlet.io/courses'

    src_png = load_fixture('./tests/fixtures/page_sources/python.png', True)

    tmpdir = tempfile.TemporaryDirectory()
    tmpdirname = tmpdir.name

    page_file_path = os.path.join(tmpdirname, 'ru-hexlet-io-courses.html')

    mocks = [
        (
            page_url,
            load_fixture(path_to_orig_page)
        ),
        (
            'https://ru.hexlet.io/assets/professions/python.png',
            src_png
        )
    ]

    with requests_mock.Mocker() as mocker:
        for url, content in mocks:
            if isinstance(content, bytes):
                mocker.get(url, content=content)
            else:
                mocker.get(url, text=content)

        assert download(page_url, tmpdirname) == page_file_path

    resources_dir = 'ru-hexlet-io_files/'
    resources = [
        (
            'ru-hexlet-io-courses.html',
            load_fixture('./tests/fixtures/page_after.html')
        ),
        (
            resources_dir + 'ru-hexlet-io-assets-professions-python.png',
            src_png
        )
    ]

    for file_name, content in resources:
        path_to_file_name = os.path.join(tmpdirname, file_name)

        read_mode = 'rb' if isinstance(content, bytes) else 'r'

        with open(path_to_file_name, read_mode) as file:
            assert file.read() == content

    tmpdir.cleanup()
