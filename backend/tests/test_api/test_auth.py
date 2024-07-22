import pytest
from unittest import mock
import src.services.verify as verify

@pytest.mark.parametrize("email, value, status_code",  [
    ("test@example.com", {"exists": True}, 200),
    ("testy@example.com", {"exists": False}, 200),
    ("", {"error": "Missing or invalid email"}, 400),
    ("    ", {"error": "Missing or invalid email"}, 400),
    ("test", {"error": "Invalid email"}, 400),
    ("test@", {"error": "Invalid email"}, 400),
    ("test@example", {"error": "Invalid email"}, 400),
    ("test@example.", {"error": "Invalid email"}, 400),
    ("test@example.c", {"error": "Invalid email"}, 400),
])
def test_exists_registration_request(client, verificator, email, value, status_code):

    def mock_generate_verification_code():
        return "123456"

    with mock.patch.object(
        verify,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):
    
        verificator.generate_verification_code = mock_generate_verification_code

        verificator.add_registration_request("test@example.com", "test", "password", "user")

        response = client.post("/user/verify/registration/exists", json={"email": email})

        assert response.status_code == status_code
        assert response.json == value


        if value.get("exists") == True:
            assert verificator.registration_requests.get(email) is not None
            assert verificator.registration_requests.get(email).get("email") == email
            assert verificator.registration_requests.get(email).get("username") == "test"
            assert verificator.registration_requests.get(email).get("password_hash") == "password"
            assert verificator.registration_requests.get(email).get("role") == "user"
            assert verificator.registration_requests.get(email).get("code") == "123456"

@pytest.mark.parametrize("email, value, status_code",  [
    ("test@example.com", {"exists": True}, 200),
    ("testy@example.com", {"exists": False}, 200),
    ("", {"error": "Missing or invalid email"}, 400),
    ("    ", {"error": "Missing or invalid email"}, 400),
    ("test", {"error": "Invalid email"}, 400),
    ("test@", {"error": "Invalid email"}, 400),
    ("test@example", {"error": "Invalid email"}, 400),
    ("test@example.", {"error": "Invalid email"}, 400),
    ("test@example.c", {"error": "Invalid email"}, 400),
])
def test_exists_change_password_request(client, verificator, email, value, status_code):

    def mock_generate_verification_code():
        return "123456"

    with mock.patch.object(
        verify,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):

        verificator.generate_verification_code = mock_generate_verification_code    

        verificator.add_change_password_request("test@example.com", "password")

        response = client.post("/user/verify/change_password/exists", json={"email": email})

        assert response.status_code == status_code
        assert response.json == value


        if value.get("exists") == True:
            assert verificator.change_password_requests.get(email) is not None
            assert verificator.change_password_requests.get(email).get("email") == email
            assert verificator.change_password_requests.get(email).get("new_password") == "password"
            assert verificator.change_password_requests.get(email).get("code") == "123456"
        
@pytest.mark.parametrize("email, value, status_code",  [
    ("test@example.com", {"exists": True}, 200),
    ("testy@example.com", {"exists": False}, 200),
    ("", {"error": "Missing or invalid email"}, 400),
    ("    ", {"error": "Missing or invalid email"}, 400),
    ("test", {"error": "Invalid email"}, 400),
    ("test@", {"error": "Invalid email"}, 400),
    ("test@example", {"error": "Invalid email"}, 400),
    ("test@example.", {"error": "Invalid email"}, 400),
    ("test@example.c", {"error": "Invalid email"}, 400),
])
def test_exists_delete_account_request(client, verificator, email, value, status_code):

    def mock_generate_verification_code():
        return "123456"

    with mock.patch.object(
        verify,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):


        verificator.add_delete_account_request("test@example.com")

        response = client.post("/user/verify/delete_account/exists", json={"email": email})

        assert response.status_code == status_code
        assert response.json == value


        if value.get("exists") == True:
            assert verificator.delete_account_requests.get(email) is not None
            assert verificator.delete_account_requests.get(email).get("email") == email
            assert verificator.delete_account_requests.get(email).get("code") == "123456"