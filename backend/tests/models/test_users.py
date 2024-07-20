from flask import Flask
from src.models import User, users
import datetime
import os
import pytest
import sys
import src.errors as errors
import unittest.mock as mock


@pytest.mark.parametrize(
    "username, password, email, exception",
    [
        ("test_userA", "Erdbeerkuchen00!", "test@example.com", None),  # Valid user
        (
            "I contain spaces",
            "Erdbeerkuchen00!",
            "test@example.com",
            errors.InvalidNameError,
        ),  # InvalidUsernameError
        (
            "test_userB",
            "password",
            "test@example.com",
            errors.BadPasswordError,
        ),  # BadPasswordError -> No uppercase letter & No digit & No special character
        (
            "test_userC",
            "Password",
            "test@example.com",
            errors.BadPasswordError,
        ),  # BadPasswordError -> No digit & No special character
        (
            "test_userD",
            "password0",
            "test@example.com",
            errors.BadPasswordError,
        ),  # BadPasswordError -> No uppercase letter & No special character
        (
            "test_userE",
            "Password0",
            "test@example.com",
            errors.BadPasswordError,
        ),  # BadPasswordError -> No special character
        (
            "test_userF",
            "password0§",
            "test@example.com",
            errors.BadPasswordError,
        ),  # BadPasswordError -> No uppercase letter
        (
            "test_userG",
            "Password§",
            "test@example.com",
            errors.BadPasswordError,
        ),  # BadPasswordError -> No digit
        (
            "test_userH",
            "password§",
            "test@example.com",
            errors.BadPasswordError,
        ),  # BadPasswordError -> No uppercase letter & No digit
        (
            "test_userI",
            "pass",
            "test@example.com",
            errors.BadPasswordError,
        ),  # BadPasswordError -> Password too short
        (
            "Idiot",
            "Erdbeerkuchen00!",
            "test@example.com",
            errors.ExplicitContentError,
        ),  # ExplicitContentError
        (
            "test_userJ",
            None,
            "test@example.com",
            errors.MissingFieldError,
        ),  # MissingFieldError -> Missing password
        (
            None,
            "Erdbeerkuchen00!",
            "test@example.com",
            errors.MissingFieldError,
        ),  # MissingFieldError -> Missing username
        ("test_userA", "Erdbeerkuchen00!", "test.com", errors.InvalidEmailError),  # InvalidEmailError
        ("test_userA", "Erdbeerkuchen00!", "testcom", errors.InvalidEmailError),  # InvalidEmailError
        ("test_userA", "Erdbeerkuchen00!", "test@com", errors.InvalidEmailError),  # InvalidEmailError
    ],
)

def test_register_user(app, verificator, username, password, email, exception):

    if os.environ.get("ENVIRONMENT") != "testing":
            pytest.skip(
                "Tests are running against the production database. Refusing to run tests."
            )

    with mock.patch('src.models.users.encrypt') as mock_encrypt, mock.patch('verificator.add_verification_request') as mock_add_verification_request:

        mock_encrypt.return_value = 'encrypted_password'
        mock_add_verification_request.return_value = "123456"

        with app.app_context():

            if exception is not None:
                with pytest.raises(exception):
                    users.register_user(verificator, username, password, email)

            if exception is None:
                users.register_user(username, password, email)
                request = verificator.requests[email]

                

                assert request != None
                assert request["code"] == mock_add_verification_request.return_value
                assert request["username"] == username
                assert request["type"] == verificator.REGISTRATION
                assert request["email"] == email
                assert request["password_hash"] == mock_encrypt.return_value
                assert request["role"] == "user"

            # assert user.username == username
            # assert user.password_hash is not None
            # assert user.role == "user"
            # assert user.id is not None
            # assert user.created_at is not None
            # assert user.created_at.utcoffset() == datetime.timedelta(0)
            # assert user.created_at < datetime.datetime.now(tz=datetime.timezone.utc)
            # assert user.created_at > datetime.datetime.now(
            #     tz=datetime.timezone.utc
            # ) - datetime.timedelta(minutes=1)
            # assert user == users.get_user_by_id(user.id)
            # assert user == User.query.filter_by(id=user.id).first()
            # assert user == User.query.filter_by(username=user.username).first()


def test_is_user_existing(app):
    with app.app_context():
        user = users.register_user("test_user", "ErdbeerKuchen00!")
        assert users.is_user_existing(user.id) == True  # Tests if the user exists
        assert (
            users.is_user_existing(user.id + 1) == False
        )  # Tests if the user does not exist


@pytest.mark.parametrize(
    "user_id, exception",
    [
        (1, None),  # Valid user
        (2, errors.UserNotFoundError),  # No user with id 2
        (0, errors.UserNotFoundError),  # No user with id 0
    ],
)
def test_get_user_by_id(app, user_id, exception):
    with app.app_context():

        user = users.register_user("test_user", "ErdbeerKuchen00!")

        if exception is not None:
            with pytest.raises(exception):
                users.get_user_by_id(user_id)
        else:
            assert user == users.get_user_by_id(user_id)


@pytest.mark.parametrize(
    "user_id, new_role, exception",
    [
        (1, "admin", None),  # Valid role
        (1, "user", None),  # Valid role
        (2, "user", errors.UserNotFoundError),  # No user with id 2
        (2, "admin", errors.UserNotFoundError),  # No user with id 2
        (1, "invalid_role", errors.InvalidRoleError),  # Invalid role
        (1, None, errors.MissingFieldError),  # Missing role
        (1, "", errors.MissingFieldError),  # Missing role
    ],
)
def test_change_user_role(app, user_id, new_role, exception):
    with app.app_context():

        user = users.register_user("test_user", "ErdbeerKuchen00!")

        assert user.role == "user"
        assert user == users.get_user_by_id(user.id)

        if exception is not None:
            with pytest.raises(exception):
                users.change_user_role(user_id, new_role)
        else:
            users.change_user_role(user_id, new_role)


