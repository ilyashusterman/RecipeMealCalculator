def load_mock_file(filename):
    """

    :param filename:
    :return: return byte string
    """
    with open(filename, '+rb') as file:
        return file.read()


def save_mock_file(filename, content):
    with open(filename, '+wb') as file:
        return file.write(content)
