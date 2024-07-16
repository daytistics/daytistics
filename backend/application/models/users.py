from datetime import datetime, timezone
from application.utils.whitelist import is_string_content_allowed
from application.utils.users import is_valid_username, is_good_password
import os
from flask import current_app as app
from application.extensions import db
import application.errors as errors


class User(db.Model):
    """
    Model for a new user
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    role = db.Column(db.String(64), default='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
def is_user_existing(id: int) -> bool:
    """
    Check if a user with the given ID exists in the database.

    Args:
        id (int): The ID of the user to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """

    return db.session.query(db.session.query(User).filter_by(id=id).exists()).scalar()

def get_user_by_id(user_id: int) -> User or None: # type: ignore
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        User or None: The user object if found, None otherwise.

    Raises:
        UserNotFoundError: If no user is found with the given ID.
    """

    if not is_user_existing(user_id):
        raise errors.UserNotFoundError("No user found with this ID")

    user = User.query.filter_by(id=user_id).first()
    return user

def register_user(username, password) -> User or None: # type: ignore
    """
    Register a new user with the provided username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        User or None: The registered user object if successful, None otherwise.

    Raises:
        MissingFieldError: If the username or password is not provided.
        InvalidNameError: If the username is invalid (must be between 3 and 20 characters and alphanumeric).
        ExplicitContentError: If the username contains explicit content.
        BadPasswordError: If the password is too weak or invalid (must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character).
    """

    if username is None or password is None or username == "" or password == "":
        raise errors.MissingFieldError("Username or password is not provided")

    if not is_valid_username(username):
        raise errors.InvalidNameError("Username is invalid (must be between 3 and 20 characters and alphanumeric)")

    if not is_string_content_allowed(username):
        raise errors.ExplicitContentError("Username contains explicit content")
    
    if not is_good_password(password):
        raise errors.BadPasswordError("Password is too weak or invalid (must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character)")

    from application.utils.encryption import encrypt_string
    user = User(username=username, password_hash=encrypt_string(password))
    db.session.add(user)
    db.session.commit()
    return user
    
def change_user_role(user_id: int, new_role: str) -> User or None: # type: ignore
    """
    Change the role of a user identified by the given user ID.

    Args:
        user_id (int): The ID of the user to change the role for.
        new_role (str): The new role to assign to the user. Must be either 'user' or 'admin'.

    Returns:
        User or None: The updated User object if the role was successfully changed, None otherwise.

    Raises:
        UserNotFoundError: If no user is found with the given user ID.
        MissingFieldError: If the new_role parameter is empty or None.
        InvalidRoleError: If the new_role parameter is not 'user' or 'admin'.
    """

    if not is_user_existing(user_id):
        raise errors.UserNotFoundError("No user found with this ID")

    if new_role not in ['user', 'admin']:
        if new_role == "" or new_role is None:
            raise errors.MissingFieldError("Role is not provided")
        raise errors.InvalidRoleError("Role is invalid (must be 'user' or 'admin')")

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return None
    user.role = new_role
    db.session.commit()
    return user

def delete_user(user_id: int, password: str) -> bool:
    """
    Deletes a user from the database.

    Args:
        user_id (int): The ID of the user to be deleted.
        password (str): The password of the user for verification.

    Returns:
        bool: True if the user is successfully deleted, False otherwise.

    Raises:
        UserNotFoundError: If no user is found with the given ID.
        MissingFieldError: If the password is not provided.
        IncorrectPasswordError: If the provided password is incorrect.
    """

    if not is_user_existing(user_id):
        raise errors.UserNotFoundError("No user found with this ID")

    if password is None or password == "":
        raise errors.MissingFieldError("Cannot verify action. Password is not provided")

    if not check_user_password(user_id, password):
        raise errors.IncorrectPasswordError("Cannot verify action. Password is incorrect")

    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return True

def check_user_password(user_id: int, password: str) -> bool:
    """
    Check if the provided password matches the password of the user with the given ID.

    Args:
        user_id (int): The ID of the user.
        password (str): The password to check.

    Returns:
        bool: True if the password is correct, False otherwise.

    Raises:
        errors.UserNotFoundError: If no user is found with the given ID.
        errors.MissingFieldError: If the password is not provided.
    """

    if not is_user_existing(user_id):
        raise errors.UserNotFoundError("No user found with this ID")
    
    if password is None or password == "":
        raise errors.MissingFieldError("Password is not provided")

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return False

    from application.utils.encryption import check_hashed_value
    is_correct = check_hashed_value(password, user.password_hash)

    return is_correct

def change_user_password(user_id: int, new_password: str, password: str) -> bool: # type: ignore
    """
    Change the password of a user.

    Args:
        user_id (int): The ID of the user.
        new_password (str): The new password to set for the user.
        password (str): The current password of the user.

    Returns:
        bool: True if the password is successfully changed, False otherwise.

    Raises:
        UserNotFoundError: If no user is found with the given ID.
        MissingFieldError: If the new password or current password is not provided.
        IncorrectPasswordError: If the current password is incorrect.
        BadPasswordError: If the new password is too weak or invalid (must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character).
    """

    if not is_user_existing(user_id):
        raise errors.UserNotFoundError("No user found with this ID")
    
    if new_password is None or new_password == "":
        raise errors.MissingFieldError("New password is not provided")

    if not is_good_password(new_password):
        raise errors.BadPasswordError("Password is too weak or invalid (must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character")

    if new_password == password:
        raise errors.SamePasswordError("New password is the same as the old password")

    if password is None or password == "":
        raise errors.MissingFieldError("Cannot verify action. Current password is not provided")

    if not check_user_password(user_id, password):
        raise errors.IncorrectPasswordError("Cannot verify action. Password is incorrect")

    user = User.query.filter_by(id=user_id).first()

    from application.utils.encryption import encrypt_string
    user.password_hash = encrypt_string(new_password)
    db.session.commit()
    return True


def change_username(user_id: int, new_username: str) -> User or None: # type: ignore
    """
    Change the username of a user.

    Args:
        user_id (int): The ID of the user.
        new_username (str): The new username to be set.

    Returns:
        User or None: The updated User object if the username is changed successfully, 
        None if the user is not found.

    Raises:
        UserNotFoundError: If no user is found with the given ID.
        MissingFieldError: If the new username is not provided.
        InvalidNameError: If the new username is invalid (must be between 3 and 20 characters and alphanumeric).
        ExplicitContentError: If the new username contains explicit content.
    """

    if not is_user_existing(user_id):
        raise errors.UserNotFoundError("No user found with this ID")

    if new_username is None or new_username == "":
        raise errors.MissingFieldError("New username is not provided")

    if not is_valid_username(new_username):
        raise errors.InvalidNameError("Username is invalid (must be between 3 and 20 characters and alphanumeric)")

    if not is_string_content_allowed(new_username):
        raise errors.ExplicitContentError("Username contains explicit content")

    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return None

    user.username = new_username
    db.session.commit()
    return user

def get_all_users() -> list:
    """
    Retrieve all users from the database.

    Returns:
        list: A list of tuples containing the user ID, the username, the email, the role, and the creation date of each user.
    """