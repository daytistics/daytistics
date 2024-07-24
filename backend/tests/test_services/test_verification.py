import pytest
import datetime
from core.services.verification import Verificator
from core.utils.verification import generate_verification_code, is_valid_verification_code
import core.errors as errors
from unittest.mock import patch
from core.models import User
import core.models.users as users


@pytest.mark.parametrize(
    "email, username, password_hash, role",
    [
        ("test@example.com", "test_user", "hash123", "user"),
        ("alreadyinverificator@example.com", "test_user", "hash123", "user"),
    ],
)
def test_add_registration_request(
    verificator, email, username, password_hash, role
):
        code = verificator.add_registration_request(
            email, username, password_hash, role
        )

        user = users.get_user_by_email(email)

        assert code in verificator.registration_requests[user.id]["code"]
        assert verificator.registration_requests[user.id]["timestamp"] is not None
        assert verificator.registration_requests[user.id]["failures"] == 0


@pytest.mark.parametrize(
    "email, new_password, exception",
    [
        ("test@example.com", "new_hash123", None),
        (None, "new_hash123", errors.MissingFieldError),
        ("", "new_hash123", errors.MissingFieldError),
        ("test@example.com", None, errors.MissingFieldError),
    ],
)
def test_add_change_password_request(db, verificator, email, new_password, exception):

    user = User(email="test@example.com", username="test_user", password_hash="hash123", role="user")
    db.session.add(user)
    db.session.commit()

    if exception is not None:
        with pytest.raises(exception):
            verificator.add_change_password_request(email, new_password)
    else:
        code = verificator.add_change_password_request(email, new_password)
        assert code in verificator.change_password_requests[user.id]["code"]
        assert (
            verificator.change_password_requests[user.id]["new_password"] == new_password
        )
        assert verificator.change_password_requests[user.id]["timestamp"] is not None
        assert verificator.change_password_requests[user.id]["failures"] == 0


@pytest.mark.parametrize(
    "email, exception",
    [
        ("test@example.com", None),
        (None, errors.MissingFieldError),
        ("", errors.MissingFieldError),
    ],
)
def test_add_delete_account_request(db, verificator, email, exception):

    user = User(email="test@example.com", username="test_user", password_hash="hash123", role="user")
    db.session.add(user)
    db.session.commit()

    if exception is not None:
        with pytest.raises(exception):
            verificator.add_delete_account_request(email)
    else:
        code = verificator.add_delete_account_request(email)
        assert code in verificator.delete_account_requests[user.id]["code"]
        assert verificator.delete_account_requests[user.id]["timestamp"] is not None
        assert verificator.delete_account_requests[user.id]["failures"] == 0



@pytest.mark.parametrize(
    "email, code, expected_result, exception",
    [
        ("test@example.com", "123456", True, None),
        ("test@example.com", "654321", False, None),
        ("verified@example.com", "654321", False, None),
        ("notexists@example.com", "123456", None, errors.UserNotFoundError),
        ("rejected@example.com", "123456", None, errors.VerificationError),
        ("failures@example.com", "123456", None, errors.VerificationError),

    ],
)
def test_verify_registration_request(
    verificator, email, code, expected_result, exception, db
):
    verificator.add_registration_request("test@example.com", "test_user", "hash123", "user")
    verificator.registration_requests[1]["code"] = "123456"

    verificator.add_registration_request("failures@example.com", "test_user", "hash123", "user")
    verificator.registration_requests[2]["failures"] = 3

    verificator.add_registration_request("rejected@example.com", "test_user", "hash123", "user")
    users.get_user_by_email("rejected@example.com").rejects = 3
    db.session.commit()
    
    db.session.add(User(email="verified@example.com", username="test_user", password_hash="hash123", role="user"))
    db.session.commit()
    

    if exception:
        with pytest.raises(exception):
            verificator.verify_registration_request(email, code)
    else:
        result = verificator.verify_registration_request(email, code)
        assert result == expected_result
            

