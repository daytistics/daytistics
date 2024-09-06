import pytest
from django.urls import reverse
from django.utils import translation

from app.activities.models import Activity

@pytest.fixture
def authenticated_client(client, django_user_model):
    with translation.override("en"):
        username = "user"
        password = "password"
        user = django_user_model.objects.create_user(username=username, password=password)
        client.force_login(user)
        yield client


@pytest.mark.django_db
def test_handle_post_request_with_empty_activity_name(authenticated_client):
    response = authenticated_client.post(
        reverse("activities:create"),
        {"name": ""}
    )

    assert response.status_code == 400
    assert "<p class='text-red-500'>Invalid activity name</p>" in response.content.decode()


@pytest.mark.django_db
def test_render_success_message_for_new_activity_creation(authenticated_client):
    response = authenticated_client.post(
        reverse("activities:create"),
        {"name": "Sleep"}
    )

    assert response.status_code == 201
    assert "<p class='text-green-500'>Activity created successfully</p>" in response.content.decode()


@pytest.mark.django_db
def test_render_success_message_for_existing_activity(authenticated_client):
    args = (reverse("activities:create"), {"name": "Sleep"})
    initial_response = authenticated_client.post(*args)

    assert initial_response.status_code == 201

    # Second attempt to create the same activity
    response = authenticated_client.post(*args)

    assert response.status_code == 201
    assert "<p class='text-green-500'>Activity updated successfully</p>" in response.content.decode()
