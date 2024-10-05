import datetime
from zoneinfo import ZoneInfo

import pytest
from ninja_jwt.tokens import AccessToken
from ninja.testing import TestClient

from daytistics.daytistics.models import Daytistic
from daytistics.activities.models import ActivityEntry, ActivityType
from daytistics.daytistics.helpers import (
    build_daytistic_response,
)
from daytistics.utils.time import minutes_today_as_iso
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
    def test_auth_success_and_created(self, daytistics_client):
        access_token = AccessToken.for_user(
            user := CustomUserFactory.create(is_active=True)
        )
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        date = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

        response = daytistics_client.post(
            "create/",
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
            "create/",
            json={"date": "Lorem ipsum dolor sit amet"},
        )
        assert response.status_code == 422
        assert response.json() == {
            "detail": "Invalid date format. Must be in ISO format"
        }

    def test_auth_success_and_already_exists(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user)

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.post(
            "create/",
            json={"date": daytistic.date.isoformat()},
        )
        assert response.status_code == 409
        assert response.json() == {"detail": "Daytistic already exists"}

    def test_auth_success_and_too_old_date(self, daytistics_client):
        access_token = AccessToken.for_user(CustomUserFactory.create(is_active=True))
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.post(
            "create/",
            json={"date": generate_date_five_weeks_ago()},
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Date must be within the last 4 weeks"}

    def test_auth_success_and_date_in_future(self, daytistics_client):
        access_token = AccessToken.for_user(CustomUserFactory.create(is_active=True))
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.post(
            "create/",
            json={"date": generate_date_tommorow()},
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Date is in the future"}

    def test_auth_failure(self, daytistics_client):
        response = daytistics_client.post(
            "create/",
            json={"date": generate_date_yesterday()},
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.django_db
class TestGetDaytistic:

    def test_auth_success_and_daytistic_found(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)

        # today 4 am in Berlin
        date = datetime.datetime(2023, 3, 1, 4, 0, tzinfo=ZoneInfo("Europe/Berlin"))

        daytistic = DaytisticFactory.create(user=user, date=date)

        access_token = AccessToken.for_user(user)

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})
        response = daytistics_client.get(f"{daytistic.id}?timezone=Europe/Athens")

        assert response.status_code == 200
        assert response.json() == build_daytistic_response(
            daytistic, ZoneInfo("Europe/Athens")
        )

    def test_auth_success_and_daytistic_not_found(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.get("1?timezone=Europe/Athens")

        assert response.status_code == 404
        assert response.json() == {"detail": "Daytistic not found"}

    def test_auth_success_and_no_timezone_provided(
        self, daytistics_client, users_client
    ):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user)

        response = users_client.post(
            "/login/", json={"email": user.email, "password": "password123"}
        )
        access_token = response.json()["accessToken"]

        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})
        response = daytistics_client.get(f"{daytistic.id}")
        assert response.status_code == 422

    def test_auth_failure(self, daytistics_client):
        response = daytistics_client.get("1")
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.django_db
class TestListDaytistics:

    def test_auth_success_and_timezone_is_valid(self, daytistics_client, users_client):
        user = CustomUserFactory.create(is_active=True)
        second_user = CustomUserFactory.create(is_active=True)

        daytistics = DaytisticFactory.create_batch(5, user=user)
        second_users_daytistic = DaytisticFactory.create(user=second_user)

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.get("list?timezone=Europe/Athens")
        assert response.status_code == 200
        assert response.json() == {
            "count": len(daytistics),
            "items": [
                build_daytistic_response(daytistic, ZoneInfo("Europe/Athens"))
                for daytistic in daytistics
            ],
        }
        assert len(response.json()["items"]) == 5
        assert (
            build_daytistic_response(second_users_daytistic, ZoneInfo("Europe/Athens"))
            not in response.json()["items"]
        )

    def test_auth_success_and_invalid_timezone(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)
        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.get("list?timezone=Invalid/Timezone")
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid timezone"}

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

        date = datetime.datetime.fromisoformat(daytistic.date.isoformat())
        start_time = (
            date.astimezone(ZoneInfo("Europe/Athens"))
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .isoformat()
        )

        end_time = (
            date.astimezone(ZoneInfo("Europe/Athens"))
            .replace(hour=1, minute=0, second=0, microsecond=0)
            .isoformat()
        )

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
                    "start_time": start_time,
                    "end_time": end_time,
                }
            ]
        } == response.json()

    def test_auth_success_and_no_errors_and_returning_list(
        self, daytistics_client, users_client
    ):
        date = datetime.datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        user = CustomUserFactory.create(is_active=True)
        daytistic: Daytistic = DaytisticFactory.create(user=user, date=date.date())

        other_activity_entry: ActivityEntry = ActivityEntryFactory.create(
            start_time=date.astimezone(ZoneInfo("Europe/Athens"))
            + datetime.timedelta(minutes=80),
            end_time=date.astimezone(ZoneInfo("Europe/Athens"))
            + datetime.timedelta(minutes=200),
        )

        daytistic.activities.add(other_activity_entry)
        activity_type: ActivityType = ActivityTypeFactory.create()

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        start_time = (
            date.astimezone(ZoneInfo("Europe/Athens"))
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .isoformat()
        )

        end_time = (
            date.astimezone(ZoneInfo("Europe/Athens"))
            .replace(hour=1, minute=0, second=0, microsecond=0)
            .isoformat()
        )

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
                    "id": other_activity_entry.pk,
                    "name": other_activity_entry.type.name,
                    "duration": 120,
                    "start_time": other_activity_entry.start_time.isoformat(),
                    "end_time": other_activity_entry.end_time.isoformat(),
                },
                {
                    "id": activity_type.pk,
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

        start_time = minutes_today_as_iso(datetime.datetime.now(), 0, "+02:00")
        end_time = minutes_today_as_iso(datetime.datetime.now(), 60, "+02:00")

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": 9999,  # Non-existent activity ID
                "start_time": start_time,
                "end_time": end_time,
            },
        )

        assert response.status_code == 404
        assert response.json() == {"detail": "Activity not found"}

    # **Aktualisierte Tests**

    def test_invalid_date_format(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user)

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": 1,
                "start_time": "invalid-date-format",
                "end_time": "2024-10-03T10:00:00+02:00",
            },
        )

        assert response.status_code == 422
        assert response.json() == {
            "detail": "Invalid date format. Must be in ISO format"
        }

    def test_missing_timezone(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user)

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        start_time = "2024-10-03T09:00:00"
        end_time = "2024-10-03T10:00:00+02:00"

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": 1,
                "start_time": start_time,
                "end_time": end_time,
            },
        )

        assert response.status_code == 422
        assert response.json() == {"detail": "Timezone is required"}

    def test_different_timezones(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user)

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        start_time = "2024-10-03T09:00:00+01:00"
        end_time = "2024-10-03T10:00:00+02:00"

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": 1,
                "start_time": start_time,
                "end_time": end_time,
            },
        )

        assert response.status_code == 422
        assert response.json() == {
            "detail": "Start time and end time must have the same timezone"
        }

    def test_activity_date_mismatch(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user, date=datetime.date(2024, 10, 3))

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        start_time = "2024-10-04T09:00:00+02:00"
        end_time = "2024-10-04T10:00:00+02:00"

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": 1,
                "start_time": start_time,
                "end_time": end_time,
            },
        )

        assert response.status_code == 422
        assert response.json() == {"detail": "Activity date must match daytistic date"}

    def test_start_time_after_end_time_corrected(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user, date=datetime.date(2024, 10, 3))
        activity_type = ActivityTypeFactory.create()

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        start_time = "2024-10-03T11:00:00+02:00"
        end_time = "2024-10-03T10:00:00+02:00"

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": activity_type.pk,
                "start_time": start_time,
                "end_time": end_time,
            },
        )

        assert response.status_code == 422
        assert response.json() == {"detail": "Start time must be before end time"}

    def test_overlapping_activity_corrected(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user, date=datetime.date(2024, 10, 3))
        activity_type = ActivityTypeFactory.create()

        existing_activity = ActivityEntryFactory.create(
            type=activity_type,
            start_time=datetime.datetime(
                2024, 10, 3, 9, 0, tzinfo=ZoneInfo("Europe/Athens")
            ),
            end_time=datetime.datetime(
                2024, 10, 3, 10, 0, tzinfo=ZoneInfo("Europe/Athens")
            ),
        )
        daytistic.activities.add(existing_activity)
        daytistic.save()

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": activity_type.pk,
                "start_time": existing_activity.start_time.isoformat(),
                "end_time": existing_activity.end_time.isoformat(),
            },
        )

        assert response.status_code == 422
        assert response.json() == {"detail": "Activity overlaps with existing activity"}

    def test_start_and_end_time_on_different_dates(self, daytistics_client):
        user = CustomUserFactory.create(is_active=True)
        daytistic = DaytisticFactory.create(user=user, date=datetime.date(2024, 10, 3))
        activity_type = ActivityTypeFactory.create()

        access_token = AccessToken.for_user(user)
        daytistics_client.headers.update({"Authorization": f"Bearer {access_token}"})

        start_time = "2024-10-03T23:00:00+02:00"
        end_time = "2024-10-04T01:00:00+02:00"

        response = daytistics_client.post(
            f"{daytistic.pk}/add-activity/",
            json={
                "id": activity_type.pk,
                "start_time": start_time,
                "end_time": end_time,
            },
        )

        assert response.status_code == 422
        assert response.json() == {
            "detail": "Start time and end time must be on the same date"
        }

    def test_auth_failure(self, daytistics_client):

        daytistic = DaytisticFactory.create()

        response = daytistics_client.post(
            f"{daytistic.id}/add-activity/",
            json={"id": 1, "start_time": 0, "end_time": 60},
        )

        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized"}
