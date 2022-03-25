import os
import tempfile

import requests_mock
from page_loader.loader import download


def test_download():
    path = './tests/fixtures/page.html'
    page_url = 'https://ethereum.org/en'

    with open(path, 'r') as file:
        content = file.read()

    tmpdir = tempfile.TemporaryDirectory()
    tmpdirname = tmpdir.name

    page_file_path = os.path.join(tmpdir.name, 'ethereum-org-en.html')

    with requests_mock.Mocker() as mock:
        mock.get(page_url, text=content)
        assert download(page_url, tmpdirname) == page_file_path

    with open(page_file_path) as file:
        assert file.read() == content

    tmpdir.cleanup()
