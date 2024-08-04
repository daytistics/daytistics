from flask_bcrypt import Bcrypt
from flask import current_app


def generate_password_hash(password: str, rounds=None, prefix=None) -> str:
    """
    Generate a password hash using bcrypt.

    Args:
        password (str): The password to be hashed.
        rounds (int, optional): The number of rounds to use for hashing. Defaults to None.
        prefix (str, optional): The prefix to use for the hash. Defaults to None.

    Returns:
        str: The generated password hash.

    """
    with current_app.app_context():
        bcrypt = Bcrypt(current_app)
        return bcrypt.generate_password_hash(password, rounds, prefix).decode("utf-8")


def check_password_hash(password: str, pw_hash: str) -> bool:
    """
    Check if a password matches the given hash. The hash should be a bcrypt hash.

    Args:
        password (str): The password to check.
        pw_hash (str): The hash to compare against.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """

    with current_app.app_context():
        bcrypt = Bcrypt(current_app)
        return bcrypt.check_password_hash(pw_hash, password)
