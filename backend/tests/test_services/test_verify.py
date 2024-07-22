import pytest
import datetime
from src.services.verify import (
    Verificator,
    generate_verification_code,
    is_valid_verification_code,
)
import src.errors as errors
from unittest.mock import patch, MagicMock


@pytest.mark.parametrize(
    "email, username, password_hash, role, exception",
    [
        ("test@example.com", "test_user", "hash123", "user", None),
        (None, "test_user", "hash123", "user", errors.MissingFieldError),
        ("", "test_user", "hash123", "user", errors.MissingFieldError),
        ("test@example.com", None, "hash123", "user", errors.MissingFieldError),
        ("test@example.com", "test_user", None, "user", errors.MissingFieldError),
        ("test@example.com", "test_user", "hash123", None, errors.MissingFieldError),
    ],
)
def test_add_registration_request(
    verificator, email, username, password_hash, role, exception
):
    if exception is not None:
        with pytest.raises(exception):
            verificator.add_registration_request(email, username, password_hash, role)
    else:
        code = verificator.add_registration_request(
            email, username, password_hash, role
        )
        assert code in verificator.registration_requests[email]["code"]
        assert verificator.registration_requests[email]["email"] == email
        assert verificator.registration_requests[email]["username"] == username
        assert (
            verificator.registration_requests[email]["password_hash"] == password_hash
        )
        assert verificator.registration_requests[email]["role"] == role


@pytest.mark.parametrize(
    "email, new_password, exception",
    [
        ("test@example.com", "new_hash123", None),
        (None, "new_hash123", errors.MissingFieldError),
        ("", "new_hash123", errors.MissingFieldError),
        ("test@example.com", None, errors.MissingFieldError),
    ],
)
def test_add_change_password_request(verificator, email, new_password, exception):
    if exception is not None:
        with pytest.raises(exception):
            verificator.add_change_password_request(email, new_password)
    else:
        code = verificator.add_change_password_request(email, new_password)
        assert code in verificator.change_password_requests[email]["code"]
        assert verificator.change_password_requests[email]["email"] == email
        assert (
            verificator.change_password_requests[email]["new_password"] == new_password
        )


@pytest.mark.parametrize(
    "email, exception",
    [
        ("test@example.com", None),
        (None, errors.MissingFieldError),
        ("", errors.MissingFieldError),
    ],
)
def test_add_delete_account_request(verificator, email, exception):
    if exception is not None:
        with pytest.raises(exception):
            verificator.add_delete_account_request(email)
    else:
        code = verificator.add_delete_account_request(email)
        assert code in verificator.delete_account_requests[email]["code"]
        assert verificator.delete_account_requests[email]["email"] == email


@pytest.mark.parametrize(
    "email, code, expected_result, exception",
    [
        ("test@example.com", "123456", True, None),
        ("test@example.com", "wrong_code", False, None),
        ("nonexistent@example.com", "123456", None, errors.VerificationError),
    ],
)
def test_verify_registration_request(
    verificator, email, code, expected_result, exception
):
    if email == "test@example.com":
        verificator.add_registration_request(email, "test_user", "hash123", "user")
        verificator.registration_requests[email]["code"] = "123456"

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
        ("nonexistent@example.com", "123456", None, errors.VerificationError),
    ],
)
def test_verify_change_password_request(
    verificator, email, code, expected_result, exception
):
    if email == "test@example.com":
        verificator.add_change_password_request(email, "new_hash123")
        verificator.change_password_requests[email]["code"] = "123456"

    if exception:
        with pytest.raises(exception):
            verificator.verify_change_password_request(email, code)
    else:
        result = verificator.verify_change_password_request(email, code)
        assert result == expected_result


@pytest.mark.parametrize(
    "email, code, expected_result, exception",
    [
        ("test@example.com", "123456", True, None),
        ("test@example.com", "wrong_code", False, None),
        ("nonexistent@example.com", "123456", None, errors.VerificationError),
    ],
)
def test_verify_delete_account_request(
    verificator, email, code, expected_result, exception
):
    if email == "test@example.com":
        verificator.add_delete_account_request(email)
        verificator.delete_account_requests[email]["code"] = "123456"

    if exception:
        with pytest.raises(exception):
            verificator.verify_delete_account_request(email, code)
    else:
        result = verificator.verify_delete_account_request(email, code)
        assert result == expected_result


@pytest.mark.parametrize(
    "email, expected_result",
    [
        ("test@example.com", True),
        ("nonexistent@example.com", False),
    ],
)
def test_exists_registration_request(verificator, email, expected_result):
    if email == "test@example.com":
        verificator.add_registration_request(email, "test_user", "hash123", "user")
    result = verificator.exists_registration_request(email)
    assert result == expected_result


@pytest.mark.parametrize(
    "email, expected_result",
    [
        ("test@example.com", True),
        ("nonexistent@example.com", False),
    ],
)
def test_exists_change_password_request(verificator, email, expected_result):
    if email == "test@example.com":
        verificator.add_change_password_request(email, "new_hash123")
    result = verificator.exists_change_password_request(email)
    assert result == expected_result


@pytest.mark.parametrize(
    "email, expected_result",
    [
        ("test@example.com", True),
        ("nonexistent@example.com", False),
    ],
)
def test_exists_delete_account_request(verificator, email, expected_result):
    if email == "test@example.com":
        verificator.add_delete_account_request(email)
    result = verificator.exists_delete_account_request(email)
    assert result == expected_result


@pytest.mark.parametrize(
    "setup_requests, expected_counts",
    [
        (
            {
                "registration": ["test1@example.com"],
                "change_password": ["test2@example.com"],
                "delete_account": ["test4@example.com"],
            },
            {
                "registration": 0,
                "change_password": 0,
                "delete_account": 0,
            },
        ),
        (
            {
                "registration": ["test1@example.com", "test2@example.com"],
                "change_password": [],
                "delete_account": [],
            },
            {
                "registration": 0,
                "change_password": 0,
                "delete_account": 0,
            },
        ),
    ],
)
def test_remove_expired_requests(verificator, setup_requests, expected_counts):
    for email in setup_requests["registration"]:
        verificator.add_registration_request(email, "test_user", "hash123", "user")
    for email in setup_requests["change_password"]:
        verificator.add_change_password_request(email, "new_hash123")
    for email in setup_requests["delete_account"]:
        verificator.add_delete_account_request(email)

    # Manually set the timestamp to be more than 5 minutes ago
    for requests in [
        verificator.registration_requests,
        verificator.change_password_requests,
        verificator.delete_account_requests,
    ]:
        for request in requests.values():
            request["timestamp"] = datetime.datetime.now() - datetime.timedelta(
                minutes=6
            )

    verificator.remove_expired_requests()

    assert len(verificator.registration_requests) == expected_counts["registration"]
    assert (
        len(verificator.change_password_requests) == expected_counts["change_password"]
    )
    assert len(verificator.delete_account_requests) == expected_counts["delete_account"]


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
