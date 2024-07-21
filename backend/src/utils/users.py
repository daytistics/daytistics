import string, random

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

# Examples for valid and invalid passwords
# print(is_good_password("password123"))  # False
# print(is_good_password("Password123"))  # False
# print(is_good_password("Password123!"))  # True
# print(is_good_password("Password123"))  # False

def generate_password():
    # Definiere die Zeichensätze
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # Berechne die Mindestanzahl für jede Kategorie
    min_length = 12
    min_uppercase = int(min_length * 0.3)
    min_lowercase = int(min_length * 0.3)
    min_digits = 3
    min_special = 2

    # Erstelle das Passwort
    password = (
        ''.join(random.choice(uppercase) for _ in range(min_uppercase)) +
        ''.join(random.choice(lowercase) for _ in range(min_lowercase)) +
        ''.join(random.choice(digits) for _ in range(min_digits)) +
        ''.join(random.choice(special_chars) for _ in range(min_special))
    )

    # Fülle auf, falls die Mindestlänge noch nicht erreicht ist
    remaining = min_length - len(password)
    if remaining > 0:
        password += ''.join(random.choice(lowercase + uppercase + digits + special_chars) for _ in range(remaining))

    # Mische das Passwort
    password_list = list(password)
    random.shuffle(password_list)
    return ''.join(password_list)
