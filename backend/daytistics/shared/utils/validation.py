import re


def is_valid_email(email: str):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return email_regex.match(email) is not None


def is_valid_password(password: str, forbidden_parts: list[str] = []):
    # Password rules:
    # - At least 8 characters
    # - At least 1 uppercase letter
    # - At least 1 lowercase letter
    # - At least 1 number
    # - At least 1 common symbol. those are: !@#$%^&*()-_=+[]{}|;:,.<>§
    password_regex = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_=+[\]{}|;:,.<>§]).{8,}$"
    )
    return password_regex.match(password) is not None and all(
        part not in password for part in forbidden_parts
    )


def is_valid_username(username: str):
    # Username rules:
    # - At least 4 characters
    # - At most 20 characters
    # - Only alphanumeric characters and underscores
    username_regex = re.compile(r"^[a-zA-Z0-9_]{4,20}$")
    return username_regex.match(username) is not None
