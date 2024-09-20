import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from app.users.models import CustomUser
from faker import Faker
import factory
from factory.django import DjangoModelFactory
from app.utils.api import success_response, error_response

from tests.conftest import fake


@pytest.mark.django_db
class TestRegisterView:
    @pytest.mark.parametrize(
        "username,email,password,expected_json",
        [
            ("valid_user", "valid@example.com", "StrongPass123!", success_response('Please check your email to verify your account.', 201)), 
            ("sh", "valid@example.com", "StrongPass123!", error_response('Invalid username.', 400)),
            ("valid_user", "invalid_email", "StrongPass123!", error_response('Invalid email.', 400)),
            ("valid_user", "valid@example.com", "short", error_response('Invalid password.', 400)),
            ("Exists", "exists@example.com", "StrongPass123!", error_response('Username already exists.', 400)),
        ],
    )
    def test_post(self, api_client, username, email, password, expected_json):
        # Create a new Faker instance inside the test method
        fake = Faker()

        url = reverse("register")
        data = {
            "username": username if username != "valid_user" else fake.user_name(),
            "email": email if email != "valid@example.com" else fake.email(),
            "password1": password,
        }

        response = api_client.post(url, data)

