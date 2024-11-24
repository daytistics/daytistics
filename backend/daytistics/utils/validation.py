import re


def is_valid_email(email: str) -> bool:
    """
    Check if the given email is valid.

    Args:
        email (str): The email address to be checked.

    Returns:
        bool: True if the email is valid, False otherwise.
    """

    return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))


def is_valid_username(username: str) -> bool:
    """
    Check if a username is valid. A username is valid if it contains only letters, numbers, and underscores, and is at least 5 characters long.

    Args:
        username (str): The username to be checked.

    Returns:
        bool: True if the username is valid, False otherwise.
    """

    return bool(re.match(r"^[a-zA-Z0-9_]{5,}$", username))


def is_valid_password(password: str) -> bool:
    """
    Check if a password is valid. A password is valid if it contains at least one lowercase letter, one uppercase letter, one number, one special character, and is at least 8 characters long.

    Args:
        password (str): The password to be checked.

    Returns:
        bool: True if the password is valid, False otherwise.
    """

    password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[#?!@$%^&*\-§]).{8,}$"
    return bool(re.match(password_regex, password))
