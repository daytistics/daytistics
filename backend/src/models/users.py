from datetime import datetime, timezone
from src.utils.whitelist import is_string_content_allowed
from src.utils.users import is_valid_username, is_good_password
from src.utils.emails import send_verification_email, is_valid_email, is_email_in_use
from src.extensions import db
import src.errors as errors
from datetime import datetime
import re
from src.utils.verify import Verificator

class User(db.Model):
    """
    Model for a new user
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    role = db.Column(db.String(64), default="user")

    def __repr__(self):
        return "<User {}>".format(self.username)
    

def is_user_existing(id: int) -> bool:
    """
    Check if a user with the given ID exists in the database.

    Args:
        id (int): The ID of the user to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """

    return db.session.query(db.session.query(User).filter_by(id=id).exists()).scalar()


def get_user_by_id(user_id: int) -> User or None:  # type: ignore
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


# TODO: Write tests for this function
def register_user(_verificator: Verificator, username: str, password: str, email: str) -> None:  
    if username is None or password is None or username == "" or password == "":
        raise errors.MissingFieldError("Username or password is not provided")

    if not is_valid_username(username):
        raise errors.InvalidNameError(
            "Username is invalid (must be between 3 and 20 characters and alphanumeric)"
        )

    if not is_valid_email(email):
        raise errors.InvalidEmailError(
            "Email is invalid (must be between 3 and 50 characters and contain an @ symbol)"
        )

    if is_email_in_use(email):
        raise errors.EmailInUseError("Email is already in use")

    if not is_string_content_allowed(username):
        raise errors.ExplicitContentError("Username contains explicit content")

    if not is_good_password(password):
        raise errors.BadPasswordError(
            "Password is too weak or invalid (must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character)"
        )

    from src.utils.encryption import encrypt_string

    code = _verificator.add_verification_request(
        type=_verificator.REGISTRATION,
        email=email,
        username=username,
        password_hash=encrypt_string(password),
    )
    send_verification_email(email, code)

# TODO: Write tests for this function
def verify_action(type: int, email: str, code: str) -> bool:
    """
    Verifies the action based on the provided type, email, and code.

    Args:
        type (int): The type of verification action. Must be 1 (Register), 2 (Change password), or 3 (Delete account).
        email (str): The email associated with the verification request.
        code (str): The verification code.

    Returns:
        bool: True if the action is successfully verified, False otherwise.

    Raises:
        MissingFieldError: If email, action type, or code is not provided.
        VerificationError: If the verification code is not a 6-digit number or the verification type is invalid.
        InvalidEmailError: If the email is invalid.
    """

    if code is None or code == "" or email is None or email == "" or type is None:
        raise errors.MissingFieldError("Email, action type, or code is not provided")

    if not re.match(r"^\d{6}$", code):
        raise errors.VerificationError("Verification code must be a 6-digit number")

    if type not in [1, 2, 3]:
        raise errors.VerificationError("Invalid verification type (must be 1: Register, 2: Change password, or 3: Delete account)")

    if not is_valid_email(email):
        raise errors.InvalidEmailError(
            "Email is invalid (must be between 3 and 50 characters and contain an @ symbol)"
        )

    if not verificator.contains_request(email, type):
        raise errors.VerificationError(
            "No verification request found for this email and type"
        )

    request = verificator.requests[email]

    if not request["code"] == code:
        raise errors.VerificationError("Verification code is incorrect")

    match type:
        case 1:
            # Register user
            user = User(
                username=request["username"],
                password_hash=request["password_hash"],
                email=request["email"],
                role=request["role"]
            )
            db.session.add(user)
            db.session.commit()
            return True
        case 2:
            # Change password
            user = User.query.filter_by(id=request["id"]).first()
            user.password_hash = request["new_password"]
            db.session.commit()
            return True
        case 3:
            # Delete account
            user = User.query.filter_by(id=request["id"]).first()
            db.session.delete(user)
            db.session.commit()
            return True

    return False


def change_user_role(user_id: int, new_role: str) -> User or None:  # type: ignore
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

    if new_role not in ["user", "admin"]:
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
        raise errors.IncorrectPasswordError(
            "Cannot verify action. Password is incorrect"
        )

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

    from src.utils.encryption import check_hashed_value

    is_correct = check_hashed_value(password, user.password_hash)

    return is_correct


def change_user_password(user_id: int, new_password: str, password: str) -> bool:  # type: ignore
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
        raise errors.BadPasswordError(
            "Password is too weak or invalid (must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
        )

    if new_password == password:
        raise errors.SamePasswordError("New password is the same as the old password")

    if password is None or password == "":
        raise errors.MissingFieldError(
            "Cannot verify action. Current password is not provided"
        )

    if not check_user_password(user_id, password):
        raise errors.IncorrectPasswordError(
            "Cannot verify action. Password is incorrect"
        )

    user = User.query.filter_by(id=user_id).first()

    from src.utils.encryption import encrypt_string

    user.password_hash = encrypt_string(new_password)
    db.session.commit()
    return True


def change_username(user_id: int, new_username: str) -> User or None:  # type: ignore
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
        raise errors.InvalidNameError(
            "Username is invalid (must be between 3 and 20 characters and alphanumeric)"
        )

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
