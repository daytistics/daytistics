def is_valid_username(name: str) -> bool:
    """
    Check if a username meets the following criteria:
    - Length is between 3 and 20 characters
    - Contains only alphanumeric characters and underscores

    Args:
        name (str): The username to be checked.

    Returns:
        bool: True if the username is valid, False otherwise.
    """
    if len(name) < 3 or len(name) > 20:
        return False

    if not name.replace("_", "").isalnum():
        return False

    return True


def is_good_password(password: str) -> bool:
    """
    Checks if a password meets the following criteria:
    - Length is at least 8 characters
    - Contains at least one digit
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one special character from the set: !\"#$%&'§()*+,-./:;<=>?@[\\]^_`{|}~
    - Contains only alphanumeric characters or special characters from the above set

    Args:
        password (str): The password to be checked.

    Returns:
        bool: True if the password meets all the criteria, False otherwise.
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
