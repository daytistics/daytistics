import pytest
from unittest import mock
import src.services.verify as verify
import src.models.users as users
import src.errors as errors
import src.utils.encryption as encryption


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
def test_exists_registration_request(app, client, verificator, email, value, status_code):

    def mock_generate_verification_code():
        return "123456"

    with mock.patch.object(
        verify,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):
        
        
        with app.app_context():
            import src.api.routes as routes
    
            verificator.generate_verification_code = mock_generate_verification_code

            verificator.add_registration_request("test@example.com", "test", "password", "user")

            response = client.post(routes.EXISTS_REGISTRATION_REQUEST_ROUTE, json={"email": email})

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
def test_exists_change_password_request(app, client, verificator, email, value, status_code):

    def mock_generate_verification_code():
        return "123456"

    with mock.patch.object(
        verify,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):

        with app.app_context():
            import src.api.routes as routes

            verificator.generate_verification_code = mock_generate_verification_code    

            verificator.add_change_password_request("test@example.com", "password")

            response = client.post(routes.EXISTS_CHANGE_PASSWORD_REQUEST_ROUTE, json={"email": email})

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
def test_exists_delete_account_request(app, client, verificator, email, value, status_code):

    def mock_generate_verification_code():
        return "123456"

    with mock.patch.object(
        verify,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):

        with app.app_context():
            import src.api.routes as routes

            verificator.add_delete_account_request("test@example.com")

            response = client.post(routes.EXISTS_DELETE_ACCOUNT_REQUEST_ROUTE, json={"email": email})

            assert response.status_code == status_code
            assert response.json == value


            if value.get("exists") == True:
                assert verificator.delete_account_requests.get(email) is not None
                assert verificator.delete_account_requests.get(email).get("email") == email
                assert verificator.delete_account_requests.get(email).get("code") == "123456"


@pytest.mark.parametrize("email, code, value, status_code",  [
    ("test@example.com", "123456", {"message": "Verified registration request"}, 200),
    ("   ", "123456", {"error": "Invalid input data"}, 400),
    ("", "123456", {"error": "Invalid input data"}, 400),
    ("test@example.com", "    ", {"error": "Invalid input data"}, 400),
    ("test@example.com", "", {"error": "Invalid input data"}, 400),
    ("test@example.com", None, {"error": "Invalid input data"}, 400),
    (None, "123456", {"error": "Invalid input data"}, 400),
    ("test", "123456", {"error": "Invalid email"}, 400),
    ("test@", "123456", {"error": "Invalid email"}, 400),
    ("test@example", "123456", {"error": "Invalid email"}, 400),
    ("test@example", "123456", {"error": "Invalid email"}, 400),
    ("test@example.com", "123 456", {"error": "Invalid code format"}, 400),
    ("test@example.com", "1234", {"error": "Invalid code format"}, 400),
    ("test@example.com", "12345f", {"error": "Invalid code format"}, 400),
    ("notfound@example.com", "123456", {"error": "No registration request found for this email"}, 404),
    ("test@example.com", "321341", {"error": "Invalid code"}, 400)
])
def test_verify_registration_request(app, client, verificator, email, code, value, status_code):

    def mock_generate_verification_code():
        return "123456"

    with mock.patch.object(
        verify,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):
        
        with app.app_context():
            import src.api.routes as routes
    
            verificator.add_registration_request("test@example.com", "test", "password", "user")

            response = client.post(routes.VERIFY_REGISTRATION_REQUEST_ROUTE, json={"email": email, "code": code})

            assert response.status_code == status_code
            assert response.json == value

            if status_code == 200:
                assert verificator.registration_requests.get(email) is None
                assert users.get_user_by_email(email) is not None
                assert users.get_user_by_email(email).username == "test"
                assert users.get_user_by_email(email).email == email
                assert users.get_user_by_email(email).role == "user"
                assert users.get_user_by_email(email).password_hash == "password"
                

