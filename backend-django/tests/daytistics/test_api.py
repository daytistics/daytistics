import datetime
from operator import le
from zoneinfo import ZoneInfo

import pytest
from ninja_jwt.tokens import AccessToken
from ninja.testing import TestClient

from daytistics.daytistics.models import Daytistic
from daytistics.activities.models import ActivityEntry, ActivityType
from daytistics.daytistics.helpers import build_daytistic_response
from ..factories import (
    ActivityEntryFactory,
    CustomUserFactory,
    DaytisticFactory,
    ActivityTypeFactory,
)


@pytest.mark.django_db
class TestCreateDaytistic:
    def test_auth_success_and_created(self, daytistics_client):
        access_token = AccessToken.for_user(
            user := CustomUserFactory.create(is_active=True)
        )
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        date = datetime.datetime.now().date().isoformat()

        response = daytistics_client.post(
            "create",
            json={"date": date},
        )
        assert response.status_code == 201
        assert response.json() == {"id": 1}

        assert Daytistic.objects.filter(
            user=user, date=datetime.datetime.fromisoformat(date)
        ).exists()

    def test_auth_success_and_invalid_date(self, daytistics_client):
        access_token = AccessToken.for_user(CustomUserFactory.create(is_active=True))
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.post(
            "create",
            json={"date": "Lorem ipsum dolor sit amet"},
        )
        assert response.status_code == 422
        assert response.json() == {
            "detail": "Invalid date format. Must be in ISO format (YYYY-MM-DD)"
        }

    def test_auth_success_and_already_exists(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user)

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        date = datetime.datetime.now().date().isoformat()

        response = daytistics_client.post(
            "create",
            json={"date": date},
        )
        assert response.status_code == 409
        assert response.json() == {"detail": "Daytistic already exists"}

    def test_auth_success_and_date_in_future(self, daytistics_client):
        access_token = AccessToken.for_user(CustomUserFactory.create(is_active=True))
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        date = (datetime.datetime.now() + datetime.timedelta(days=2)).date().isoformat()

        response = daytistics_client.post(
            "create",
            json={
                "date": date,
            },
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Date is in the future"}

    def test_auth_failure(self, daytistics_client):
        response = daytistics_client.post(
            "create",
            json={
                "date": (datetime.datetime.now() + datetime.timedelta(days=1))
                .astimezone(ZoneInfo("UTC"))
                .isoformat()
            },
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.django_db
class TestGetDaytistic:

    def test_auth_success_and_daytistic_found(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)

        date = datetime.datetime(2023, 3, 1, 4, 0)

        daytistic = DaytisticFactory.create(user=user, date=date)

        access_token = AccessToken.for_user(user)

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})
        response = daytistics_client.get(f"{daytistic.id}")

        assert response.status_code == 200
        assert response.json() == build_daytistic_response(daytistic)

    def test_auth_success_and_daytistic_not_found(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)

        access_token = AccessToken.for_user(user)
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

    def test_auth_success_and_no_page_given(self, daytistics_client, users_client):
        user = CustomUserFactory.create(is_active=True)
        second_user = CustomUserFactory.create(is_active=True)

        dates = [
            datetime.datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0, day=i
            )
            for i in range(1, 6)
        ]
        daytistics = [DaytisticFactory.create(user=user, date=date) for date in dates]
        second_users_daytistic = DaytisticFactory.create(user=second_user)

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.get("list")
        assert response.status_code == 200
        assert response.json()["items"] == [
            build_daytistic_response(daytistic) for daytistic in daytistics[::-1]
        ]

        assert len(response.json()["items"]) == len(daytistics)
        assert (
            build_daytistic_response(second_users_daytistic)
            not in response.json()["items"]
        )

    def test_auth_success_and_page_given(self, daytistics_client, users_client):
        user = CustomUserFactory.create(is_active=True)

        dates = [
            datetime.datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0, day=i
            )
            for i in range(1, 11)
        ]
        daytistics = [DaytisticFactory.create(user=user, date=date) for date in dates]

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.get("list", params={"page": 1})
        assert response.status_code == 200
        assert response.json()["items"] == [
            build_daytistic_response(daytistic) for daytistic in daytistics[::-1][:5]
        ]

        response = daytistics_client.get("list?page=2")
        assert response.status_code == 200
        assert response.json()["items"] == [
            build_daytistic_response(daytistic) for daytistic in daytistics[::-1][5:]
        ]

    def test_auth_failure(self, daytistics_client):
        response = daytistics_client.get("list")
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.django_db
class TestAddActivityToDaytistic:

    def test_auth_success_and_no_errors_and_first_activity_in_daytistic(
        self, daytistics_client: TestClient
    ):
        user = CustomUserFactory.create(is_active=True)
        daytistic: Daytistic = DaytisticFactory.create(user=user)
        activity_type: ActivityType = ActivityTypeFactory.create()

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        start_time = 10
        end_time = 70

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity",
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
                    "start_time": start_time,
                    "end_time": end_time,
                }
            ]
        } == response.json()

    def test_auth_success_and_no_errors_and_returning_list(
        self, daytistics_client, users_client
    ):
        date = datetime.datetime.now().date()

        user = CustomUserFactory.create(is_active=True)
        daytistic: Daytistic = DaytisticFactory.create(user=user, date=date)
        activity_type: ActivityType = ActivityTypeFactory.create()

        other_activity_entry: ActivityEntry = ActivityEntryFactory.create(
            start_time=500, end_time=600
        )
        daytistic.activities.add(other_activity_entry)

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        start_time = 0
        end_time = 60

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity",
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
                    "id": other_activity_entry.pk,
                    "name": other_activity_entry.type.name,
                    "duration": 100,
                    "start_time": other_activity_entry.start_time,
                    "end_time": other_activity_entry.end_time,
                },
                {
                    "id": 2,
                    "name": activity_type.name,
                    "duration": 60,
                    "start_time": start_time,
                    "end_time": end_time,
                },
            ]
        } == response.json()

    def test_auth_success_and_activity_not_found(self, daytistics_client, users_client):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user)

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        start_time = 20
        end_time = 40

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity",
            json={
                "id": 9999,  # Non-existent activity ID
                "start_time": start_time,
                "end_time": end_time,
            },
        )

        assert response.status_code == 404
        assert response.json() == {"detail": "Activity not found"}

    @pytest.mark.parametrize(
        "start_time, end_time",
        (
            (-10, 60),
            (2000, 60),
            (0, 1441),
            (0, -1),
        ),
    )
    def test_auth_success_and_times_out_of_bounds(
        self, daytistics_client, start_time, end_time
    ):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user)

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity",
            json={
                "id": ActivityEntryFactory.create().type.pk,
                "start_time": start_time,
                "end_time": end_time,
            },
        )

        assert response.status_code == 422

    def test_start_time_after_end_time(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(
            user=user, date=datetime.datetime.now().date()
        )
        activity_type = ActivityTypeFactory.create()

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        start_time = 60
        end_time = 30

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity",
            json={
                "id": activity_type.pk,
                "start_time": start_time,
                "end_time": end_time,
            },
        )

        assert response.status_code == 422
        assert response.json() == {"detail": "Start time must be before end time"}

    def test_auth_failure(self, daytistics_client):

        daytistic = DaytisticFactory.create()

        response = daytistics_client.post(
            f"{daytistic.id}/add-activity",
            json={"id": 1, "start_time": 0, "end_time": 60},
        )

        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}
