import pytest
from ninja.testing import TestClient
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from daytistics.users.tokens import account_activation_token
from daytistics.users.models import CustomUser
from daytistics.activities.models import ActivityType
from tests.factories import CustomUserFactory


@pytest.mark.django_db
class TestRegisterView:
    @pytest.mark.parametrize(
        "username,email,password1,password2,expected_json,expected_status",
        [
            (
                "valid_user",
                "valid@example.com",
                "StrongPass123!",
                "StrongPass123!",
                {"detail": "Please check your email to verify your account."},
                201,
            ),
            (
                "existing",
                "existing@example.com",
                "StrongPass123!",
                "StrongPass123!",
                {"detail": "User already exists."},
                400,
            ),
            (
                "Invalid User",
                "valid@example.com",
                "StrongPass123!",
                "StrongPass123!",
                {"detail": "Invalid username."},
                400,
            ),
            (
                "valid_user",
                "valid@example.com",
                "StrongPass1234!",
                "StrongPass123!",
                {"detail": "Passwords do not match."},
                400,
            ),
            (
                "valid_user",
                "valid@example.com",
                "StrongPass123",
                "StrongPass123",
                {"detail": "Invalid or insecure password."},
                400,
            ),
            (
                "valid_user",
                "valid@example.com",
                "StrongPass!",
                "StrongPass!",
                {"detail": "Invalid or insecure password."},
                400,
            ),
            (
                "valid_user",
                "valid@example.com",
                "Str",
                "Str",
                {"detail": "Invalid or insecure password."},
                400,
            ),
            (
                "valid_user",
                "valid@example.com",
                "strongpassword123!",
                "strongpassword123!",
                {"detail": "Invalid or insecure password."},
                400,
            ),
            (
                "valid_user",
                "valid@example.com",
                "STRONGPASSWORD123!",
                "STRONGPASSWORD123!",
                {"detail": "Invalid or insecure password."},
                400,
            ),
        ],
    )
    def test_post(
        self,
        users_client: TestClient,
        username,
        email,
        password1,
        password2,
        expected_json,
        expected_status,
        default_activities,
    ):
        from django.core import mail

        CustomUser.objects.create(
            username=username, email="existing@example.com", password=password1
        )

        payload = {
            "username": username,
            "email": email,
            "password1": password1,
            "password2": password2,
        }
        response = users_client.post("register/", json=payload)
        assert response.json() == expected_json
        assert response.status_code == expected_status

        assert CustomUser.objects.filter(email=email).exists() == (
            expected_status == 201
            or expected_json == {"detail": "User already exists."}
        )
        user = CustomUser.objects.filter(email=email).first()

        if expected_status == 201:
            for activity_type, _ in default_activities:
                assert activity_type in user.activities.all()

        if expected_status == 201:
            assert len(mail.outbox) == 1
            assert email in mail.outbox[0].to
        else:
            assert len(mail.outbox) == 0


@pytest.mark.django_db
class TestAccountActivationView:

    @pytest.mark.parametrize(
        "is_valid_token,expected_json,expected_status",
        [
            (True, {"detail": "Account activated successfully!"}, 200),
            (False, {"detail": "Activation link is invalid."}, 400),
        ],
    )
    def test_activate(
        self,
        users_client: TestClient,
        is_valid_token,
        expected_json,
        expected_status,
    ):

        inactive_user = CustomUserFactory.create(is_active=False)

        uid = urlsafe_base64_encode(force_bytes(inactive_user.pk))
        token = account_activation_token.make_token(inactive_user)

        if not is_valid_token:
            # Invalidate the token by changing the user's password
            inactive_user.set_password("abc")
            inactive_user.save()

        response = users_client.get(f"/activate/{uid}/{token}")

        assert response.status_code == expected_status
        assert response.json() == expected_json

        inactive_user.refresh_from_db()
        assert inactive_user.is_active == (expected_status == 200)

    def test_activate_invalid_user(self, users_client: TestClient):
        uid = urlsafe_base64_encode(force_bytes(999))  # Non-existent user ID
        token = "invalid-token"

        response = users_client.get(f"/activate/{uid}/{token}")

        assert response.status_code == 400
        assert response.json() == {"detail": "Activation link is invalid."}


@pytest.mark.django_db
class TestLoginView:
    @pytest.fixture
    def active_user(self):
        return CustomUserFactory.create(is_active=True, password="password123")

    @pytest.fixture
    def inactive_user(self):
        return CustomUserFactory.create(is_active=False)

    def test_successful_login(self, users_client: TestClient, active_user):
        payload = {"email": active_user.email, "password": "password123"}
        response = users_client.post("/login/", json=payload)

        assert response.status_code == 200
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()

        user_from_db = get_object_or_404(CustomUser, pk=active_user.pk)
        assert user_from_db.last_login is not None
        assert user_from_db.last_login.date() == timezone.now().date()

    def test_login_with_incorrect_password(self, users_client: TestClient, active_user):
        payload = {"email": active_user.email, "password": "wrongpassword"}
        response = users_client.post("/login/", json=payload)

        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid credentials."}

    def test_login_with_nonexistent_email(self, users_client: TestClient):
        payload = {"email": "nonexistent@example.com", "password": "password123"}
        response = users_client.post("/login/", json=payload)

        assert response.status_code == 404
        assert response.json() == {"detail": "User not found."}

    def test_login_with_inactive_user(self, users_client: TestClient, inactive_user):
        payload = {"email": inactive_user.email, "password": "password123"}
        response = users_client.post("/login/", json=payload)

        assert response.status_code == 400
        assert response.json() == {"detail": "Account is not activated."}

    @pytest.mark.parametrize(
        "email,password,expected_status,expected_json",
        [
            ("", "password123", 400, {"detail": "Email and password are required."}),
            ("invalid_email", "password123", 400, {"detail": "Invalid email."}),
            (
                "valid@example.com",
                "",
                400,
                {"detail": "Email and password are required."},
            ),
        ],
    )
    def test_login_with_invalid_input(
        self, users_client: TestClient, email, password, expected_status, expected_json
    ):
        payload = {"email": email, "password": password}
        response = users_client.post("/login/", json=payload)

        assert response.status_code == expected_status
        assert response.json() == expected_json


@pytest.mark.django_db
class TestGetUserProfile:

    def test_auth_success(self, users_client: TestClient):
        user = CustomUserFactory.create(is_active=True)
        response = users_client.post(
            "/login/", json={"email": user.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]

        users_client.headers.update({"Authorization": f"Bearer {access_token}"})
        response = users_client.get("/profile")
        assert response.status_code == 200
        for item in {
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "groups": [],
            "user_permissions": [],
            "timezone": user.timezone,
            "timeformat": user.timeformat,
        }:
            assert item in response.json()

    def test_auth_failure(self, users_client: TestClient):
        response = users_client.get("/profile")
        assert response.status_code == 401
