import os

import pytest
import requests
from page_loader.loader import download
from requests.exceptions import RequestException


def load_fixture(path_to_file, binary=False):
    read_mode = 'rb' if binary else 'r'
    with open(path_to_file, read_mode) as file:
        return file.read()


def test_download(requests_mock, tmpdir):
    path_to_orig_page = './tests/fixtures/page.html'
    page_url = 'https://ru.hexlet.io/courses'

    python_png = load_fixture('./tests/fixtures/page_sources/python.png', True)
    application_css = load_fixture(
        './tests/fixtures/page_sources/application.css')
    runtime_js = load_fixture('./tests/fixtures/page_sources/runtime.js')


    page_file_path = tmpdir / 'ru-hexlet-io-courses.html'

    mocks = [
        (
            page_url,
            load_fixture(path_to_orig_page)
        ),
        (
            'https://ru.hexlet.io/assets/professions/python.png',
            python_png
        ),
        (
            'https://ru.hexlet.io/assets/application.css',
            application_css
        ),
        (
            'https://ru.hexlet.io/packs/js/runtime.js',
            runtime_js
        )
    ]

# Check a path of web page
    for url, content in mocks:
        if isinstance(content, bytes):
            requests_mock.get(url, content=content)
        else:
            requests_mock.get(url, text=content)

    assert download(page_url, str(tmpdir)) == page_file_path

# Compare html of web page
    path_to_page = tmpdir / 'ru-hexlet-io-courses.html'
    page_html = load_fixture('./tests/fixtures/page_after.html')
    with open(path_to_page, 'r') as file:
        assert file.read() == page_html

    # Check a path of web page resources
    resources_dir = 'ru-hexlet-io-courses_files/'
    resources = [
        (
            resources_dir + 'ru-hexlet-io-courses.html',
            load_fixture('./tests/fixtures/page.html')
        ),
        (
            resources_dir + 'ru-hexlet-io-assets-professions-python.png',
            python_png
        ),
        (
            resources_dir + 'ru-hexlet-io-assets-application.css',
            application_css
        ),
        (
            resources_dir + 'ru-hexlet-io-packs-js-runtime.js',
            runtime_js
        )
    ]

    for file_name, content in resources:
        path_to_file_name = tmpdir / file_name

        read_mode = 'rb' if isinstance(content, bytes) else 'r'

        with open(path_to_file_name, read_mode) as file:
            assert file.read() == content


def test_download_unavailable_page(requests_mock, tmpdir):
    url = 'https://test.com'
    requests_mock.get(url, status_code=404)

    with pytest.raises(RequestException):
        download(url, str(tmpdir))


def test_download_some_unavailable_page(requests_mock, tmpdir):
    url = 'https://test.com'
    html = '''
        <html>
            <body>
                <img src="unavailable.png">
                <img src="available.png">
            <body>
        </html>
    '''

    requests_mock.get(url, text=html)
    requests_mock.get(url + '/unavailable.png', status_code=404)
    requests_mock.get(url + '/available.png', content=b'0b001100')

    download(url, str(tmpdir))
    resources_dir = tmpdir / 'test-com_files'

    assert os.path.isfile(tmpdir / 'test-com.html')
    assert os.path.isfile(resources_dir / 'test-com-available.png')
    assert not os.path.isfile(resources_dir / 'test-com-unavailable.png')


def test_download_without_resources(requests_mock, tmpdir):
    url = 'https://test.com'
    html = '<html><p>Hello World!</p></html>'

    requests_mock.get(url, text=html)
    download(url, tmpdir)

    assert not os.path.isdir(tmpdir / 'test-com_files')
    assert os.path.isfile(tmpdir / 'test-com.html')
