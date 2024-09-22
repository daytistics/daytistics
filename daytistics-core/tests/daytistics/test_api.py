import datetime

from ninja.testing import TestClient
import pytest

from app.daytistics.models import Daytistic
from app.users.models import CustomUser
from ..factories import CustomUserFactory, DaytisticFactory


def generate_date_yesterday():
    date = datetime.date.today() - datetime.timedelta(days=1)
    return date.strftime("%m/%d/%Y")


def generate_date_two_weeks_ago():
    date = datetime.date.today() - datetime.timedelta(weeks=2)
    return date.strftime("%m/%d/%Y")


def generate_date_five_weeks_ago():
    date = datetime.date.today() - datetime.timedelta(weeks=5)
    return date.strftime("%m/%d/%Y")


def generate_date_tommorow():
    # In Format 2023-03-01
    date = datetime.date.today() + datetime.timedelta(days=1)
    return date.strftime("%m/%d/%Y")


@pytest.mark.django_db
class TestCreateDaytistic:

    @pytest.mark.parametrize(
        "date,expected_status,expected_json",
        [
            (
                generate_date_yesterday(),
                201,
                {"id": 1},
            ),
            (
                datetime.date.today().strftime("%m/%d/%Y"),
                201,
                {"id": 1},
            ),
            ("", 422, {"detail": "Date is required"}),
            (generate_date_tommorow(), 400, {"detail": "Date is in the future"}),
            ("21/21/2121", 422, {"detail": "Invalid date format. Use %m/%d/%Y"}),
            (
                generate_date_five_weeks_ago(),
                400,
                {"detail": "Date must be within the last 4 weeks"},
            ),
            (
                generate_date_two_weeks_ago(),
                409,
                {"detail": "Daytistic already exists"},
            ),
        ],
    )
    def test_auth_success(
        self, daytistics_client, users_client, date, expected_status, expected_json
    ):
        user = CustomUserFactory.create(is_active=True)
        if expected_status == 409:
            DaytisticFactory.create(
                user=user, date=datetime.datetime.strptime(date, "%m/%d/%Y")
            )

        response = users_client.post(
            "/login/", json={"email": user.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})
        response = daytistics_client.post(
            "create/",
            json={"date": date},
        )
        assert response.status_code == expected_status
        assert response.json() == expected_json

        if expected_status == 201:
            date = datetime.datetime.strptime(date, "%m/%d/%Y")
            assert Daytistic.objects.filter(user=user, date=date).exists()

    def test_auth_failure(self, daytistics_client):
        response = daytistics_client.post(
            "create/",
            json={"date": generate_date_yesterday()},
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}


# TODO: Complete tests
@pytest.mark.django_db
class TestListDaytistics:

    def test_auth_success(self, daytistics_client: TestClient, users_client):
        user1 = CustomUserFactory.create(is_active=True)
        user2 = CustomUserFactory.create(is_active=True)

        user1_daytistics: list[Daytistic] = [
            DaytisticFactory.create(user=user1) for _ in range(10)
        ]
        user2_daytistics: list[Daytistic] = [
            DaytisticFactory.create(user=user2) for _ in range(2)
        ]

        response = users_client.post(
            "/login/", json={"email": user1.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})
        response = daytistics_client.get("")

        assert response.status_code == 200

        daytistics = response.json()["items"]
        assert len(daytistics) == 5

        user1_from_db = CustomUser.objects.get(id=user1.id)

        user1_schema = {
            "username": user1_from_db.username,
            "email": user1_from_db.email,
            "is_active": user1_from_db.is_active,
            "is_staff": user1_from_db.is_staff,
            "is_superuser": user1_from_db.is_superuser,
            "groups": [group.name for group in user1_from_db.groups.all()],
            "user_permissions": [
                permission.codename
                for permission in user1_from_db.user_permissions.all()
            ],
            "date_joined": user1_from_db.date_joined.isoformat()[:19],
            "last_login": (
                user1_from_db.last_login.isoformat()[:19]
                if user1_from_db.last_login
                else None
            ),
        }

    def test_auth_failure(self, daytistics_client):
        response = daytistics_client.get("")
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}
