import pytest
from django.urls import reverse
from django.test import Client

@pytest.mark.django_db
def test_available_activities_view(test_user_with_activities, global_activities):
    user = test_user_with_activities

    client = Client()
    client.force_login(user)

    url = reverse('activities_list')  
    response = client.get(url)

    assert response.status_code == 200

    for activity in user.activities.all():
        assert f'<option value="{activity.id}">{activity.name}</option>' in response.content.decode()

    for activity in global_activities:
        assert f'<option value="{activity.id}">{activity.name}</option>' in response.content.decode()