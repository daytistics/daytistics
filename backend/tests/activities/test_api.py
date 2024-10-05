import pytest
from daytistics.activities.models import ActivityCategory, ActivityType
from tests.factories import CustomUserFactory


@pytest.mark.django_db
class TestListActivities:

    @pytest.fixture
    def setup_data(self):
        categories = [
            ActivityCategory.objects.create(name=f"Category {i}") for i in range(1, 3)
        ]
        activity_types = [
            ActivityType.objects.create(
                name="Activity 1", category=categories[0], active=True
            ),
            ActivityType.objects.create(
                name="Activity 2", category=categories[0], active=True
            ),
            ActivityType.objects.create(
                name="Activity 3", category=categories[1], active=True
            ),
            ActivityType.objects.create(
                name="Activity 4", category=categories[1], active=False
            ),
        ]
        return categories, activity_types

    @pytest.fixture
    def authenticated_client(self, activities_client, users_client):
        user = CustomUserFactory.create(is_active=True)
        response = users_client.post(
            "/login/", json={"email": user.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]
        activities_client.headers.update({"Authorization": f"Bearer {access_token}"})
        return activities_client, user

    def test_user_activities(self, authenticated_client, setup_data):
        client, user = authenticated_client
        _, activity_types = setup_data
        user.activities.set(activity_types[:2])

        response = client.get("/?all=false")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(activity["available"] for activity in data)
        assert all(activity["active"] for activity in data)
        assert set(activity["name"] for activity in data) == {
            "Activity 1",
            "Activity 2",
        }

    def test_all_activities(self, authenticated_client, setup_data):
        client, _ = authenticated_client
        _, activity_types = setup_data

        response = client.get("/?all=true")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3  # Should not include inactive Activity 4
        assert set(activity["name"] for activity in data) == {
            "Activity 1",
            "Activity 2",
            "Activity 3",
        }

    def test_default_to_user_activities(self, authenticated_client, setup_data):
        client, user = authenticated_client
        _, activity_types = setup_data
        user.activities.set(activity_types[:2])

        response = client.get("/")  # No 'all' parameter

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(activity["available"] for activity in data)

    def test_inactive_activities_excluded(self, authenticated_client, setup_data):
        client, _ = authenticated_client
        _, activity_types = setup_data

        response = client.get("/?all=true")

        assert response.status_code == 200
        data = response.json()
        assert "Activity 4" not in [activity["name"] for activity in data]
