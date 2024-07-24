from core.models import User, users
import datetime
import os
import pytest
import core.errors as errors
import unittest.mock as mock
from core.utils.encryption import check_password_hash, generate_password_hash


@pytest.mark.parametrize(
    "username, password, email, exception",
    [
        ("test_userA", "Erdbeerkuchen00!", "test@example.com", None),  
        (
            "I contain spaces",
            "Erdbeerkuchen00!",
            "test@example.com",
            errors.InvalidNameError,
        ),  
        (
            "test_userB",
            "password",
            "test@example.com",
            errors.BadPasswordError,
        ),  
        (
            "test_userC",
            "Password",
            "test@example.com",
            errors.BadPasswordError,
        ), 
        (
            "test_userD",
            "password0",
            "test@example.com",
            errors.BadPasswordError,
        ),  
        (
            "test_userE",
            "Password0",
            "test@example.com",
            errors.BadPasswordError,
        ), 
        (
            "test_userF",
            "password0§",
            "test@example.com",
            errors.BadPasswordError,
        ),  
        (
            "test_userG",
            "Password§",
            "test@example.com",
            errors.BadPasswordError,
        ), 
        (
            "test_userH",
            "password§",
            "test@example.com",
            errors.BadPasswordError,
        ),  
        (
            "test_userI",
            "pass",
            "test@example.com",
            errors.BadPasswordError,
        ),  
        (
            "test_userJ",
            None,
            "test@example.com",
            errors.MissingFieldError,
        ), 
        (
            None,
            "Erdbeerkuchen00!",
            "test@example.com",
            errors.MissingFieldError,
        ),  
        (
            "test_userA",
            "Erdbeerkuchen00!",
            "test.com",
            errors.InvalidEmailError,
        ),  
        (
            "test_userA",
            "Erdbeerkuchen00!",
            "testcom",
            errors.InvalidEmailError,
        ),  
        (
            "test_userA",
            "Erdbeerkuchen00!",
            "test@com",
            errors.InvalidEmailError,
        ),  
    ],
)
def test_register_user(app, verificator, username, password, email, exception):


    with mock.patch("src.models.users.encrypt_string") as mock_encrypt:

        mock_encrypt.return_value = "encrypted_password"

        def mock_add_registration_request(email, username, password_hash, role):
            verificator.registration_requests[email] = {
                "code": "123456",
                "username": username,
                "email": email,
                "password_hash": password_hash,
                "role": role,
                "timestamp": datetime.datetime.now(),
            }
            return "123456"

        with mock.patch.object(
            verificator,
            "add_registration_request",
            side_effect=mock_add_registration_request,
        ):

            with app.app_context():

                if exception is not None:
                    with pytest.raises(exception):
                        users.register_user(username, password, email)

                if exception is None:
                    users.register_user(
                        username=username, password=password, email=email
                    )
                    request = verificator.registration_requests[email]

                    assert request is not None
                    assert request["code"] == "123456"
                    assert request["username"] == username
                    assert request["email"] == email
                    assert request["password_hash"] == mock_encrypt.return_value
                    assert request["role"] == "user"


def test_is_user_existing_by_id(app, db):


    with app.app_context():
        user = User(
            username="test_user",
            password_hash="ErdbeerKuchen00!",
            email="test@example.com",
        )
        db.session.add(user)
        db.session.commit()

        assert users.is_user_existing_by_id(user.id) == True  # Tests if the user exists
        assert (
            users.is_user_existing_by_id(user.id + 1) == False
        )  # Tests if the user does not exist