@pytest.mark.parametrize("email, code, value, status_code",  [
    ("test@example.com", "123456", {"message": "Verified change password request"}, 200),
    ("   ", "123456", {"error": "Invalid input data"}, 400),
    ("", "123456", {"error": "Invalid input data"}, 400),
    ("test@example.com", "    ", {"error": "Invalid input data"}, 400),
    ("test@example.com", "", {"error": "Invalid input data"}, 400),
    ("test@example.com", None, {"error": "Invalid input data"}, 400),
    (None, "123456", {"error": "Invalid input data"}, 400),
    ("test", "123456", {"error": "Invalid email"}, 400),
    ("test@", "123456", {"error": "Invalid email"}, 400),
    ("test@example", "123456", {"error": "Invalid email"}, 400),
    ("test@example", "123456", {"error": "Invalid email"}, 400),
    ("test@example.com", "123 456", {"error": "Invalid code format"}, 400),
    ("test@example.com", "1234", {"error": "Invalid code format"}, 400),
    ("test@example.com", "12345f", {"error": "Invalid code format"}, 400),
    ("notfound@example.com", "123456", {"error": "No change password request found for this email"}, 404),
    ("test@example.com", "321341", {"error": "Invalid code"}, 400)
])
def test_verify_change_password_request(app, db, client, verificator, email, code, value, status_code):

    def mock_generate_verification_code():
        return "123456"

    with mock.patch.object(
        verify,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):
        
        with app.app_context():
            import src.api.routes as routes


        
            user = users.User(username="test", email="test@example.com", password_hash="password", role="user")
            db.session.add(user)
            db.session.commit()
        
            verificator.add_change_password_request("test@example.com", "test2")

            response = client.post(routes.VERIFY_CHANGE_PASSWORD_REQUEST_ROUTE, json={"email": email, "code": code})

            assert response.status_code == status_code
            assert response.json == value

            if status_code == 200:
                assert verificator.registration_requests.get(email) is None
                assert users.get_user_by_email(email) is not None
                assert users.get_user_by_email(email).username == "test"
                assert users.get_user_by_email(email).email == email
                assert users.get_user_by_email(email).role == "user"
                assert users.get_user_by_email(email).password_hash == "test2"


@pytest.mark.parametrize("email, code, value, status_code",  [
    ("test@example.com", "123456", {"message": "Verified delete account request"}, 200),
    ("   ", "123456", {"error": "Invalid input data"}, 400),
    ("", "123456", {"error": "Invalid input data"}, 400),
    ("test@example.com", "    ", {"error": "Invalid input data"}, 400),
    ("test@example.com", "", {"error": "Invalid input data"}, 400),
    ("test@example.com", None, {"error": "Invalid input data"}, 400),
    (None, "123456", {"error": "Invalid input data"}, 400),
    ("test", "123456", {"error": "Invalid email"}, 400),
    ("test@", "123456", {"error": "Invalid email"}, 400),
    ("test@example", "123456", {"error": "Invalid email"}, 400),
    ("test@example", "123456", {"error": "Invalid email"}, 400),
    ("test@example.com", "123 456", {"error": "Invalid code format"}, 400),
    ("test@example.com", "1234", {"error": "Invalid code format"}, 400),
    ("test@example.com", "12345f", {"error": "Invalid code format"}, 400),
    ("notfound@example.com", "123456", {"error": "No delete account request found for this email"}, 404),
    ("test@example.com", "321341", {"error": "Invalid code"}, 400)
])
def test_verify_delete_account_request(app, db, client, verificator, email, code, value, status_code):

    def mock_generate_verification_code():
        return "123456"

    with mock.patch.object(
        verify,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):
        
        with app.app_context():
            import src.api.routes as routes


        
            user = users.User(username="test", email="test@example.com", password_hash="password", role="user")
            db.session.add(user)
            db.session.commit()
        
            verificator.add_delete_account_request("test@example.com")

            response = client.post(routes.VERIFY_DELETE_ACCOUNT_REQUEST_ROUTE, json={"email": email, "code": code})

            assert response.status_code == status_code
            assert response.json == value

            if status_code == 200:
                assert verificator.registration_requests.get(email) is None

                with pytest.raises(errors.UserNotFoundError):
                    users.get_user_by_email(email)

