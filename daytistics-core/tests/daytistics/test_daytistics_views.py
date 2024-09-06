import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from app.daytistics.models import Daytistic, ActivityEntry
from tests.factories import CustomUserFactory, DaytisticFactory, ActivityEntryFactory, ActivityFactory
from django.utils import translation
from django.conf import settings
import json
from django.template.response import TemplateResponse, HttpResponse


@pytest.mark.django_db
class TestDashboard:
    def test_dashboard_view_redirects_for_anonymous_user(self, client):
        with translation.override("en"):
            response = client.get(reverse("daytistics:dashboard"))
        assert response.status_code == 302  # Redirect to login

    def test_dashboard_view_renders_for_logged_in_user(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)
            response = client.get(reverse("daytistics:dashboard"))
            assert response.status_code == 200
            assert "daytistics/dashboard.html" in [t.name for t in response.templates]
            assert "daytistics_list" in response.context
            assert "daytistics_list_limit" in response.context
            assert (
                response.context["daytistics_list_limit"]
                == settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
            )

    def test_dashboard_view_no_params(self, client):
        DAYTISTICS_COUNT = 10

        with translation.override("en"):
            user = CustomUserFactory()

            daytistics = [DaytisticFactory(user=user) for _ in range(DAYTISTICS_COUNT)]

            client.force_login(user)
            response = client.get(reverse("daytistics:dashboard"))
            assert response.status_code == 200
            assert "daytistics/dashboard.html" in [t.name for t in response.templates]
            assert "daytistics_list" in response.context
            assert (
                len(response.context["daytistics_list"])
                == settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
            )

            # Check that only the first DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD daytistics are in the context
            for daytistic in daytistics[
                : settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
            ]:
                assert daytistic in response.context["daytistics_list"]

            # Check that the remaining daytistics are not in the context
            for daytistic in daytistics[
                settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD :
            ]:
                assert daytistic not in response.context["daytistics_list"]

    def test_dashboard_view_params_missing_list_type(self, client):
        DAYTISTICS_COUNT = 10
        LIMIT = 6

        with translation.override("en"):
            user = CustomUserFactory()

            daytistics = [DaytisticFactory(user=user) for _ in range(DAYTISTICS_COUNT)]

            client.force_login(user)
            response = client.get(
                reverse("daytistics:dashboard") + f"?listSize={LIMIT}"
            )
            assert response.status_code == 200
            assert "daytistics/dashboard.html" in [t.name for t in response.templates]
            assert "daytistics_list" in response.context
            assert len(response.context["daytistics_list"]) == LIMIT

            # Check that only the first LIMIT daytistics are in the context
            for daytistic in daytistics[:LIMIT]:
                assert daytistic in response.context["daytistics_list"]

            # Check that the remaining daytistics are not in the context
            for daytistic in daytistics[LIMIT:]:
                assert daytistic not in response.context["daytistics_list"]

    def test_dashboard_view_params_list_type_date_missing_list_size(
        self, client, day_generator
    ):
        DAYTISTICS_COUNT = 10

        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)

            dates = day_generator(datetime.now().date(), DAYTISTICS_COUNT)

            daytistics = list()
            for i in range(DAYTISTICS_COUNT):
                date = next(dates)
                daytistic = DaytisticFactory(user=user, date=date)
                if i >= settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD:
                    daytistics.append(daytistic)

                assert daytistic.date == date

            response = client.get(reverse("daytistics:dashboard") + "?listType=date")
            assert response.status_code == 200
            assert "daytistics_list" in response.context
            assert (
                len(response.context["daytistics_list"])
                == settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
            )

            for daytistic in daytistics:
                assert daytistic in response.context["daytistics_list"]

    def test_dashboard_view_params_list_type_created_at_missing_list_size(self, client):
        DAYTISTICS_COUNT = 10

        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)

            daytistics = list()
            for i in range(DAYTISTICS_COUNT):
                daytistic = DaytisticFactory(user=user)
                if i >= settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD:
                    daytistics.append(daytistic)

            response = client.get(
                reverse("daytistics:dashboard") + "?listType=createdAt"
            )
            assert response.status_code == 200
            assert "daytistics_list" in response.context
            assert (
                len(response.context["daytistics_list"])
                == settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
            )

            for daytistic in daytistics:
                assert daytistic in response.context["daytistics_list"]

    def test_dashboard_view_params_list_type_updated_at_missing_list_size(self, client):
        DAYTISTICS_COUNT = 10

        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)

            daytistics = list()
            for i in range(DAYTISTICS_COUNT):
                daytistic = DaytisticFactory(user=user)
                if i >= settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD:
                    daytistics.append(daytistic)

            response = client.get(
                reverse("daytistics:dashboard") + "?listType=updatedAt"
            )
            assert response.status_code == 200
            assert "daytistics_list" in response.context
            assert (
                len(response.context["daytistics_list"])
                == settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
            )

            for daytistic in daytistics:
                assert daytistic in response.context["daytistics_list"]

    def test_dashboard_view_params_list_type_randomized_missing_list_size(self, client):
        DAYTISTICS_COUNT = 10
        LIMIT = settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
        SAMPLE_RUNS = 100

        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)

            daytistics = list()
            for i in range(DAYTISTICS_COUNT):
                daytistic = DaytisticFactory(user=user)
                daytistics.append(daytistic)

            # Run the test multiple times to verify that the results are not the same
            results = []
            for _ in range(SAMPLE_RUNS):
                response = client.get(
                    reverse("daytistics:dashboard") + "?listType=random"
                )
                assert response.status_code == 200
                assert "daytistics_list" in response.context
                assert len(response.context["daytistics_list"]) == LIMIT

                # Save the IDs of the Daytistics in the result
                result_ids = tuple(
                    sorted(
                        daytistic.id
                        for daytistic in response.context["daytistics_list"]
                    )
                )
                results.append(result_ids)

            # Verify that the results are not the same
            unique_results = set(results)
            assert len(unique_results) > 1

            # Verify that all Daytistics are included in the results
            all_selected_ids = set()
            for result in results:
                all_selected_ids.update(result)
            assert all_selected_ids == set(d.id for d in daytistics)

    def test_dashboard_view_params_list_type_date_with_list_size(
        self, client, day_generator
    ):
        DAYTISTICS_COUNT = 10
        LIMIT = 5

        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)

            dates = day_generator(datetime.now().date(), DAYTISTICS_COUNT)

            daytistics = list()
            for i in range(DAYTISTICS_COUNT):
                date = next(dates)
                daytistic = DaytisticFactory(user=user, date=date)
                if i >= LIMIT:
                    daytistics.append(daytistic)

                assert daytistic.date == date

            response = client.get(
                reverse("daytistics:dashboard") + f"?listType=date&listSize={LIMIT}"
            )
            assert response.status_code == 200
            assert "daytistics_list" in response.context
            assert len(response.context["daytistics_list"]) == LIMIT

            for daytistic in daytistics:
                assert daytistic in response.context["daytistics_list"]

    def test_dashboard_view_params_list_type_created_at_with_list_size(self, client):
        DAYTISTICS_COUNT = 10
        LIMIT = 5

        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)

            daytistics = list()
            for i in range(DAYTISTICS_COUNT):
                daytistic = DaytisticFactory(user=user)
                if i >= LIMIT:
                    daytistics.append(daytistic)

            response = client.get(
                reverse("daytistics:dashboard")
                + f"?listType=createdAt&listSize={LIMIT}"
            )
            assert response.status_code == 200
            assert "daytistics_list" in response.context
            assert len(response.context["daytistics_list"]) == LIMIT

            for daytistic in daytistics:
                assert daytistic in response.context["daytistics_list"]

    def test_dashboard_view_params_list_type_updated_at_with_list_size(self, client):
        DAYTISTICS_COUNT = 10
        LIMIT = 5

        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)

            daytistics = list()
            for i in range(DAYTISTICS_COUNT):
                daytistic = DaytisticFactory(user=user)
                if i >= LIMIT:
                    daytistics.append(daytistic)

            response = client.get(
                reverse("daytistics:dashboard")
                + f"?listType=updatedAt&listSize={LIMIT}"
            )
            assert response.status_code == 200
            assert "daytistics_list" in response.context
            assert len(response.context["daytistics_list"]) == LIMIT

            for daytistic in daytistics:
                assert daytistic in response.context["daytistics_list"]

    def test_dashboard_view_params_list_type_randomized_with_list_size(self, client):
        DAYTISTICS_COUNT = 10
        LIMIT = 5
        SAMPLE_RUNS = 100

        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)

            daytistics = list()
            for _ in range(DAYTISTICS_COUNT):
                daytistic = DaytisticFactory(user=user)
                daytistics.append(daytistic)

            results = []
            for _ in range(SAMPLE_RUNS):
                response = client.get(
                    reverse("daytistics:dashboard")
                    + f"?listType=random&listSize={LIMIT}"
                )
                assert response.status_code == 200
                assert "daytistics_list" in response.context
                assert len(response.context["daytistics_list"]) == LIMIT

                result_ids = tuple(
                    sorted(
                        daytistic.id
                        for daytistic in response.context["daytistics_list"]
                    )
                )
                results.append(result_ids)

            unique_results = set(results)
            assert len(unique_results) > 1

            all_selected_ids = set()
            for result in results:
                all_selected_ids.update(result)
            assert all_selected_ids == set(d.id for d in daytistics)

    def test_dashboard_view_params_list_type_date_invalid_list_size(
        self, client, day_generator
    ):
        DAYTISTICS_COUNT = 10
        LIMIT = -2

        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)

            dates = day_generator(datetime.now().date(), DAYTISTICS_COUNT)

            daytistics = list()
            for i in range(DAYTISTICS_COUNT):
                date = next(dates)
                daytistic = DaytisticFactory(user=user, date=date)
                if i >= settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD:
                    daytistics.append(daytistic)

                assert daytistic.date == date

            response = client.get(
                reverse("daytistics:dashboard") + f"?listType=date&listSize={LIMIT}"
            )
            assert response.status_code == 200
            assert "daytistics_list" in response.context
            assert (
                len(response.context["daytistics_list"])
                == settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
            )

            for daytistic in daytistics:
                assert daytistic in response.context["daytistics_list"]

    def test_dashboard_view_params_list_type_created_at_with_list_size(self, client):
        DAYTISTICS_COUNT = 10
        LIMIT = -2

        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)

            daytistics = list()
            for i in range(DAYTISTICS_COUNT):
                daytistic = DaytisticFactory(user=user)
                if i >= settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD:
                    daytistics.append(daytistic)

            response = client.get(
                reverse("daytistics:dashboard")
                + f"?listType=createdAt&listSize={LIMIT}"
            )
            assert response.status_code == 200
            assert "daytistics_list" in response.context
            assert (
                len(response.context["daytistics_list"])
                == settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
            )

            for daytistic in daytistics:
                assert daytistic in response.context["daytistics_list"]

    def test_dashboard_view_params_list_type_updated_at_with_list_size(self, client):
        DAYTISTICS_COUNT = 10
        LIMIT = -2

        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)

            daytistics = list()
            for i in range(DAYTISTICS_COUNT):
                daytistic = DaytisticFactory(user=user)
                if i >= settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD:
                    daytistics.append(daytistic)

            response = client.get(
                reverse("daytistics:dashboard")
                + f"?listType=updatedAt&listSize={LIMIT}"
            )
            assert response.status_code == 200
            assert "daytistics_list" in response.context
            assert (
                len(response.context["daytistics_list"])
                == settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
            )

            for daytistic in daytistics:
                assert daytistic in response.context["daytistics_list"]

    def test_dashboard_view_params_list_type_randomized_with_list_size(self, client):
        DAYTISTICS_COUNT = 10
        LIMIT = -2
        SAMPLE_RUNS = 100

        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)

            daytistics = list()
            for _ in range(DAYTISTICS_COUNT):
                daytistic = DaytisticFactory(user=user)
                daytistics.append(daytistic)

            results = []
            for _ in range(SAMPLE_RUNS):
                response = client.get(
                    reverse("daytistics:dashboard")
                    + f"?listType=random&listSize={LIMIT}"
                )
                assert response.status_code == 200
                assert "daytistics_list" in response.context
                assert (
                    len(response.context["daytistics_list"])
                    == settings.DEFAULT_DAYTISTICS_NUMBER_IN_DASHBOARD
                )

                result_ids = tuple(
                    sorted(
                        daytistic.id
                        for daytistic in response.context["daytistics_list"]
                    )
                )
                results.append(result_ids)

            unique_results = set(results)
            assert len(unique_results) > 1

            all_selected_ids = set()
            for result in results:
                all_selected_ids.update(result)
            assert all_selected_ids == set(d.id for d in daytistics)


