import pytest
from django.test import Client
from django.urls import reverse
from tests.factories import ActivityFactory

@pytest.mark.django_db
class TestAvailableActivitiesView:
        
        def test_invalid_request_method(self, client):
            response = client.post(reverse('available_activities'), follow=True)
            assert response.status_code == 405

        def test_valid_request_method(self, client):
            response = client.get(reverse('available_activities'), follow=True)
            assert response.status_code == 200
