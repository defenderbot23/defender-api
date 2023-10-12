import tempfile


def dump_to_file(filename, content):

    # dump to file
    temp_dir = tempfile.TemporaryDirectory()
    file_path = f'{temp_dir.name}/{filename}'

    with open(file_path, 'w') as f:
        f.write(content)

    return file_path
