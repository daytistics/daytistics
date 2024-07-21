from flask_bcrypt import Bcrypt
from flask import current_app


def encrypt_string(string: str, rounds=None, prefix=None) -> str:
    """
    Encrypts a string using bcrypt and returns the hashed version
    :param string: The string to encrypt
    :param rounds: The number of rounds to hash (default is 12)
    :param prefix: The prefix to use (2b, 2y, etc)
    :return: A hashed version of the string
    """

    with current_app.app_context():
        bcrypt = Bcrypt(current_app)

        return bcrypt.generate_password_hash(string, rounds, prefix).decode("utf-8")


def check_hashed_value(value: str, hashed_value: str) -> bool:
    """
    Checks if a value matches a hashed value
    :param value: The value to check
    :param hashed_value: The hashed value to check against
    :return: True if the value matches, False otherwise
    """

    with current_app.app_context():
        bcrypt = Bcrypt(current_app)

        return bcrypt.check_password_hash(hashed_value, value)
