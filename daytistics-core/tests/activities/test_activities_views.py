import pytest
from django.urls import reverse
from django.utils import translation

@pytest.mark.django_db
class TestAvailableActivitiesView:
        
        def test_invalid_request_method(self, client):
            with translation.override('en'):  # Beispiel für Englisch
                response = client.post(reverse('activities_availables_as_options_list'), follow=True)
                assert response.status_code == 405

        def test_valid_request_method(self, client):
            with translation.override('en'):
                response = client.get(reverse('activities_availables_as_options_list'), follow=True)
                assert response.status_code == 200
