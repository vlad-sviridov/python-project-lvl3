import pytest

from page_loader.url import url_to_dirname, url_to_filename


@pytest.mark.parametrize(
    'url,expected',
    [
        ('http://test.com', 'test-com.html'),
        ('https://test.com', 'test-com.html'),
        ('https://test.com/', 'test-com.html'),
        ('https://test.com/path', 'test-com-path.html'),
        ('https://test.com/path/', 'test-com-path.html'),
        ('https://test.com/file.png', 'test-com-file.png'),
        ('https://test.com/path/file_js.js', 'test-com-path-file_js.js')
    ]
)
def test_url_to_filename(url, expected):
    assert url_to_filename(url) == expected


@pytest.mark.parametrize(
    'url,expected',
    [
        ('http://test.com', 'test-com_files'),
        ('https://test.com/', 'test-com_files'),
        ('https://test.com/path', 'test-com-path_files')
    ]
)
def test_url_to_dirname(url, expected):
    assert url_to_dirname(url) == expected
