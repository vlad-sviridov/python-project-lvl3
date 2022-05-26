import pytest
from page_loader.storage import save_file, create_dir
import tempfile
import os


tmpdir = tempfile.TemporaryDirectory()
tmpdirname = tmpdir.name

@pytest.mark.parametrize(
    'content,path',
    [
        ('<html></html>', tmpdirname +'/test.html'),
        (b'0b001100', tmpdirname + '/test.png')
    ]
)
def test_save_file(content, path):
    save_file(content, path)

    read_mode = 'rb' if isinstance(content, bytes) else 'r'
    with open(path, read_mode) as file:
        assert file.read() == content


def test_save_file_path_doesnt_exist():
    with pytest.raises(OSError):
        save_file('some text', 'path/does/not/exist.txt')


def test_create_dir():
    dir_path = tmpdirname + '/dir'
    create_dir(dir_path)

    assert os.path.isdir(dir_path)


def test_create_dir_path_doesnt_exist():
    with pytest.raises(OSError):
        create_dir('path/does/not/exist.txt')
