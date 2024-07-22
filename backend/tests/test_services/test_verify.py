from src.services.verify import Verificator, generate_verification_code
import src.errors as errors
from datetime import datetime, timedelta
import pytest
import time

def test_singleton(verificator):
    assert Verificator() is verificator

def test_generate_verification_code():
    code = generate_verification_code()
    assert 100000 <= int(code) <= 999999

@pytest.mark.parametrize("email, username, password_hash, role", [
    ("test@example.com", "testuser", "hashedpassword", "user"),
])
def test_add_registration_request(verificator, email, username, password_hash, role):
    code = verificator.add_registration_request(email, username, password_hash, role)
    assert email in verificator.registration_requests
    assert verificator.registration_requests[email]["username"] == username
    assert verificator.registration_requests[email]["password_hash"] == password_hash
    assert verificator.registration_requests[email]["role"] == role
    assert verificator.registration_requests[email]["code"] == code

@pytest.mark.parametrize("email, username, password_hash, role", [
    (None, "testuser", "hashedpassword", "user"),
    ("", "testuser", "hashedpassword", "user"),
])
def test_add_registration_request_missing_field(verificator, email, username, password_hash, role):
    with pytest.raises(errors.MissingFieldError):
        verificator.add_registration_request(email, username, password_hash, role)

def test_add_registration_request_duplicate(verificator):
    email = "test@example.com"
    verificator.add_registration_request(email, "testuser", "hashedpassword", "user")
    with pytest.raises(errors.VerificationError):
        verificator.add_registration_request(email, "testuser", "hashedpassword", "user")

@pytest.mark.parametrize("email, new_password", [
    ("test@example.com", "newhashedpassword"),
])
def test_add_change_password_request(verificator, email, new_password):
    code = verificator.add_change_password_request(email, new_password)
    assert email in verificator.change_password_requests
    assert verificator.change_password_requests[email]["new_password"] == new_password
    assert verificator.change_password_requests[email]["code"] == code

@pytest.mark.parametrize("email, new_password", [
    (None, "newhashedpassword"),
    ("", "newhashedpassword"),
])
def test_add_change_password_request_missing_field(verificator, email, new_password):
    with pytest.raises(errors.MissingFieldError):
        verificator.add_change_password_request(email, new_password)

def test_add_change_password_request_duplicate(verificator):
    email = "test@example.com"
    verificator.add_change_password_request(email, "newhashedpassword")
    with pytest.raises(errors.VerificationError):
        verificator.add_change_password_request(email, "newhashedpassword")

@pytest.mark.parametrize("email", [
    ("test@example.com"),
])
def test_add_reset_password_request(verificator, email):
    code = verificator.add_reset_password_request(email)
    assert email in verificator.reset_password_requests
    assert verificator.reset_password_requests[email]["code"] == code

@pytest.mark.parametrize("email", [
    (None),
    (""),
])
def test_add_reset_password_request_missing_field(verificator, email):
    with pytest.raises(errors.MissingFieldError):
        verificator.add_reset_password_request(email)

def test_add_reset_password_request_duplicate(verificator):
    email = "test@example.com"
    verificator.add_reset_password_request(email)
    with pytest.raises(errors.VerificationError):
        verificator.add_reset_password_request(email)

@pytest.mark.parametrize("email", [
    ("test@example.com"),
])
def test_add_delete_account_request(verificator, email):
    code = verificator.add_delete_account_request(email)
    assert email in verificator.delete_account_requests
    assert verificator.delete_account_requests[email]["code"] == code

@pytest.mark.parametrize("email", [
    (None),
    (""),
])
def test_add_delete_account_request_missing_field(verificator, email):
    with pytest.raises(errors.MissingFieldError):
        verificator.add_delete_account_request(email)

def test_add_delete_account_request_duplicate(verificator):
    email = "test@example.com"
    verificator.add_delete_account_request(email)
    with pytest.raises(errors.VerificationError):
        verificator.add_delete_account_request(email)