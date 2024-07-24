import pytest
from unittest import mock
import core.services.verification as verification
import core.models.users as users
import core.errors as errors
import core.utils.encryption as encryption
from flask_jwt_extended import create_access_token, create_refresh_token
from core.utils.encryption import generate_password_hash

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
        verification,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):
        
        
        with app.app_context():
            import core.utils.routes as routes
    
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
        verification,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):

        with app.app_context():
            import core.utils.routes as routes

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
        verification,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):

        with app.app_context():
            import core.utils.routes as routes

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
        verification,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):
        
        with app.app_context():
            import core.utils.routes as routes
    
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
        verification,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):
        
        with app.app_context():
            import core.utils.routes as routes


        
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
        verification,
        "generate_verification_code",
        side_effect=mock_generate_verification_code,
    ):
        
        with app.app_context():
            import core.utils.routes as routes


        
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
        import core.utils.routes as routes

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


@pytest.mark.parametrize("email, password, value, status_code",  [
    ("test@example.com", "TollesPasswort123!", {"access_token": "mocked_access_token", "refresh_token": "mocked_refresh_token"}, 200),
    ("  ", "TollesPasswort123!", {"error": "Missing or invalid input data"}, 400),
    ("", "TollesPasswort123!", {"error": "Missing or invalid input data"}, 400),
    (None, "TollesPasswort123!", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", "", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", "  ", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", None, {"error": "Missing or invalid input data"}, 400),
    ("test", "TollesPasswort123!", {"error": "Invalid email"}, 400),
    ("test@", "TollesPasswort123!", {"error": "Invalid email"}, 400),
    ("test@example", "TollesPasswort123!", {"error": "Invalid email"}, 400),
    ("test@example.", "TollesPasswort123!", {"error": "Invalid email"}, 400),
    ("test@example.c", "TollesPasswort123!", {"error": "Invalid email"}, 400),
    ("test.com", "TollesPasswort123!", {"error": "Invalid email"}, 400),
    ("testy@example.com", "TollesPasswort123!", {"error": "User not found"}, 404),
    ("test@example.com", "TollesPasswort123?", {"error": "Invalid password"}, 401),
])
def test_user_login(client, app, db, email, password, value, status_code):
    def mock_create_access_token(identity):
        return "mocked_access_token"
    
    def mock_create_refresh_token(identity):
        return "mocked_refresh_token"

    def mock_check_hashed_value(value, hashed_value):
        return value == "TollesPasswort123!"

    def mock_decode_token(token):
        return {"sub": "test@example.com"}

    with mock.patch("core.api.auth.create_access_token", side_effect=mock_create_access_token):
        with mock.patch("core.models.users.check_hashed_value", side_effect=mock_check_hashed_value):
            with mock.patch("core.api.auth.decode_token", side_effect=mock_decode_token):
                with mock.patch("core.api.auth.create_refresh_token", side_effect=mock_create_refresh_token):
                    with app.app_context():
                        import core.utils.routes as routes

                        user = users.User(username="test", email="test@example.com", password_hash="TollesPassword123!", role="user")
                        db.session.add(user)
                        db.session.commit()

                        response = client.post(routes.USER_LOGIN_ROUTE, json={"email": email, "password": password})

                        assert response.status_code == status_code
                        assert response is not None
                        assert response.json == value

                        if status_code == 200:
                            assert response.json["access_token"] is not None
                            assert mock_decode_token(response.json["access_token"])["sub"] == "test@example.com"
                            assert response.json["refresh_token"] is not None
                            assert mock_decode_token(response.json["refresh_token"])["sub"] == "test@example.com"




def test_token_refresh(client, refresh_token):
    # Anfrage an den TokenRefresh-Endpunkt senden
    
    preset_refresh_token = create_refresh_token(identity="test@example.com")

    response = client.post('/user/token/refresh', headers={'Authorization': f'Bearer {preset_refresh_token}'})

    assert response.status_code == 200
    assert response.json is not None

    assert response.json.get("access_token") is not None
    assert response.json.get("access_token") != preset_refresh_token

def test_token_email(client):
    # Anfrage an den TokenEmail-Endpunkt senden
    preset_refresh_token = create_access_token(identity="test@example.com")

    response = client.get('/user/token/email', headers={'Authorization': f'Bearer {preset_refresh_token}'})

    assert response.status_code == 200
    assert response.json is not None
    assert response.json.get("email") == "test@example.com"

@pytest.mark.parametrize("email, new_username, value, status_code",  [
    ("test@example.com", "newusername", {"message": "Username changed successfully"}, 200),
    ("   ", "newusername", {"error": "Missing or invalid input data"}, 400),
    ("", "newusername", {"error": "Missing or invalid input data"}, 400),
    (None, "newusername", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", "", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", "  ", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", None, {"error": "Missing or invalid input data"}, 400),
    ("test", "newusername", {"error": "Invalid email"}, 400),
    ("test@", "newusername", {"error": "Invalid email"}, 400),
    ("test@example", "newusername", {"error": "Invalid email"}, 400),
    ("test@example.", "newusername", {"error": "Invalid email"}, 400),
    ("test@example.c", "newusername", {"error": "Invalid email"}, 400),
    ("test.com", "newusername", {"error": "Invalid email"}, 400),
    ("test@example.com", "Hallo[]", {"error": "Invalid username"}, 400),
    ("test@example.com", "Hallo ", {"error": "Invalid username"}, 400),
])
def test_change_username(client, app, db, email, new_username, value, status_code):
    user = users.User(username="test", email="test@example.com")
    db.session.add(user)
    db.session.commit()

    with app.app_context():
        import core.utils.routes as routes

        response = client.post(routes.CHANGE_USERNAME_ROUTE, json={"email": email, "new_username": new_username})

        assert response.status_code == status_code
        assert response.json == value

        if status_code == 200:
            assert users.get_user_by_email(email).username == new_username

@pytest.mark.parametrize("email, new_password, value, status_code",  [
    ("test@example.com", "TollesPasswort123!", {"message": "Change password request sent"}, 200),
    ("   ", "TollesPasswort123!", {"error": "Missing or invalid input data"}, 400),
    ("", "TollesPasswort123!", {"error": "Missing or invalid input data"}, 400),
    (None, "TollesPasswort123!", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", "", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", "  ", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", None, {"error": "Missing or invalid input data"}, 400),
    ("test", "TollesPasswort123!", {"error": "Invalid email"}, 400),
    ("test@", "TollesPasswort123!", {"error": "Invalid email"}, 400),
    ("test@example", "TollesPasswort123!", {"error": "Invalid email"}, 400),
    ("test@example.", "TollesPasswort123!", {"error": "Invalid email"}, 400),
    ("test@example.c", "TollesPasswort123!", {"error": "Invalid email"}, 400),
    ("test.com", "TollesPasswort123!", {"error": "Invalid email"}, 400),
    ("testy@example.com", "TollesPasswort123!", {"error": "User not found"}, 404),
    ("alreadyinverificator@example.com", "TollesPasswort123!", {"error": "Change password request already exists"}, 409),
    ("test@example.com", "TollesPasswort123", {"error": "Bad password"}, 400),
    ("test@example.com", "tollespasswort123!", {"error": "Bad password"}, 400),
    ("test@example.com", "TOLLESPASSWORT123!", {"error": "Bad password"}, 400)
])
def test_user_change_password(client, app, db, verificator, email, new_password, value, status_code):
    with app.app_context():
        import core.utils.routes as routes

        user = users.User(username="test", email="test@example.com", password_hash="password", role="user")
        db.session.add(user)
        db.session.commit()

        user = users.User(username="test", email="alreadyinverificator@example.com", password_hash="password", role="user")
        db.session.add(user)
        db.session.commit()

        verificator.add_change_password_request("alreadyinverificator@example.com", "password")

        response = client.post(routes.CHANGE_USER_PASSWORD_ROUTE, json={"email": email, "new_password": new_password})

        assert response.status_code == status_code
        assert response.json == value

        if status_code == 200:
            assert verificator.change_password_requests.get(email) is not None
            assert verificator.change_password_requests.get(email).get("email") == email
            assert verificator.change_password_requests.get(email).get("code") is not None
            assert verificator.change_password_requests.get(email).get("new_password") is not None
            assert verificator.exists_change_password_request(email) == True
            assert encryption.check_hashed_value(new_password, verificator.change_password_requests[email]["new_password"]) == True
            

@pytest.mark.parametrize("email, password, value, status_code",  [
    ("test@example.com", "Password123!", {"message": "Password is correct"}, 200),
    ("   ", "Password123!", {"error": "Missing or invalid input data"}, 400),
    ("", "Password123!", {"error": "Missing or invalid input data"}, 400),
    (None, "Password123!", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", "", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", "  ", {"error": "Missing or invalid input data"}, 400),
    ("test@example.com", None, {"error": "Missing or invalid input data"}, 400),
    ("notfound@example.com", "Password123!", {"error": "User not found"}, 404),
    ("test", "Password123!", {"error": "Invalid email"}, 400),
    ("test@", "Password123!", {"error": "Invalid email"}, 400),
    ("test@example", "Password123!", {"error": "Invalid email"}, 400),
    ("test@example.", "Password123!", {"error": "Invalid email"}, 400),
    ("test@example.c", "Password123!", {"error": "Invalid email"}, 400),
    ("test.com", "Password123!", {"error": "Invalid email"}, 400),
    ("test@example.com", "Passwort321!", {"error": "Invalid password"}, 401),
])
def test_check_password(client, app, db, email, password, value, status_code):
    with app.app_context():
        import core.utils.routes as routes

        user = users.User(username="test", email="test@example.com", password_hash=generate_password_hash("Password123!"), role="user")
        db.session.add(user)
        db.session.commit()

        response = client.post(routes.CHECK_PASSWORD_ROUTE, json={"email": email, "password": password})

        assert response.status_code == status_code
        assert response.json == value

        if status_code == 200:
            assert response.json["message"] == "Password is correct"


def test_user_information(client, db):
    # Anfrage an den TokenEmail-Endpunkt senden
    preset_refresh_token = create_access_token(identity="test@example.com")

    user = users.User(username="test", email="test@example.com", role="user")
    db.session.add(user)
    db.session.commit()

    from core.utils.routes import USER_INFORMATION_ROUTE
    response = client.get(USER_INFORMATION_ROUTE, headers={'Authorization': f'Bearer {preset_refresh_token}'})

    assert response.status_code == 200
    assert response.json is not None
    assert response.json.get("email") == "test@example.com"
    assert response.json.get("username") == "test"
    assert response.json.get("role") == "user"
    assert response.json.get("created_at") is not None
    assert response.json.get("id") is not None