@pytest.mark.parametrize(
    "user_id, password, exception",
    [
        (1, "ErdbeerKuchen00!", None),  # Valid password
        (2, "ErdbeerKuchen00!", errors.UserNotFoundError),  # No user with id 2
        (1, None, errors.MissingFieldError),  # MissingFieldError -> Missing password
        (1, "", errors.MissingFieldError),  # MissingFieldError -> Missing password
        (
            1,
            "Blaubeerkuchen00!",
            errors.IncorrectPasswordError,
        ),  # Password is incorrect
    ],
)
def test_delete_user(app, user_id, password, exception):
    with app.app_context():

        user = users.register_user("test_user", "ErdbeerKuchen00!")

        if exception is not None:
            with pytest.raises(exception):
                users.delete_user(user_id, password)
        else:
            assert users.delete_user(user_id, password) == True
            assert users.is_user_existing(user_id) == False


@pytest.mark.parametrize(
    "user_id, password, exception",
    [
        (1, "ErdbeerKuchen00!", None),  # Valid password
        (2, "ErdbeerKuchen00!", errors.UserNotFoundError),  # No user with id 2
        (1, None, errors.MissingFieldError),  # MissingFieldError -> Missing password
        (1, "", errors.MissingFieldError),  # MissingFieldError -> Missing password
    ],
)
def test_check_user_password(app, user_id, password, exception):
    with app.app_context():

        user = users.register_user("test_user", "ErdbeerKuchen00!")

        if exception is not None:
            with pytest.raises(exception):
                users.check_user_password(user_id, password)
        else:
            assert users.check_user_password(user_id, password) == True


@pytest.mark.parametrize(
    "user_id, new_password, password, exception",
    [
        (1, "NewPassword00!", "ErdbeerKuchen00!", None),  # Valid password change
        (
            2,
            "NewPassword00!",
            "ErdbeerKuchen00!",
            errors.UserNotFoundError,
        ),  # No user with id 2
        (
            1,
            "NewPassword00!",
            None,
            errors.MissingFieldError,
        ),  # MissingFieldError -> Missing current password
        (
            1,
            "NewPassword00!",
            "",
            errors.MissingFieldError,
        ),  # MissingFieldError -> Missing current password
        (
            1,
            "",
            "ErdbeerKuchen00!",
            errors.MissingFieldError,
        ),  # MissingFieldError -> Missing new password
        (
            1,
            None,
            "ErdbeerKuchen00!",
            errors.MissingFieldError,
        ),  # MissingFieldError -> Missing new password
        (
            1,
            "password",
            "ErdbeerKuchen00!",
            errors.BadPasswordError,
        ),  # BadPasswordError -> No uppercase letter & No digit & No special character
        (
            1,
            "Password",
            "ErdbeerKuchen00!",
            errors.BadPasswordError,
        ),  # BadPasswordError -> No digit & No special character
        (
            1,
            "password0",
            "ErdbeerKuchen00!",
            errors.BadPasswordError,
        ),  # BadPasswordError -> No uppercase letter & No special character
        (
            1,
            "Password0",
            "ErdbeerKuchen00!",
            errors.BadPasswordError,
        ),  # BadPasswordError -> No special character
        (
            1,
            "password0§",
            "ErdbeerKuchen00!",
            errors.BadPasswordError,
        ),  # BadPasswordError -> No uppercase letter
        (
            1,
            "Password§",
            "ErdbeerKuchen00!",
            errors.BadPasswordError,
        ),  # BadPasswordError -> No digit
        (
            1,
            "password§",
            "ErdbeerKuchen00!",
            errors.BadPasswordError,
        ),  # BadPasswordError -> No uppercase letter & No digit
        (
            1,
            "pass",
            "ErdbeerKuchen00!",
            errors.BadPasswordError,
        ),  # BadPasswordError -> Password too short
        (
            1,
            "ErdbeerKuchen00!",
            "ErdbeerKuchen00!",
            errors.SamePasswordError,
        ),  # SamePasswordError
        (
            1,
            "NewPassword00!",
            "ErdbeerKuchen10!",
            errors.IncorrectPasswordError,
        ),  # Incorrect current password
    ],
)
def test_change_user_pasword(app, user_id, new_password, password, exception):
    with app.app_context():

        user = users.register_user("test_user", "ErdbeerKuchen00!")

        if exception is not None:
            with pytest.raises(exception):
                users.change_user_password(user_id, new_password, password)
        else:
            assert users.change_user_password(user_id, new_password, password) == True
            assert users.check_user_password(user_id, new_password) == True


@pytest.mark.parametrize(
    "user_id, new_username, exception",
    [
        (1, "Jakob", None),  # Username changed successfully
        (2, "Jakob", errors.UserNotFoundError),  # No user with id 2
        (1, "I contain spaces", errors.InvalidNameError),  # InvalidUsernameError
        (
            1,
            None,
            errors.MissingFieldError,
        ),  # MissingFieldError -> Missing new username
        (1, "", errors.MissingFieldError),  # MissingFieldError -> Missing new username
        (1, "Idiot", errors.ExplicitContentError),  # ExplicitContentError
    ],
)
def test_change_username(app, user_id, new_username, exception):
    with app.app_context():

        user = users.register_user("Franz", "Erdbeerkuchen00!")

        if exception is not None:
            with pytest.raises(exception):
                users.change_username(user_id, new_username)

        else:
            assert users.change_username(user_id, new_username) == user
