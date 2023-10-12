import tempfile


def dump_to_tmp(filename, content):

    # prepare name
    file_path = f'/tmp/{filename}'

    # write to file
    with open(file_path, 'w') as f:
        f.write(content)

    return file_path