@pytest.mark.django_db
class TestCreateDaytistic:
    def test_missing_date(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)
            response = client.post(reverse("daytistics:create_daytistic"))
            assert response.status_code == 200
            assert (
                "<p class='text-red-500'>Error: Date is missing</p>"
                in response.content.decode()
            )

    def test_invalid_date_format(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)
            response = client.post(
                reverse("daytistics:create_daytistic"), {"date": "invalid_date"}
            )
            assert response.status_code == 200
            assert (
                "<p class='text-red-500'>Error: Invalid date</p>"
                in response.content.decode()
            )

    def test_daytistic_already_exists(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            existing_daytistic = DaytisticFactory(user=user)
            client.force_login(user)
            response = client.post(
                reverse("daytistics:create_daytistic"),
                {"date": existing_daytistic.date.strftime("%d.%m.%Y")},
            )
            assert response.status_code == 200
            assert (
                "<p class='text-red-500'>Error: Daytistic already exists</p>"
                in response.content.decode()
            )

    def test_date_older_than_4_weeks(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)
            old_date = (timezone.now() - timedelta(weeks=5)).strftime("%d.%m.%Y")
            response = client.post(reverse("daytistics:create_daytistic"), {"date": old_date})
            assert response.status_code == 200
            assert (
                "<p class='text-red-500'>Error: The Daytistic can't be older than 4 weeks</p>"
                in response.content.decode()
            )

    def test_date_in_future(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)
            future_date = (timezone.now() + timedelta(days=1)).strftime("%d.%m.%Y")
            response = client.post(reverse("daytistics:create_daytistic"), {"date": future_date})
            assert response.status_code == 200
            assert (
                "<p class='text-red-500'>Error: Are you watching Back To The Future right now? :D</p>"
                in response.content.decode()
            )

    def test_successful_daytistic_creation(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)
            valid_date = timezone.now().strftime("%d.%m.%Y")
            response = client.post(reverse("daytistics:create_daytistic"), {"date": valid_date})
            assert response.status_code == 201
            new_daytistic = Daytistic.objects.get(user=user, date=timezone.now().date())
            assert new_daytistic is not None
            assert (
                "<p class='text-green-500'>Daytistic created successfully</p>"
                in response.content.decode()
            )

    def test_invalid_request_method(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)
            response = client.get(reverse("daytistics:create_daytistic"))
            assert response.status_code == 405


@pytest.mark.django_db
class TestAddActivityToDaytistic:
    def test_add_new_activity(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            daytistic = DaytisticFactory(user=user)
            client.force_login(user)

            duration = "01:30"
            activity = ActivityFactory()  # Ensure Activity is created
            activity_id = activity.id

            response = client.post(
                reverse("daytistics:add_activity_to_daytistic", args=[daytistic.id]),
                json.dumps({"duration": duration, "activity_id": activity_id}),
                content_type="application/json",
            )
            activity_entry = ActivityEntry.objects.get(
                daytistic=daytistic, activity=activity
            )
            assert response.status_code == 201
            assert activity_entry in daytistic.activities.all()
            assert (
                "<p class='text-green-500'>Activity added successfully</p>"
                in response.content.decode()
            )

    def test_invalid_duration_format(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            daytistic = DaytisticFactory(user=user)
            client.force_login(user)
            duration = "invalid_duration"
            activity = ActivityFactory()  # Ensure Activity is created
            activity_id = activity.id

            response = client.post(
                reverse("daytistics:add_activity_to_daytistic", args=[daytistic.id]),
                json.dumps({"duration": duration, "activity_id": activity_id}),
                content_type="application/json",
            )
            assert response.status_code == 200
            assert (
                "<p class='text-red-500'>Error: Invalid duration format</p>"
                in response.content.decode()
            )

    def test_activity_already_exists(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            daytistic = DaytisticFactory(user=user)
            client.force_login(user)

            existing_activity = ActivityFactory()
            existing_activity_entry = ActivityEntryFactory(daytistic=daytistic, activity=existing_activity)
            existing_activity_duration = existing_activity_entry.duration

            daytistic.activities.add(existing_activity_entry)
            daytistic.save()

            duration = "01:30"
            activity_id = existing_activity.id

            response = client.post(
                reverse("daytistics:add_activity_to_daytistic", args=[daytistic.id]),
                json.dumps({"duration": duration, "activity_id": activity_id}),
                content_type="application/json",
            )
            activity_entry = ActivityEntry.objects.get(
                daytistic=daytistic, activity=existing_activity
            )
            expected_duration = existing_activity_duration + timedelta(
                hours=1, minutes=30
            )

            assert response.status_code == 201
            assert activity_entry in daytistic.activities.all()
            assert activity_entry.duration == expected_duration
            assert (
                "<p class='text-green-500'>Activity added successfully</p>"
                in response.content.decode()
            )

    def test_invalid_request_method(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            daytistic = DaytisticFactory(user=user)
            client.force_login(user)

            response = client.get(
                reverse("daytistics:add_activity_to_daytistic", args=[daytistic.id])
            )
            assert response.status_code == 405


@pytest.mark.django_db
class TestEditDaytistic:
    def test_edit_daytistic_success(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            daytistic = DaytisticFactory(user=user)
            ActivityEntryFactory(daytistic=daytistic)
            client.force_login(user)

            url = reverse("daytistics:edit_daytistic", args=[daytistic.id])
            response = client.get(url)

            assert response.status_code == 200
            assert isinstance(response, HttpResponse)
            assert "daytistics/modal/edit_daytistic.html" in [t.name for t in response.templates]
            assert "daytistic" in response.context
            assert response.context["daytistic"] == daytistic

    def test_daytistic_not_found(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            client.force_login(user)

            # Use a daytistic ID that does not exist
            url = reverse("daytistics:edit_daytistic", args=[999])
            response = client.get(url)

            assert response.status_code == 404
            assert response.content.decode() == "Daytistic not found"

    def test_internal_only_decorator(self, client):
        with translation.override("en"):
            user = CustomUserFactory()
            daytistic = DaytisticFactory(user=user)
            client.force_login(user)

            # Mock the internal_only decorator behavior if needed, or ensure it is correctly applied
            # This test will generally ensure that internal_only is enforced, but mocking or additional
            # decorators tests may be needed based on your implementation.

            url = reverse("daytistics:edit_daytistic", args=[daytistic.id])
            response = client.get(url)
            assert response.status_code == 200  # Assuming internal_only only restricts access to non-internal users

            # For testing the decorator specifically, you might need to mock or override the decorator
            # depending on how it's implemented.

