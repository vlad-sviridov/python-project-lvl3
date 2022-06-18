import os

import tempfile
import pytest

from page_loader.storage import create_dir, save_file, check_directory


tmpdir = tempfile.TemporaryDirectory()
tmpdirname = tmpdir.name


@pytest.mark.parametrize(
    'content,path',
    [
        ('<html></html>', tmpdirname + '/test.html'),
        (b'0b001100', tmpdirname + '/test.png')
    ]
)
def test_save_file(content, path):
    save_file(content, path)

    read_mode = 'rb' if isinstance(content, bytes) else 'r'
    with open(path, read_mode) as file:
        assert file.read() == content


def test_save_file_path_doesnt_exist():
    with pytest.raises(FileNotFoundError):
        save_file('some text', 'path/does/not/exist.txt')


def test_create_dir(tmpdir):
    dir_path = tmpdir + '/dir'
    create_dir(dir_path)
    assert os.path.isdir(dir_path)


def test_create_dir_path_doesnt_exist():
    with pytest.raises(FileNotFoundError):
        create_dir('path/does/not/exists.txt')


def test_check_directory(tmpdir):
    path_not_exist = 'path/does/not/exist'
    not_adirectory = tmpdir + '/not_adirectroy.txt'
    path_without_permission = tmpdir + '/without_permission'

    os.mknod(not_adirectory)
    os.mkdir(path_without_permission, mode=0o444)

    with pytest.raises(FileNotFoundError):
        check_directory(path_not_exist)

    with pytest.raises(NotADirectoryError):
        check_directory(not_adirectory)

    with pytest.raises(PermissionError):
        check_directory(path_without_permission)
