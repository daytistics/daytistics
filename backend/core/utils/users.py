def is_valid_username(name: str) -> bool:
    """
    Checks if a username is valid
    :param name: The username to check
    :return: True if the username is valid, False otherwise
    """
    if len(name) < 3 or len(name) > 20:
        return False

    #
    if not name.replace("_", "").isalnum():
        return False

    return True


def is_good_password(password: str) -> bool:
    """
    Checks if a password is good
    :param password: The password to check
    :return: True if the password is good, False otherwise
    """
    if len(password) < 8:
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    special_chars = "!\"#$%&'§()*+,-./:;<=>?@[\\]^_`{|}~"

    if not any(char in special_chars for char in password):
        return False

    if not any(char.isalnum() or char in special_chars for char in password):
        return False

    return True
