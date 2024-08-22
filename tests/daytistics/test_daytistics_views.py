import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from daytistics.models import Daytistic
from django.test import Client
from tests.factories import CustomUserFactory, DaytisticFactory

@pytest.mark.django_db
class TestDashboardView:

    def test_dashboard_view_redirects_for_anonymous_user(self, client):
        response = client.get(reverse('daytistics_dashboard'))
        assert response.status_code == 302  # Redirect to login

    def test_dashboard_view_renders_for_logged_in_user(self, client):
        user = CustomUserFactory()
        client.force_login(user)
        response = client.get(reverse('daytistics_dashboard'))
        assert response.status_code == 200
        assert 'pages/daytistics/dashboard.html' in [t.name for t in response.templates]


@pytest.mark.django_db
class TestCreateDaytistic:

    def test_missing_date(self, client):
        user = CustomUserFactory()
        client.force_login(user)
        response = client.post(reverse('daytistics_create'))
        assert response.status_code == 400
        assert "<p class='text-red-500'>Error: Date is missing</p>" in response.content.decode()

    def test_invalid_date_format(self, client):
        user = CustomUserFactory()
        client.force_login(user)
        response = client.post(reverse('daytistics_create'), {'date': 'invalid_date'})
        assert response.status_code == 400
        assert "<p class='text-red-500'>Error: Invalid date</p>" in response.content.decode()

    def test_daytistic_already_exists(self, client):
        user = CustomUserFactory()
        existing_daytistic = DaytisticFactory(user=user)
        client.force_login(user)
        response = client.post(reverse('daytistics_create'), {'date': existing_daytistic.date.strftime('%d.%m.%Y')})
        assert response.status_code == 400
        assert "<p class='text-red-500'>Error: Daytistics already exists</p>" in response.content.decode()

    def test_date_older_than_4_weeks(self, client):
        user = CustomUserFactory()
        client.force_login(user)
        old_date = (timezone.now() - timedelta(weeks=5)).strftime('%d.%m.%Y')
        response = client.post(reverse('daytistics_create'), {'date': old_date})
        assert response.status_code == 400
        assert "<p class='text-red-500'>Error: The daytistic can't be older than 4 weeks</p>" in response.content.decode()

    def test_date_in_future(self, client):
        user = CustomUserFactory()
        client.force_login(user)
        future_date = (timezone.now() + timedelta(days=1)).strftime('%d.%m.%Y')
        response = client.post(reverse('daytistics_create'), {'date': future_date})
        assert response.status_code == 400
        assert "<p class='text-red-500'>Error: The daytistic can't be in the future</p>" in response.content.decode()

    def test_successful_daytistic_creation(self, client):
        user = CustomUserFactory()
        client.force_login(user)
        valid_date = timezone.now().strftime('%d.%m.%Y')
        response = client.post(reverse('daytistics_create'), {'date': valid_date})
        assert response.status_code == 302  # Should redirect
        new_daytistic = Daytistic.objects.get(user=user, date=timezone.now().date())
        assert new_daytistic is not None
        assert response['HX-Redirect'] == reverse('daytistics_edit', args=[new_daytistic.id])

    def test_invalid_request_method(self, client):
        user = CustomUserFactory()
        client.force_login(user)
        response = client.get(reverse('daytistics_create'))
        assert response.status_code == 400
        assert "<p class='text-red-500'>Error: Invalid request</p>" in response.content.decode()
