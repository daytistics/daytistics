import random


def generate_verification_code() -> str:
    """
    Generates a verification code.

    Returns:
        str: The generated verification code.
    """

    return str(random.randint(100000, 999999))


def is_valid_verification_code(code: str) -> bool:
    """
    Check if a verification code is valid.

    Args:
        code (str): The verification code to be checked.

    Returns:
        bool: True if the code is valid, False otherwise.
    """

    return code.isnumeric() and len(code) == 6