@pytest.mark.parametrize("email, password, username, value, status_code",  [
    ("test@example.com", "TollesPasswort123!", "test", {"message": "Registration request sent"}, 200),
    ("   ", "TollesPasswort123!", "test", {"error": "Missing or invalid input data"}, 400),
    ("", "TollesPasswort123!", "test", {"error": "Missing or invalid input data"}, 400),
    (None, "TollesPasswort123!", "test", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", "", "test", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", "   ", "test", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", None, "test", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", "TollesPasswort123!", "", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", "TollesPasswort123!", "   ", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", "TollesPasswort123!", None, {"error": "Missing or invalid input data"}, 400),
    ("test", "TollesPasswort123!", "test", {"error": "Invalid email"}, 400),
    ("test@", "TollesPasswort123!", "test", {"error": "Invalid email"}, 400),
    ("test@example", "TollesPasswort123!", "test", {"error": "Invalid email"}, 400),
    ("test@example.", "TollesPasswort123!", "test", {"error": "Invalid email"}, 400),
    ("test@example.c", "TollesPasswort123!", "test", {"error": "Invalid email"}, 400),
    ("test.com", "TollesPasswort123!", "test", {"error": "Invalid email"}, 400),
    ("alreadyinverificator@example.com", "TollesPasswort123!", "test", {"error": "Registration request already exists"}, 409),
    ("alreadyregistered@example.com", "TollesPasswort123!", "test", {"error": "Email already in use"}, 409),
    ("test@example.com", "TollesPasswort123!", "te", {"error": "Invalid username"}, 400),
    ("test@example.com", "TollesPasswort123!", "test!§", {"error": "Invalid username"}, 400),
    ("test@example.com", "TollesPasswort123!", "test ", {"error": "Invalid username"}, 400),
    ("test@example.com", "TollesPasswort123!", "teniuasdhjashdojashdkjahskdjhaskjdhakjshdkjahs", {"error": "Invalid username"}, 400),
    ("test@example.com", "TollesPasswort123", "test", {"error": "Bad password"}, 400),
    ("test@example.com", "TollesPasswort!", "test", {"error": "Bad password"}, 400),
    ("test@example.com", "tollespasswort123!", "test", {"error": "Bad password"}, 400),
    ("test@example.com", "TOLLESPASSWORT123!", "test", {"error": "Bad password"}, 400),
])
def test_user_registration(client, app, db, verificator, email, password, username, value, status_code):
    with app.app_context():
        import src.api.routes as routes

        verificator.add_registration_request("alreadyinverificator@example.com", "test", "password", "user")

        user = users.User(username="alreadyregistered", email="alreadyregistered@example.com", password_hash="password", role="user")
        db.session.add(user)
        db.session.commit()

        response = client.post(routes.USER_REGISTRATION_ROUTE, json={"username": username, "email": email, "password": password})

        assert response.status_code == status_code
        assert response.json == value

        if status_code == 200:
            assert verificator.registration_requests.get(email) is not None
            assert verificator.registration_requests.get(email).get("email") == email
            assert verificator.registration_requests.get(email).get("username") == username
            assert encryption.check_hashed_value(password, verificator.registration_requests.get(email).get("password_hash")) == True
            assert verificator.registration_requests.get(email).get("role") == "user"
            assert verificator.registration_requests.get(email).get("code") is not None
            assert verificator.exists_registration_request(email) == True
            
            with pytest.raises(errors.UserNotFoundError):
                users.get_user_by_email(email)

