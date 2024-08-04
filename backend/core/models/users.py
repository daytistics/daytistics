from datetime import datetime, timezone
from core.utils.users import is_valid_username, is_good_password
from core.utils.emails import is_valid_email, send_registration_request_email
from core.extensions import db
import core.errors as errors
from core.utils.encryption import check_password_hash, generate_password_hash


class User(db.Model):
    """
    Model for a new user
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    role = db.Column(db.String(64), default="user")
    verification = db.Column(db.String(64), default="pending")
    verification_rejections = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "<User {}>".format(self.username)


def is_user_existing_by_id(id: int) -> bool:
    """
    Check if a user with the given ID exists in the database.

    Args:
        id (int): The ID of the user to check.

    Returns:
        bool: True if the user exists, False otherwise.

    Raises:
        MissingFieldError: If the ID is not provided.
    """

    if id is None or id == "":
        raise errors.MissingFieldError("ID is not provided")

    return db.session.query(db.session.query(User).filter_by(id=id).exists()).scalar()


def is_user_existing_by_email(email: str) -> bool:
    """
    Check if a user with the given email exists in the database.

    Args:
        email (str): The email address to check.

    Returns:
        bool: True if a user with the given email exists, False otherwise.

    Raises:
        MissingFieldError: If the email is not provided.<br>
        InvalidEmailError: If the email is invalid.
    """

    if email is None or email == "":
        raise errors.MissingFieldError("Email is not provided")

    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")

    return db.session.query(
        db.session.query(User).filter_by(email=email).exists()
    ).scalar()


def get_user_by_id(user_id: int) -> User:
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        User or None: The user object if found, None otherwise.

    Raises:
        MissingFieldError: If the ID is not provided.<br>
        UserNotFoundError: If no user is found with the given ID.
    """

    if user_id is None or user_id == "":
        raise errors.MissingFieldError("ID is not provided")

    if not is_user_existing_by_id(user_id):
        raise errors.UserNotFoundError("No user found with this ID")

    user = User.query.filter_by(id=user_id).first()
    return user


def get_user_by_email(email: str) -> User:
    """
    Retrieve a user by their email.

    Args:
        email (str): The email of the user to retrieve.

    Returns:
        User or None: The user object if found, None otherwise.

    Raises:
        MissingFieldError: If the email is not provided.<br>
        InvalidEmailError: If the email is invalid.<br>
        UserNotFoundError: If no user is found with the given email.
    """

    if email is None or email == "":
        raise errors.MissingFieldError("Email is not provided")

    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")

    if not is_user_existing_by_email(email):
        raise errors.UserNotFoundError("No user found with this email")

    user = User.query.filter_by(email=email).first()
    return user


def register_user(username: str, password: str, email: str) -> bool:
    """
    Creates a new user in the database. The user is not verified until they verify their email address.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        email (str): The email of the user.

    Raises:
        MissingFieldError: If the username or password is not provided.<br>
        InvalidNameError: If the username is invalid.<br>
        InvalidEmailError: If the email is invalid.<br>
        EmailInUseError: If the email is already in use.<br>
        BadPasswordError: If the password is too weak or invalid.<br>

    Returns:
        bool: True if the user is successfully registered, False otherwise.
    """

    from core.extensions import verificator

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

    if is_user_existing_by_email(email):
        raise errors.EmailInUseError("Email is already in use")

    if not is_good_password(password):
        raise errors.BadPasswordError(
            "Password is too weak or invalid (must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character)"
        )

    try:
        code = verificator.add_registration_request(
            email, username, generate_password_hash(password), "user"
        )
        send_registration_request_email(email, code)
        return True
    except:
        return False


def change_user_role(email: str, new_role: str) -> User:
    """
    Change the role of a user identified by their email.

    Args:
        email (str): The email of the user.
        new_role (str): The new role to assign to the user. Must be either 'user' or 'admin'.

    Returns:
        User: The updated User object with the new role.

    Raises:
        MissingFieldError: If email or role is not provided.
        InvalidEmailError: If the email is invalid.
        UserNotFoundError: If no user is found with the provided email.
        InvalidRoleError: If the new role is invalid (must be 'user' or 'admin').
    """

    if email is None or email == "" or new_role is None or new_role == "":
        raise errors.MissingFieldError("Email or role is not provided")

    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")

    if not is_user_existing_by_email(email):
        raise errors.UserNotFoundError("No user found with this email")

    if new_role not in ["user", "admin"]:
        if new_role == "" or new_role is None:
            raise errors.MissingFieldError("Role is not provided")
        raise errors.InvalidRoleError("Role is invalid (must be 'user' or 'admin')")

    user = get_user_by_email(email)
    user.role = new_role
    db.session.commit()

    return user


# TODO: Implement user deletion functionality (including verification)
def delete_user(email: str) -> None:
    pass


