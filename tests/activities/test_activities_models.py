import pytest
from tests.factories import ActivityFactory, CustomUserFactory

@pytest.mark.django_db
class TestActivityModel:
    
    def test_activity_creation_non_global(self):
        activity = ActivityFactory()
        assert activity.name
        assert activity.is_global == False

    def test_activity_creation_global(self):
        activity = ActivityFactory(is_global=True)
        assert activity.name
        assert activity.is_global == True

    def test_activity_str(self):
        activity = ActivityFactory()
        assert str(activity) == activity.name

    def test_activity_users(self):
        activity = ActivityFactory()
        user = CustomUserFactory()

        activity.users.add(user)

        assert activity.users.count() == 1
        assert activity.users.first() == user