@pytest.mark.parametrize(
    "email, code, expected_result, exception",
    [
        ("test@example.com", "123456", True, None),
        ("test@example.com", "wrong_code", False, None),
        ("nonexistent@example.com", "123456", None, errors.UserNotFoundError),
    ],
)
def test_verify_change_password_request(db, verificator, email, code, expected_result, exception):
    if email == "test@example.com":
        user = User(email=email, username="test_user", password_hash="old_hash123", role="user")
        db.session.add(user)
        db.session.commit()
        verificator.add_change_password_request(email, "new_hash123")
        verificator.change_password_requests[user.id]["code"] = "123456"

    if exception:
        with pytest.raises(exception):
            verificator.verify_change_password_request(email, code)
    else:
        result = verificator.verify_change_password_request(email, code)
        assert result == expected_result
        if result:
            user = User.query.filter_by(email=email).first()
            assert user.password_hash == "new_hash123"

@pytest.mark.parametrize(
    "current_email, code, expected_result, exception",
    [
        ("test@example.com", "123456", True, None),
        ("test@example.com", "wrong_code", False, None),
        ("nonexistent@example.com", "123456", None, errors.UserNotFoundError),
    ],
)
def test_verify_change_email_request(db, verificator, current_email, code, expected_result, exception):
    if current_email == "test@example.com":
        user = User(email=current_email, username="test_user", password_hash="hash123", role="user")
        db.session.add(user)
        db.session.commit()
        verificator.add_change_email_request(current_email, "new@example.com")
        verificator.change_email_requests[user.id]["code"] = "123456"

    if exception:
        with pytest.raises(exception):
            verificator.verify_change_email_request(current_email, code)
    else:
        result = verificator.verify_change_email_request(current_email, code)
        assert result == expected_result
        if result:
            user = User.query.filter_by(username="test_user").first()
            assert user.email == "new@example.com"

@pytest.mark.parametrize(
    "email, code, expected_result, exception",
    [
        ("test@example.com", "123456", True, None),
        ("test@example.com", "wrong_code", False, None),
        ("nonexistent@example.com", "123456", None, errors.UserNotFoundError),
    ],
)
def test_verify_delete_account_request(db, verificator, email, code, expected_result, exception):
    if email == "test@example.com":
        user = User(email=email, username="test_user", password_hash="hash123", role="user")
        db.session.add(user)
        db.session.commit()
        verificator.add_delete_account_request(email)
        verificator.delete_account_requests[user.id]["code"] = "123456"

    if exception:
        with pytest.raises(exception):
            verificator.verify_delete_account_request(email, code)
    else:
        result = verificator.verify_delete_account_request(email, code)
        assert result == expected_result
        if result:
            assert User.query.filter_by(email=email).first() is None

@pytest.mark.parametrize(
    "email, code, expected_result, exception",
    [
        ("test@example.com", "123456", True, None),
        ("test@example.com", "wrong_code", False, None),
        ("nonexistent@example.com", "123456", None, errors.UserNotFoundError),
    ],
)
def test_verify_reset_password_request(db, verificator, email, code, expected_result, exception):
    if email == "test@example.com":
        user = User(email=email, username="test_user", password_hash="old_hash123", role="user")
        db.session.add(user)
        db.session.commit()
        verificator.add_reset_password_request(email, "new_hash123")
        verificator.reset_password_requests[user.id]["code"] = "123456"

    if exception:
        with pytest.raises(exception):
            verificator.verify_reset_password_request(email, code)
    else:
        result = verificator.verify_reset_password_request(email, code)
        assert result == expected_result
        if result:
            user = User.query.filter_by(email=email).first()
            assert user.password_hash == "new_hash123"

@pytest.mark.parametrize(
    "current_email, new_email, exception",
    [
        ("test@example.com", "new@example.com", None),
        ("test@example.com", "existing@example.com", errors.EmailInUseError),
        (None, "new@example.com", errors.MissingFieldError),
        ("test@example.com", None, errors.MissingFieldError),
        ("", "new@example.com", errors.MissingFieldError),
        ("test@example.com", "", errors.MissingFieldError),
    ],
)
def test_add_change_email_request(db, verificator, current_email, new_email, exception):
    user = User(email="test@example.com", username="test_user", password_hash="hash123", role="user")
    db.session.add(user)
    existing_user = User(email="existing@example.com", username="existing_user", password_hash="hash456", role="user")
    db.session.add(existing_user)
    db.session.commit()

    if exception:
        with pytest.raises(exception):
            verificator.add_change_email_request(current_email, new_email)
    else:
        code = verificator.add_change_email_request(current_email, new_email)
        assert code in verificator.change_email_requests[user.id]["code"]
        assert verificator.change_email_requests[user.id]["new_email"] == new_email
        assert verificator.change_email_requests[user.id]["timestamp"] is not None
        assert verificator.change_email_requests[user.id]["failures"] == 0