def check_user_password(email: str, password: str) -> bool:
    """
    Check if the provided email and password match the user's credentials.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        bool: True if the email and password match, False otherwise.

    Raises:
        MissingFieldError: If the email or password is not provided.
        InvalidEmailError: If the email is invalid.
        UserNotFoundError: If no user is found with the provided email.
    """

    if email is None or email == "" or password is None or password == "":
        raise errors.MissingFieldError("Email or password is not provided")

    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")

    if not is_user_existing_by_email(email):
        raise errors.UserNotFoundError("No user found with this email")

    if password is None or password == "":
        raise errors.MissingFieldError("Password is not provided")

    user = get_user_by_email(email)

    is_correct = check_password_hash(password, user.password_hash)

    return is_correct


# TODO: Implement password change functionality (including verification)
def change_user_password(email: str, new_password: str) -> None:
    pass


def change_username(email: str, new_username: str) -> User:
    """
    Change the username of a user identified by their email.

    Args:
        email (str): The email of the user.
        new_username (str): The new username to be set.

    Returns:
        User: The updated User object.

    Raises:
        MissingFieldError: If email or new_username is not provided.
        InvalidEmailError: If the email is invalid.
        UserNotFoundError: If no user is found with the given email.
        InvalidNameError: If the new username is invalid.
    """

    if email is None or email == "" or new_username is None or new_username == "":
        raise errors.MissingFieldError("Email or new username is not provided")

    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")

    if not is_user_existing_by_email(email):
        raise errors.UserNotFoundError("No user found with this email")

    if not is_valid_username(new_username):
        raise errors.InvalidNameError(
            "Username is invalid (must be between 3 and 20 characters and alphanumeric)"
        )

    user = get_user_by_email(email)

    user.username = new_username
    db.session.commit()
    return user


# TODO: Implement password reset functionality (using verificator)
def reset_password(email: str) -> None:
    pass


# TODO: Tests for get_all_users
def get_all_users() -> list:
    """
    Retrieve all users from the database. This function might consume a lot of resources if there are many users.

    Returns:
        list: A list of tuples containing the user ID, the username, the email, the role, and the creation date of each user.
    """

    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append(
            (
                user.id,
                user.username,
                user.email,
                user.role,
                user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                user.verification,
                user.verification_rejections,
            )
        )
    return user_list

def is_verified(email: str) -> bool:
    """
    Checks if a user with the given email is verified.

    Args:
        email (str): The email of the user.

    Returns:
        bool: True if the user is verified, False otherwise.

    Raises:
        errors.MissingFieldError: If the email is not provided.
        errors.InvalidEmailError: If the email is invalid.
        errors.UserNotFoundError: If no user is found with the given email.
    """

    if email is None or email == "":
        raise errors.MissingFieldError("Email is not provided")
    
    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")
    
    if not is_user_existing_by_email(email):
        raise errors.UserNotFoundError("No user found with this email")
    
    user = get_user_by_email(email)
    return user.verification == "done"

def verify_user(email: str) -> bool:
    """
    Verifies a user by setting their verification status to "done" in the database.

    Args:
        email (str): The email of the user to be verified.

    Returns:
        bool: True if the user is successfully verified, False otherwise.
    """
    if email is None or email == "":
        raise errors.MissingFieldError("Email is not provided")
    
    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")
    
    if not is_user_existing_by_email(email):
        raise errors.UserNotFoundError("No user found with this email")
    
    try:
        user = get_user_by_email(email)
        user.verification = "done"
        db.session.commit()
        return True
    except:
        return False
    
def get_user_verification_status(email: str) -> str:
    """
    Get the verification status of a user based on their email.

    Args:
        email (str): The email of the user.

    Returns:
        str: The verification status of the user.

    Raises:
        errors.MissingFieldError: If the email is not provided.
        errors.InvalidEmailError: If the email is invalid.
        errors.UserNotFoundError: If no user is found with the given email.
    """

    if email is None or email == "":
        raise errors.MissingFieldError("Email is not provided")
    
    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")
    
    if not is_user_existing_by_email(email):
        raise errors.UserNotFoundError("No user found with this email")
    
    user = get_user_by_email(email)
    return user.verification

def increase_verification_rejections(email: str) -> None:
    """
    Increase the number of verification rejections for a user.

    Args:
        email (str): The email of the user.

    Raises:
        errors.MissingFieldError: If the email is not provided.
        errors.InvalidEmailError: If the email is invalid.
        errors.UserNotFoundError: If no user is found with the given email.
    """

    if email is None or email == "":
        raise errors.MissingFieldError("Email is not provided")
    
    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")
    
    if not is_user_existing_by_email(email):
        raise errors.UserNotFoundError("No user found with this email")
    
    user = get_user_by_email(email)
    user.verification_rejections += 1
    db.session.commit()