@pytest.mark.parametrize(
    "email, exception",
    [
        ("test@example.com", None),  
        ("test.com", errors.InvalidEmailError), 
        ("testcom", errors.InvalidEmailError), 
        ("test@com", errors.InvalidEmailError),  
    ],
)
def test_is_user_existing_by_email(app, db, email, exception):


    with app.app_context():
        user = User(
            username="test_user",
            password_hash="ErdbeerKuchen00!",
            email="test@example.com",
        )
        db.session.add(user)
        db.session.commit()

        if exception is not None:
            with pytest.raises(exception):
                users.is_user_existing_by_email(email)
        else:
            assert (
                users.is_user_existing_by_email(user.email) == True
            )  # Tests if the user exists
            assert (
                users.is_user_existing_by_id(user.id + 1) == False
            )  # Tests if the user does not exist


@pytest.mark.parametrize(
    "user_id, exception",
    [
        (1, None),  
        (2, errors.UserNotFoundError), 
        (0, errors.UserNotFoundError),  
    ],
)
def test_get_user_by_id(app, db, user_id, exception):


    with app.app_context():

        user = User(
            username="test_user",
            password_hash="ErdbeerKuchen00!",
            email="test@example.com",
        )
        db.session.add(user)
        db.session.commit()

        if exception is not None:
            with pytest.raises(exception):
                users.get_user_by_id(user_id)
        else:
            assert user == users.get_user_by_id(user_id)


@pytest.mark.parametrize(
    "email, exception",
    [
        ("test@example.com", None), 
        ("test.com", errors.InvalidEmailError), 
        ("testcom", errors.InvalidEmailError), 
        ("test@com", errors.InvalidEmailError), 
        ("notexists@example.com", errors.UserNotFoundError),  
    ],
)
def test_get_user_by_email(app, db, email, exception):


    with app.app_context():
        user = User(
            username="test_user",
            password_hash="ErdbeerKuchen00!",
            email="test@example.com",
        )
        db.session.add(user)
        db.session.commit()

        if exception is not None:
            with pytest.raises(exception):
                users.get_user_by_email(email)
        else:
            assert user == users.get_user_by_email(user.email)


@pytest.mark.parametrize(
    "email, new_role, exception",
    [
        ("test@example.com", "admin", None),  
        ("test@example.com", "user", None),  
        ("nonexistent@example.com", "user", errors.UserNotFoundError), 
        ("nonexistent@example.com", "admin", errors.UserNotFoundError),  
        ("test@example.com", "invalid_role", errors.InvalidRoleError),  
        ("test@example.com", None, errors.MissingFieldError), 
        ("test@example.com", "", errors.MissingFieldError),  
    ],
)
def test_change_user_role(app, db, email, new_role, exception):

    with app.app_context():
        user = User(username="test_user", password_hash="ErdbeerKuchen00!", email="test@example.com")
        db.session.add(user)
        db.session.commit()

        if email == "test@example.com":
            assert user.role == "user"
            assert user == users.get_user_by_email(email)
        else:
            with pytest.raises(errors.UserNotFoundError):
                users.get_user_by_email(email)

        if exception:
            with pytest.raises(exception):
                users.change_user_role(email, new_role)
        else:
            users.change_user_role(email, new_role)
            updated_user = users.get_user_by_email(email)
            assert updated_user.role == new_role


@pytest.mark.parametrize(
    "email, exception",
    [
        ("test@example.com", None), 
        (
            "test2@example.com",
            errors.UserNotFoundError,
        ),
        ("t@com", errors.InvalidEmailError),
        ("t.com", errors.InvalidEmailError),
        ("tcom", errors.InvalidEmailError)  
    ],
)
def test_delete_user(app, db, verificator, email, exception):
    def mock_add_delete_account_request(email):
        verificator.delete_account_requests[email] = {
            "code": "123456",
            "email": email,
            "timestamp": datetime.datetime.now(),
        }
        return "123456"

    with mock.patch.object(
        verificator,
        "add_delete_account_request",
        side_effect=mock_add_delete_account_request,
    ):

        with app.app_context():

            user = User(
                username="test_user",
                password_hash=generate_password_hash("ErdbeerKuchen00!"),
                email="test@example.com",
            )
            db.session.add(user)
            db.session.commit()

            if exception is not None:
                with pytest.raises(exception):
                    users.delete_user(email)
            else:
                users.delete_user(email)
                request = verificator.delete_account_requests[user.email]

                assert request is not None
                assert request["code"] is not None
                assert request["email"] == user.email
                assert request["timestamp"] is not None
                assert request["code"] == "123456"


