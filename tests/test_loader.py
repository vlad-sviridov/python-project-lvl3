import os
import tempfile

import requests_mock
from page_loader.loader import download


def load_fixture(path_to_file, binary=False):
    read_mode = 'rb' if binary else 'r'
    with open(path_to_file, read_mode) as file:
        return file.read()


def test_download():
    path_to_orig_page = './tests/fixtures/page.html'
    page_url = 'https://ru.hexlet.io/courses'

    python_png = load_fixture('./tests/fixtures/page_sources/python.png', True)
    application_css = load_fixture(
        './tests/fixtures/page_sources/application.css')
    runtime_js = load_fixture('./tests/fixtures/page_sources/runtime.js')

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
    with requests_mock.Mocker() as mocker:
        for url, content in mocks:
            if isinstance(content, bytes):
                mocker.get(url, content=content)
            else:
                mocker.get(url, text=content)

        assert download(page_url, tmpdirname) == page_file_path

# Compare html of web page
    path_to_page = os.path.join(tmpdirname, 'ru-hexlet-io-courses.html')
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
        path_to_file_name = os.path.join(tmpdirname, file_name)

        read_mode = 'rb' if isinstance(content, bytes) else 'r'

        with open(path_to_file_name, read_mode) as file:
            assert file.read() == content

    tmpdir.cleanup()
