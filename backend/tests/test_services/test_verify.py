from src.services.verify import Verificator
import src.errors as errors
from datetime import datetime, timedelta
import pytest
import time

def test_singleton(verificator):
    assert Verificator() is verificator

@pytest.mark.parametrize("req_type, email, kwargs, expected_type", [
    (Verificator.REGISTRATION, "test@example.com", {"username": "testuser", "password_hash": "hashed_password", "role": "user"}, Verificator.REGISTRATION),
    (Verificator.CHANGE_PASSWORD, "test@example.com", {"new_password": "new_password", "id": 1}, Verificator.CHANGE_PASSWORD),
    (Verificator.DELETE_ACCOUNT, "test@example.com", {"id": 1}, Verificator.DELETE_ACCOUNT),
])
def test_add_verification_request(verificator, req_type, email, kwargs, expected_type):
    code = verificator.add_verification_request(req_type, email, **kwargs)
    assert len(code) == 6
    assert email in verificator.requests
    assert verificator.requests[email]["type"] == expected_type

@pytest.mark.parametrize("req_type, email, kwargs, exception", [
    (4, "test@example.com", {}, errors.VerificationError),
    (Verificator.REGISTRATION, "test@example.com", {}, errors.MissingFieldError),
    (Verificator.REGISTRATION, "", {"username": "testuser", "password_hash": "hashed_password", "role": "user"}, errors.MissingFieldError),
])
def test_add_verification_request_errors(verificator, req_type, email, kwargs, exception):
    with pytest.raises(exception):
        verificator.add_verification_request(req_type, email, **kwargs)

def test_add_verification_request_duplicate_email(verificator):
    verificator.add_verification_request(
        Verificator.REGISTRATION,
        "test@example.com",
        username="testuser",
        password_hash="hashed_password",
        role="user"
    )
    with pytest.raises(errors.VerificationError):
        verificator.add_verification_request(
            Verificator.CHANGE_PASSWORD,
            "test@example.com",
            new_password="new_password",
            id=1
        )

@pytest.mark.parametrize("email, req_type, expected", [
    ("test@example.com", Verificator.REGISTRATION, True),
    ("test@example.com", Verificator.CHANGE_PASSWORD, False),
    ("other@example.com", Verificator.REGISTRATION, False),
])
def test_contains_request(verificator, email, req_type, expected):
    verificator.add_verification_request(
        Verificator.REGISTRATION,
        "test@example.com",
        username="testuser",
        password_hash="hashed_password",
        role="user"
    )
    assert verificator.contains_request(email, req_type) == expected

def test_remove_expired_requests(verificator):
    verificator.add_verification_request(
        Verificator.REGISTRATION,
        "test1@example.com",
        username="testuser1",
        password_hash="hashed_password1",
        role="user"
    )
    verificator.requests["test1@example.com"]["timestamp"] = datetime.now() - timedelta(minutes=6)
    
    verificator.add_verification_request(
        Verificator.REGISTRATION,
        "test2@example.com",
        username="testuser2",
        password_hash="hashed_password2",
        role="user"
    )
    
    verificator.remove_expired_requests()
    
    assert "test1@example.com" not in verificator.requests
    assert "test2@example.com" in verificator.requests

@pytest.mark.parametrize("_", range(5))  # Run this test 5 times
def test_generate_verification_code(verificator, _):
    code = verificator.generate_verification_code()
    assert len(code) == 6
    assert code.isdigit()
    assert 100000 <= int(code) <= 999999

def test_remove_expired_requests_loop(verificator):
    verificator.add_verification_request(
        Verificator.REGISTRATION,
        "test@example.com",
        username="testuser",
        password_hash="hashed_password",
        role="user"
    )
    verificator.requests["test@example.com"]["timestamp"] = datetime.now() - timedelta(minutes=6)
    
    time.sleep(11)  # Wait for the loop to run
    
    assert "test@example.com" not in verificator.requests