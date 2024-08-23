from tests.factories import CustomUserFactory, ActivityFactory, DaytisticFactory, ActivityEntryFactory
import pytest
from datetime import datetime 

@pytest.fixture
def global_activity():
    return ActivityFactory(is_global=True)

@pytest.mark.django_db
def test_custom_user_creation():
        user = CustomUserFactory()
        assert user.pk is not None

@pytest.mark.django_db
def test_get_todays_activities_with_daytistic(custom_user):
    today = datetime.now().date()
    activity_entry = ActivityEntryFactory()
    daytistic = DaytisticFactory(user=custom_user, date=today)
    daytistic.activities.add(activity_entry)

    todays_activities = custom_user.get_todays_activities()
    assert todays_activities is not None
    assert activity_entry in todays_activities.all()

@pytest.mark.django_db
def test_get_todays_activities_without_daytistic(custom_user):
    todays_activities = custom_user.get_todays_activities()
    assert todays_activities is None

@pytest.mark.django_db
def test_global_activities_added_on_user_creation(global_activity):
    user = CustomUserFactory()
    assert global_activity in user.activities.all()

@pytest.mark.django_db
def test_non_global_activities_not_added_on_user_creation():
    non_global_activity = ActivityFactory()
    user = CustomUserFactory()
    assert non_global_activity not in user.activities.all()


