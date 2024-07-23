from datetime import datetime, timezone
from src.utils.whitelist import is_string_content_allowed
from src.utils.users import is_valid_username, is_good_password
from src.utils.emails import is_valid_email, send_registration_request_email
from src.extensions import db, verificator
import src.errors as errors
from src.utils.encryption import encrypt_string, check_hashed_value

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

    def __repr__(self):
        return "<User {}>".format(self.username)
    
def is_user_existing_by_id(id: int) -> bool:
    """
    Check if a user with the given ID exists in the database.

    Args:
        id (int): The ID of the user to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """

    return db.session.query(db.session.query(User).filter_by(id=id).exists()).scalar()

def is_user_existing_by_email(email: str) -> bool:
    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")

    return db.session.query(db.session.query(User).filter_by(email=email).exists()).scalar()

def get_user_by_id(user_id: int) -> User: 
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        User or None: The user object if found, None otherwise.

    Raises:
        UserNotFoundError: If no user is found with the given ID.
    """

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
        UserNotFoundError: If no user is found with the given email.
    """

    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")

    if not is_user_existing_by_email(email):
        raise errors.UserNotFoundError("No user found with this email")

    user = User.query.filter_by(email=email).first()
    return user

def register_user(username: str, password: str, email: str) -> None:
    """
    Register a new user with the provided username, password, and email.

    Args:
        verificator (Verificator): The verificator object used for verification.
        username (str): The username of the user.
        password (str): The password of the user.
        email (str): The email of the user.

    Raises:
        MissingFieldError: If the username or password is not provided.<br>
        InvalidNameError: If the username is invalid.<br>
        InvalidEmailError: If the email is invalid.<br>
        EmailInUseError: If the email is already in use.<br>
        ExplicitContentError: If the username contains explicit content.<br>
        BadPasswordError: If the password is too weak or invalid.<br>

    Returns:
        None
    """

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

    if not is_string_content_allowed(username):
        raise errors.ExplicitContentError("Username contains explicit content")

    if not is_good_password(password):
        raise errors.BadPasswordError(
            "Password is too weak or invalid (must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character)"
        )

    code = verificator.add_registration_request(email, username, encrypt_string(password), "user")
    send_registration_request_email(email, code)

def change_user_role(email: str, new_role: str) -> bool:  

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

def delete_user(email: str) -> None:

    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")
    
    if not is_user_existing_by_email(email):
        raise errors.UserNotFoundError("No user found with this email")

    user = get_user_by_email(email)

    code = verificator.add_delete_account_request(user.email)
    # TODO: Send verification email

def check_user_password(email: str, password: str) -> bool:

    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")
    
    if not is_user_existing_by_email(email):
        raise errors.UserNotFoundError("No user found with this email")

    if password is None or password == "":
        raise errors.MissingFieldError("Password is not provided")

    user = get_user_by_email(email)

    

    is_correct = check_hashed_value(password, user.password_hash)

    return is_correct

def change_user_password(email: str, new_password: str) -> None:

    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")
    
    if not is_user_existing_by_email(email):
        raise errors.UserNotFoundError("No user found with this email")

    if new_password is None or new_password == "":
        raise errors.MissingFieldError("New password is not provided")

    if not is_good_password(new_password):
        raise errors.BadPasswordError(
            "Password is too weak or invalid (must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
        )


    user = get_user_by_email(email)

    verificator.add_change_password_request(user.email, encrypt_string(new_password))
    # TODO: Send verification email

def change_username(email: str, new_username: str) -> User or None:  # type: ignore

    if not is_valid_email(email):
        raise errors.InvalidEmailError("Email is invalid")
    
    if not is_user_existing_by_email(email):
        raise errors.UserNotFoundError("No user found with this email")

    if new_username is None or new_username == "":
        raise errors.MissingFieldError("New username is not provided")

    if not is_valid_username(new_username):
        raise errors.InvalidNameError(
            "Username is invalid (must be between 3 and 20 characters and alphanumeric)"
        )

    if not is_string_content_allowed(new_username):
        raise errors.ExplicitContentError("Username contains explicit content")

    user = get_user_by_email(email)

    user.username = new_username
    db.session.commit()
    return user

# TODO: Implement password reset functionality (using verificator)

def get_all_users() -> list:
    """
    Retrieve all users from the database.

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
                user.created_at,
            )
        )
    return user_list