@pytest.mark.parametrize(
    "setup_requests, expected_counts",
    [
        (
            {
                "registration": ["test1@example.com"],
                "change_password": ["test2@example.com"],
                "reset_password": ["test3@example.com"],
                "delete_account": ["test4@example.com"],
                "change_email": ["test5@example.com"],
            },
            {
                "registration": 0,
                "change_password": 0,
                "reset_password": 0,
                "delete_account": 0,
                "change_email": 0,
            },
        ),
    ],
)
def test_remove_expired_requests(db, verificator, setup_requests, expected_counts):
    for email in setup_requests["registration"]:
        user = User(email=email, username=f"user_{email}", password_hash="hash123", role="user")
        db.session.add(user)
        db.session.commit()
        verificator.add_registration_request(email, f"user_{email}", "hash123", "user")
    for email in setup_requests["change_password"]:
        user = User(email=email, username=f"user_{email}", password_hash="hash123", role="user")
        db.session.add(user)
        db.session.commit()
        verificator.add_change_password_request(email, "new_hash123")
    for email in setup_requests["reset_password"]:
        user = User(email=email, username=f"user_{email}", password_hash="hash123", role="user")
        db.session.add(user)
        db.session.commit()
        verificator.add_reset_password_request(email, "new_hash123")
    for email in setup_requests["delete_account"]:
        user = User(email=email, username=f"user_{email}", password_hash="hash123", role="user")
        db.session.add(user)
        db.session.commit()
        verificator.add_delete_account_request(email)
    for email in setup_requests["change_email"]:
        user = User(email=email, username=f"user_{email}", password_hash="hash123", role="user")
        db.session.add(user)
        db.session.commit()
        verificator.add_change_email_request(email, f"new_{email}")

    # Manually set the timestamp to be more than 5 minutes ago
    for requests in [
        verificator.registration_requests,
        verificator.change_password_requests,
        verificator.reset_password_requests,
        verificator.delete_account_requests,
        verificator.change_email_requests,
    ]:
        for request in requests.values():
            request["timestamp"] = datetime.datetime.now() - datetime.timedelta(minutes=6)

    verificator.remove_expired_requests()

    assert len(verificator.registration_requests) == expected_counts["registration"]
    assert len(verificator.change_password_requests) == expected_counts["change_password"]
    assert len(verificator.reset_password_requests) == expected_counts["reset_password"]
    assert len(verificator.delete_account_requests) == expected_counts["delete_account"]
    assert len(verificator.change_email_requests) == expected_counts["change_email"]


@pytest.mark.parametrize(
    "email, expected_result",
    [
        ("test@example.com", True),
        ("nonexistent@example.com", errors.UserNotFoundError),
        ("notinverificator@example.com", False)
    ],
)
def test_exists_delete_account_request(db, verificator, email, expected_result):
    user = User(email="notinverificator@example.com", username="test_user", password_hash="hash123", role="user")
    db.session.add(user)
    db.session.commit()

    user = User(email="test@example.com", username="test_user", password_hash="hash123", role="user")
    db.session.add(user)
    db.session.commit()

    if expected_result == errors.UserNotFoundError:
        with pytest.raises(errors.UserNotFoundError):
            verificator.exists_change_password_request(email)
    else:
        if email == "test@example.com":
            verificator.add_delete_account_request(email)
            
        result = verificator.exists_delete_account_request(email)
        assert result == expected_result


