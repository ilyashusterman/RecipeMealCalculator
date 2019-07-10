def load_mock_file(filename):
    with open(filename, '+rb') as f:
        return f.read()


def save_mock_file(filename, content):
    with open(filename, '+wb') as f:
        return f.write(content)
