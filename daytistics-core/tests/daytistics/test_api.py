import datetime

import pytest

from daytistics.daytistics.models import Daytistic
from daytistics.activities.models import ActivityEntry, ActivityType
from daytistics.daytistics.helpers import (
    build_daytistic_response,
)
from daytistics.utils.time import minutes_today_as_iso, minutes_as_datetime
from ..factories import (
    ActivityEntryFactory,
    CustomUserFactory,
    DaytisticFactory,
    ActivityTypeFactory,
)


def generate_date_yesterday():
    date = datetime.date.today() - datetime.timedelta(days=1)
    return date.isoformat()


def generate_date_two_weeks_ago():
    date = datetime.date.today() - datetime.timedelta(weeks=2)
    return date.isoformat()


def generate_date_five_weeks_ago():
    date = datetime.date.today() - datetime.timedelta(weeks=5)
    return date.isoformat()


def generate_date_tommorow():
    # In Format 2023-03-01
    date = datetime.date.today() + datetime.timedelta(days=1)
    return date.isoformat()


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
                datetime.date.today().isoformat(),
                201,
                {"id": 1},
            ),
            ("", 422, {"detail": "Date is required"}),
            (generate_date_tommorow(), 400, {"detail": "Date is in the future"}),
            (
                "21/21/2121",
                422,
                {"detail": "Invalid date format. Must be in ISO format"},
            ),
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
            DaytisticFactory.create(user=user, date=date)

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
            date = datetime.datetime.isoformat(datetime.datetime.fromisoformat(date))
            assert Daytistic.objects.filter(
                user=user, date=datetime.datetime.fromisoformat(date)
            ).exists()

    def test_auth_failure(self, daytistics_client):
        response = daytistics_client.post(
            "create/",
            json={"date": generate_date_yesterday()},
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.django_db
class TestGetDaytistic:

    def test_auth_success_and_daytistic_found(self, daytistics_client, users_client):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user)

        response = users_client.post(
            "/login/", json={"email": user.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})
        response = daytistics_client.get(f"{daytistic.id}")
        assert response.status_code == 200
        assert response.json() == build_daytistic_response(daytistic)

    def test_auth_success_and_daytistic_not_found(
        self, daytistics_client, users_client
    ):
        user = CustomUserFactory.create(is_active=True)

        response = users_client.post(
            "/login/", json={"email": user.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})
        response = daytistics_client.get("1")
        assert response.status_code == 404
        assert response.json() == {"detail": "Daytistic not found"}

    def test_auth_failure(self, daytistics_client):
        response = daytistics_client.get("1")
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.django_db
class TestListDaytistics:

    def test_auth_success(self, daytistics_client, users_client):
        user = CustomUserFactory.create(is_active=True)
        second_user = CustomUserFactory.create(is_active=True)
        daytistics = DaytisticFactory.create_batch(5, user=user)
        second_users_daytistic = DaytisticFactory.create(user=second_user)

        response = users_client.post(
            "/login/", json={"email": user.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})
        response = daytistics_client.get("")
        assert response.status_code == 200
        assert response.json() == {
            "count": len(daytistics),
            "items": [build_daytistic_response(daytistic) for daytistic in daytistics],
        }
        assert len(response.json()["items"]) == 5
        assert (
            build_daytistic_response(second_users_daytistic)
            not in response.json()["items"]
        )

    def test_auth_failure(self, daytistics_client):
        response = daytistics_client.get("")
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.django_db
class TestAddActivityToDaytistic:

    def test_auth_success_and_no_errors_and_first_activity_in_daytistic(
        self, daytistics_client, users_client
    ):
        user = CustomUserFactory.create(is_active=True)
        daytistic: Daytistic = DaytisticFactory.create(user=user)
        activity_type: ActivityType = ActivityTypeFactory.create()

        response = users_client.post(
            "/login/", json={"email": user.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        date = datetime.datetime.fromisoformat(daytistic.date.isoformat())
        start_time = minutes_today_as_iso(date, 0, "+02:00")
        end_time = minutes_today_as_iso(date, 60, "+02:00")

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": activity_type.pk,
                "start_time": start_time,
                "end_time": end_time,
            },
        )

        assert response.status_code == 201
        assert {
            "activities": [
                {
                    "id": 1,
                    "name": activity_type.name,
                    "duration": 60,
                    "start_time": 0,
                    "end_time": 60,
                }
            ]
        } == response.json()

    def test_auth_success_and_no_errors_and_returning_list(
        self, daytistics_client, users_client
    ):
        base_date = datetime.datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        user = CustomUserFactory.create(is_active=True)
        daytistic: Daytistic = DaytisticFactory.create(user=user, date=base_date.date())
        other_activity_entry = ActivityEntryFactory.create(
            start_time=minutes_as_datetime(base_date, 80, "+02:00"),
            end_time=minutes_as_datetime(base_date, 200, "+02:00"),
        )
        daytistic.activities.add(other_activity_entry)
        activity_type: ActivityType = ActivityTypeFactory.create()

        response = users_client.post(
            "/login/", json={"email": user.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        start_time = minutes_today_as_iso(base_date, 0, "+02:00")
        end_time = minutes_today_as_iso(base_date, 60, "+02:00")

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": activity_type.pk,
                "start_time": start_time,
                "end_time": end_time,
            },
        )

        assert response.status_code == 201
        assert {
            "activities": [
                {
                    "id": 1,
                    "name": other_activity_entry.type.name,
                    "duration": 120,
                    "start_time": 80,
                    "end_time": 200,
                },
                {
                    "id": 2,
                    "name": activity_type.name,
                    "duration": 60,
                    "start_time": 0,
                    "end_time": 60,
                },
            ]
        } == response.json()

    def test_auth_success_and_activity_not_found(self, daytistics_client, users_client):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user)

        response = users_client.post(
            "/login/", json={"email": user.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        start_time = minutes_today_as_iso(datetime.datetime.now(), 0, "+02:00")
        end_time = minutes_today_as_iso(datetime.datetime.now(), 60, "+02:00")

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": 9999,
                "start_time": start_time,
                "end_time": end_time,
            },  # Non-existent activity ID
        )

        assert response.status_code == 404
        assert response.json() == {"detail": "Activity not found"}

    def test_auth_success_and_start_time_out_of_bounds(
        self, daytistics_client, users_client
    ):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user)
        activity_type = ActivityTypeFactory.create()

        response = users_client.post(
            "/login/", json={"email": user.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": activity_type.pk,
                "start_time": -10,
                "end_time": 60,
            },  # Invalid start time
        )

        assert response.status_code == 422
        assert response.json() == {"detail": "Start time must be between 0 and 1440"}

    def test_auth_success_and_end_time_out_of_bounds(
        self, daytistics_client, users_client
    ):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user)
        activity_type = ActivityTypeFactory.create()

        response = users_client.post(
            "/login/", json={"email": user.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": activity_type.pk,
                "start_time": 0,
                "end_time": 1500,
            },  # Invalid end time
        )

        assert response.status_code == 422
        assert response.json() == {"detail": "End time must be between 0 and 1440"}

    def test_auth_success_and_start_time_after_end_time(
        self, daytistics_client, users_client
    ):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user)
        activity_type = ActivityTypeFactory.create()

        response = users_client.post(
            "/login/", json={"email": user.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": activity_type.pk,
                "start_time": 100,
                "end_time": 50,
            },  # Start time after end time
        )

        assert response.status_code == 422
        assert response.json() == {"detail": "Start time must be before end time"}

    def test_auth_success_and_activities_overlap(self, daytistics_client, users_client):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user)
        activity_type = ActivityTypeFactory.create()

        # Create the ActivityEntry instance without the daytistics field
        other_activity_entry = ActivityEntryFactory.create(
            start_time=minutes_today_as_datetime(80),
            end_time=minutes_today_as_datetime(200),
        )

        # Add the Daytistic instance using the set() method
        other_activity_entry.daytistics.set([daytistic])

        response = users_client.post(
            "/login/", json={"email": user.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": activity_type.pk,
                "start_time": 100,
                "end_time": 150,
            },  # Overlapping time
        )

        assert response.status_code == 422
        assert response.json() == {"detail": "Activity overlaps with existing activity"}

    def test_auth_failure(self, daytistics_client):

        daytistic = DaytisticFactory.create()

        response = daytistics_client.post(
            f"{daytistic.id}/add-activity/",
            json={"id": 1, "start_time": 0, "end_time": 60},
        )

        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}