@pytest.mark.parametrize(
    "email, expected_result",
    [
        ("test@example.com", True),
        ("nonexistent@example.com", False),
        ("notinverificator@example.com", False)
    ],
)
def test_exists_registration_request(db, verificator, email, expected_result):

    user = User(email="notinverificator@example.com", username="test_user", password_hash="hash123", role="user")
    db.session.add(user)
    db.session.commit()

    if expected_result == errors.UserNotFoundError:
        with pytest.raises(errors.UserNotFoundError):
            verificator.exists_registration_request(email)
    else:
        if email == "test@example.com":
            verificator.add_registration_request(email, "test_user", "hash123", "user")
            
        result = verificator.exists_registration_request(email)
        assert result == expected_result


@pytest.mark.parametrize(
    "email, expected_result",
    [
        ("test@example.com", True),
        ("nonexistent@example.com", errors.UserNotFoundError),
        ("notinverificator@example.com", False)
    ],
)
def test_exists_change_password_request(db, verificator, email, expected_result):
    user = User(email="notinverificator@example.com", username="test_user", password_hash="hash123", role="user")
    db.session.add(user)
    db.session.commit()

    user = User(email="test@example.com", username="test_user", password_hash="hash123", role="user")
    db.session.add(user)
    db.session.commit()

    if expected_result == errors.UserNotFoundError:
        with pytest.raises(errors.UserNotFoundError):
            verificator.exists_change_password_request(email)
    else:
        if email == "test@example.com":
            verificator.add_change_password_request(email, "hash123")
            
        result = verificator.exists_change_password_request(email)
        assert result == expected_result


@pytest.mark.parametrize(
    "email, expected_result",
    [
        ("test@example.com", True),
        ("nonexistent@example.com", errors.UserNotFoundError),
        ("notinverificator@example.com", False)
    ],
)
def test_exists_delete_account_request(db, verificator, email, expected_result):
    user = User(email="notinverificator@example.com", username="test_user", password_hash="hash123", role="user")
    db.session.add(user)
    db.session.commit()

    user = User(email="test@example.com", username="test_user", password_hash="hash123", role="user")
    db.session.add(user)
    db.session.commit()

    if expected_result == errors.UserNotFoundError:
        with pytest.raises(errors.UserNotFoundError):
            verificator.exists_delete_account_request(email)
    else:
        if email == "test@example.com":
            verificator.add_delete_account_request(email)
            
        result = verificator.exists_delete_account_request(email)
        assert result == expected_result

@pytest.mark.parametrize(
    "email, expected_result",
    [
        ("test@example.com", True),
        ("nonexistent@example.com", errors.UserNotFoundError),
        ("notinverificator@example.com", False)
    ],
)
def test_exists_change_email_request(db, verificator, email, expected_result):
    user = User(email="notinverificator@example.com", username="test_user", password_hash="hash123", role="user")
    db.session.add(user)
    db.session.commit()

    user = User(email="test@example.com", username="test_user", password_hash="hash123", role="user")
    db.session.add(user)
    db.session.commit()

    if expected_result == errors.UserNotFoundError:
        with pytest.raises(errors.UserNotFoundError):
            verificator.exists_change_email_request(email)
    else:
        if email == "test@example.com":
            verificator.add_change_email_request(email, "neuemail@examp.ecom")
            
        result = verificator.exists_change_email_request(email)
        assert result == expected_result


def test_remove_expired_requests(verificator):
    # Aktuelle Zeit holen
    current_time = datetime.datetime.now()

    # Neue Verifikationsanfragen mit verschiedenen Zeitstempeln hinzufügen
    verificator.registration_requests["user1@example.com"] = {
        "code": "code1",
        "timestamp": current_time - datetime.timedelta(minutes=6),
        "failures": 0
    }
    verificator.change_password_requests["user2@example.com"] = {
        "code": "code2",
        "timestamp": current_time - datetime.timedelta(minutes=4),
        "new_password": "new_password2",
        "failures": 0
    }
    verificator.reset_password_requests["user3@example.com"] = {
        "code": "code3",
        "timestamp": current_time - datetime.timedelta(minutes=10),
        "new_password": "new_password3",
        "failures": 0
    }
    verificator.delete_account_requests["user4@example.com"] = {
        "code": "code4",
        "timestamp": current_time - datetime.timedelta(minutes=7),
        "failures": 0
    }
    verificator.change_email_requests["user5@example.com"] = {
        "code": "code5",
        "timestamp": current_time - datetime.timedelta(minutes=3),
        "new_email": "new_user5@example.com",
        "failures": 0
    }

    # Methode zum Entfernen abgelaufener Anfragen aufrufen
    verificator.remove_expired_requests()

    # Überprüfen, dass abgelaufene Anfragen entfernt wurden und andere bestehen bleiben
    assert "user1@example.com" not in verificator.registration_requests
    assert "user2@example.com" in verificator.change_password_requests
    assert "user3@example.com" not in verificator.reset_password_requests
    assert "user4@example.com" not in verificator.delete_account_requests
    assert "user5@example.com" in verificator.change_email_requests

