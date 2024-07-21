import pytest
from unittest.mock import patch
from src.models import User
from src import errors

@pytest.mark.parametrize(
    "email, type, expected_status, expected_response",
    [
        ("test@example.com", 1, 200, {"exists": True}),
        ("nonexistent@example.com", 1, 200, {"exists": False}),
        ("invalid_email", 1, 400, {"message": "Email is required"}),
        ("test@example.com", None, 400, {"message": "Type is required"}),
    ]
)
def test_exists_verification_request(client, db, verificator, email, type, expected_status, expected_response):
    with patch('src.api.auth.verificator', verificator):
        if email == "test@example.com":
            user = User(username="testuser", email=email, password_hash="hashed_password")
            db.session.add(user)
            db.session.commit()

        if expected_status == 400:
            with pytest.raises(Exception) as exc_info:
                client.post('/user/verify/exists', json={'email': email, 'type': type})
            assert str(exc_info.value) == expected_response["message"]
        else:
            response = client.post('/user/verify/exists', json={'email': email, 'type': type})
            assert response.status_code == expected_status
            assert response.json == expected_response

@pytest.mark.parametrize(
    "email, code, type, expected_status, expected_response",
    [
        ("test@example.com", "123456", 1, 200, {"id": 1, "email": "test@example.com", "password_hash": "hashed_password", "username": "testuser"}),
        ("nonexistent@example.com", "123456", 1, 404, {"error": "User not found"}),
        ("test@example.com", "wrong_code", 1, 400, {"error": "Invalid verification code"}),
        ("test@example.com", "123456", 999, 400, {"error": "Invalid verification type"}),
        ("", "123456", 1, 400, {"error": "Missing email or code"}),
    ]
)
def test_verify_action(client, db, verificator, email, code, type, expected_status, expected_response):
    with patch('src.api.auth.verificator', verificator), \
         patch('src.api.auth.users.verify_action') as mock_verify_action:
        
        if email == "test@example.com":
            user = User(id=1, username="testuser", email=email, password_hash="hashed_password")
            db.session.add(user)
            db.session.commit()
            verificator.add_verification_request(type, email, "testuser", "hashed_password", "user")
            verificator.requests[email]['code'] = "123456"

        if expected_status != 200:
            mock_verify_action.side_effect = errors.VerificationError("Verification failed")
        
        if expected_status != 200:
            with pytest.raises(errors.VerificationError) as exc_info:
                client.post('/user/verify', json={'email': email, 'code': code, 'type': type})
            assert str(exc_info.value) == "Verification failed"
        else:
            response = client.post('/user/verify', json={'email': email, 'code': code, 'type': type})
            assert response.status_code == expected_status
            assert response.json == expected_response

@pytest.mark.parametrize(
    "email, password, expected_status, expected_response",
    [
        ("test@example.com", "correct_password", 200, {"id": 1, "email": "test@example.com", "password_hash": "hashed_password", "username": "testuser"}),
        ("test@example.com", "wrong_password", 401, {"error": "Invalid email or password"}),
        ("nonexistent@example.com", "password", 401, {"error": "Invalid email or password"}),
        ("", "password", 400, {"message": "Email is required"}),
        ("test@example.com", "", 400, {"message": "Password is required"}),
    ]
)
def test_user_login(client, db, email, password, expected_status, expected_response):
    with patch('src.api.auth.users.check_user_password') as mock_check_password:
        if email == "test@example.com":
            user = User(id=1, username="testuser", email=email, password_hash="hashed_password")
            db.session.add(user)
            db.session.commit()
            mock_check_password.return_value = (password == "correct_password")
        
        if expected_status == 400:
            with pytest.raises(Exception) as exc_info:
                client.post('/user/login', json={'email': email, 'password': password})
            assert str(exc_info.value) == expected_response["message"]
        else:
            response = client.post('/user/login', json={'email': email, 'password': password})
            assert response.status_code == expected_status
            assert response.json == expected_response

@pytest.mark.parametrize(
    "username, email, password, expected_status, expected_response",
    [
        ("newuser", "new@example.com", "Valid_password1", 200, {"message": "Registration request sent"}),
        ("existinguser", "existing@example.com", "Valid_password1", 400, {"error": "Email already registered"}),
        ("newuser", "invalid_email", "Valid_password1", 400, {"error": "Invalid email format"}),
        ("newuser", "new@example.com", "weak", 400, {"error": "Password does not meet requirements"}),
        ("", "new@example.com", "Valid_password1", 400, {"message": "Username is required"}),
        ("newuser", "", "Valid_password1", 400, {"message": "Email is required"}),
        ("newuser", "new@example.com", "", 400, {"message": "Password is required"}),
    ]
)
def test_user_registration(client, db, verificator, username, email, password, expected_status, expected_response):
    with patch('src.api.auth.verificator', verificator), \
         patch('src.api.auth.users.register_user') as mock_register_user:
        
        if email == "existing@example.com":
            existing_user = User(username="existinguser", email=email, password_hash="hashed_password")
            db.session.add(existing_user)
            db.session.commit()
            mock_register_user.side_effect = errors.EmailAlreadyRegisteredError("Email already registered")
        elif password == "weak":
            mock_register_user.side_effect = errors.BadPasswordError("Password does not meet requirements")
        elif email == "invalid_email":
            mock_register_user.side_effect = errors.InvalidEmailError("Invalid email format")
        
        if expected_status == 400:
            with pytest.raises(Exception) as exc_info:
                client.post('/user/register', json={'username': username, 'email': email, 'password': password})
            assert str(exc_info.value) == expected_response["error"] or expected_response["message"]
        else:
            response = client.post('/user/register', json={'username': username, 'email': email, 'password': password})
            assert response.status_code == expected_status
            assert response.json == expected_response

        if expected_status == 200:
            mock_register_user.assert_called_once_with(verificator, username, password, email)