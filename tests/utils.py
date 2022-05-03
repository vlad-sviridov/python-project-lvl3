def load_fixture(path_to_file, binary=False):
    read_mode = 'rb' if binary else 'r'
    with open(path_to_file, read_mode) as file:
        return file.read()