@pytest.mark.parametrize(
    "code, expected",
    [
        ("123456", True),
        ("12345", False),
        ("1234567", False),
        ("abcdef", False),
        ("12345a", False),
    ],
)
def test_is_valid_verification_code(code, expected):
    assert is_valid_verification_code(code) == expected


@pytest.mark.parametrize(
    "execution_count",
    [1, 5, 10],
)
def test_generate_verification_code(execution_count):
    for _ in range(execution_count):
        code = generate_verification_code()
        assert isinstance(code, str)
        assert len(code) == 6
        assert code.isdigit()


@pytest.mark.parametrize(
    "daemon_value",
    [True, False],
)
def test_scheduler_thread(daemon_value):
    with patch('threading.Thread') as mock_thread:
        mock_thread.return_value.daemon = daemon_value
        new_verificator = Verificator()
        assert new_verificator._scheduler_thread.daemon == True  # Changed this line
        mock_thread.assert_called_once_with(
            target=new_verificator._remove_expired_requests_loop
        )
        mock_thread.return_value.start.assert_called_once()


@pytest.mark.parametrize(
    "is_set_value",
    [True, False],
)
def test_stop_scheduler(verificator, is_set_value):
    with patch.object(verificator._stop_event, "set") as mock_set:
        with patch.object(verificator._scheduler_thread, "join") as mock_join:
            verificator.stop_scheduler()
            mock_set.assert_called_once()
            mock_join.assert_called_once()


@pytest.mark.parametrize(
    "loop_iterations",
    [1, 3, 5],
)
def test_remove_expired_requests_loop(verificator, loop_iterations):
    with patch("time.sleep") as mock_sleep:
        with patch.object(verificator, "remove_expired_requests") as mock_remove:
            def side_effect():
                if mock_remove.call_count >= loop_iterations:
                    verificator._stop_event.set()
            mock_remove.side_effect = side_effect
            
            verificator._remove_expired_requests_loop()
            
            assert mock_remove.call_count == loop_iterations
            assert mock_sleep.call_count == loop_iterations - 1
            if loop_iterations > 1:
                mock_sleep.assert_called_with(10)

def test_remove_expired_requests_loop_immediate_stop():
    verificator = Verificator()
    with patch("time.sleep") as mock_sleep:
        with patch.object(verificator, "remove_expired_requests") as mock_remove:
            verificator._stop_event.set()  # Set stop event immediately
            verificator._remove_expired_requests_loop()
            assert mock_remove.call_count == 0
            assert mock_sleep.call_count == 0

def test_remove_expired_requests_loop_single_iteration():
    verificator = Verificator()
    with patch("time.sleep") as mock_sleep:
        with patch.object(verificator, "remove_expired_requests") as mock_remove:
            def side_effect():
                verificator._stop_event.set()
            mock_remove.side_effect = side_effect
            
            verificator._remove_expired_requests_loop()
            
            assert mock_remove.call_count == 1
            assert mock_sleep.call_count == 0

def test_remove_expired_requests_loop_immediate_stop():
    verificator = Verificator()
    with patch("time.sleep") as mock_sleep:
        with patch.object(verificator, "remove_expired_requests") as mock_remove:
            verificator._stop_event.set()  # Set stop event immediately
            verificator._remove_expired_requests_loop()
            assert mock_remove.call_count == 0
            assert mock_sleep.call_count == 0

def test_singleton_instance():
    verificator1 = Verificator()
    verificator2 = Verificator()
    assert verificator1 is verificator2