@pytest.mark.parametrize(
    "email, password, exception",
    [
        ("test@example.com", "ErdbeerKuchen00!", None),  
        ("tes2t@example.com", "ErdbeerKuchen00!", errors.UserNotFoundError),  
        ("test@example.com", None, errors.MissingFieldError), 
        ("test@example.com", "", errors.MissingFieldError),  
    ],
)
def test_check_user_password(app, db, email, password, exception):

    with app.app_context():

        hashed_password = generate_password_hash(password) if password else None
        user = User(
            username=password, password_hash=hashed_password, email="test@example.com"
        )
        db.session.add(user)
        db.session.commit()

        if exception is not None:
            with pytest.raises(exception):
                users.check_user_password(email, password)
        else:
            assert users.check_user_password(email, password) == True


@pytest.mark.parametrize(
    "email, new_password, exception",
    [
        ("test@example.com", "NewPassword00!", None),  # 
        (
            "tes2t@example.com",
            "NewPassword00!",
            errors.UserNotFoundError,
        ),  
        (
            "test@example.com",
            None,
            errors.MissingFieldError,
        ),  
        (
            "test@example.com",
            "password",
            errors.BadPasswordError,
        ),  
        (
            "test@example.com",
            "Password",
            errors.BadPasswordError,
        ),  
        (
            "test@example.com",
            "password0",
            errors.BadPasswordError,
        ), 
        (
            "test@example.com",
            "Password0",
            errors.BadPasswordError,
        ), 
        (
            "test@example.com",
            "password0§",
            errors.BadPasswordError,
        ), 
        (
            "test@example.com",
            "Password§",
            errors.BadPasswordError,
        ),  
        (
            "test@example.com",
            "password§",
            errors.BadPasswordError,
        ),  
        (
            "test@example.com",
            "pass",
            errors.BadPasswordError,
        ),  
    ],
)
def test_change_user_pasword(app, db, verificator, email, new_password, exception):


    def mock_add_change_password_request(email, new_password):
        verificator.change_password_requests[email] = {
            "code": "123456",
            "email": email,
            "new_password": new_password,
            "timestamp": datetime.datetime.now(),
        }
        return "123456"

    verificator

    with mock.patch.object(
        verificator,
        "add_change_password_request",
        side_effect=mock_add_change_password_request,
    ):

        with app.app_context():
            user = User(
                username="Test_User",
                password_hash="Dasisteintollespw12!",
                email="test@example.com",
            )
            db.session.add(user)
            db.session.commit()

            if exception is not None:
                with pytest.raises(exception):
                    users.change_user_password(email, new_password)
            else:
                users.change_user_password(email, new_password)
                request = verificator.change_password_requests[email]
                assert request is not None
                assert request["code"] == "123456"


@pytest.mark.parametrize(
    "email, new_username, exception",
    [
        ("test@example.com", "Jakob", None),
        ("te2st@example.com", "Jakob", errors.UserNotFoundError),
        ("test@example.com", "I contain spaces", errors.InvalidNameError),
        (
            "test@example.com",
            None,
            errors.MissingFieldError,
        ),
        ("test@example.com", "", errors.MissingFieldError),
    ],
)
def test_change_username(app, db, email, new_username, exception):

    with app.app_context():

        user = User(
            username="test_user",
            password_hash="ErdbeerKuchen00!",
            email="test@example.com",
        )
        db.session.add(user)
        db.session.commit()

        if exception is not None:
            with pytest.raises(exception):
                users.change_username(email, new_username)

        else:

            users.change_username(email, new_username)
            assert user.username == new_username
