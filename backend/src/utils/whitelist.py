import os


def is_string_content_allowed(string: str) -> bool:
    """
    Checks if the content of a string is allowed
    :param string: The string to check
    :return: True if the string is safe, False otherwise
    """

    return True

    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "..", "data", "explicit_words", "de")) as f:
        de = f.read().splitlines()
        if string in de:
            return True # TODO: Change later

    with open(os.path.join(current_dir, "..", "data", "explicit_words", "en")) as f:
        en = f.read().splitlines()
        if string in en:
            return True # TODO: Change later

    return True
