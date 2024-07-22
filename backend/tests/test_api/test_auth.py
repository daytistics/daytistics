import pytest
import time
import unittest.mock as mock
from src.models import User

@pytest.mark.parametrize("email, type, expected, status, in_verificator", [
    ("test@example.com", 1, {"exists": True}, 200, True),
    ("test@example.com", 2, {"exists": True}, 200, True),
    ("test@example.com", 3, {"exists": True}, 200, True),
    ("test@example.com", 1, {"exists": False}, 200, False),
    ("test@example.com", 2, {"exists": False}, 200, False),
    ("test@example.com", 3, {"exists": False}, 200, False),
    ("testxample.com", 1, {"error": "Missing or invalid email"}, 400, False),
    ("test@com", 1, {"error": "Missing or invalid email"}, 400, False),
    ("", 1, {"error": "Missing or invalid email"}, 400, False),
    (None, 1, {"error": "Missing or invalid email"}, 400, False),
    ("test@example.com", 0, {"error": "Invalid type"}, 400, False),
    ("test@example.com", 5, {"error": "Invalid type"}, 400, False),
    ("test@example.com", None, {"error": "Invalid type"}, 400, False),
])
def test_exists_verification_request_post(app, db, client, verificator, email, type, expected, status, in_verificator):

    if in_verificator:
        match type:
            case 1:
                verificator.add_verification_request(type, email, username="test", password_hash="test", role="user")
            case 2:
                verificator.add_verification_request(type, email, new_password="test", id=1)
            case 3:
                verificator.add_verification_request(type, email, id=1)
        time.sleep(1)  # Simulating delay for the verification request to be processed

    response = client.post("/user/verify/exists", json={"email": email, "type": type})

    assert response.status_code == status, f"Expected status code {status} but got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", f"Expected Content-Type 'application/json' but got {response.headers['Content-Type']}"

    if status == 200:
        assert response.json["exists"] == expected["exists"], f"Expected {expected} but got {response.json}"
    else:
        assert response.json["error"] == expected["error"], f"Expected {expected} but got {response.json}"

