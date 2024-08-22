import pytest
from datetime import timedelta
from daytistics.models import ActivityEntry, Daytistic
from tests.factories import CustomUserFactory, ActivityFactory, ActivityEntryFactory, DaytisticFactory
from django.utils import timezone

@pytest.mark.django_db
class TestActivityEntryModel:
    @pytest.fixture
    def activity_entry(self):
        user = CustomUserFactory()
        activity = ActivityFactory()
        return ActivityEntryFactory(user=user, activity=activity)

    def test_activity_entry_creation(self, activity_entry):
        assert isinstance(activity_entry, ActivityEntry)
        assert activity_entry.user is not None
        assert activity_entry.activity is not None
        assert isinstance(activity_entry.duration, timedelta)

    def test_duration_in_seconds(self, activity_entry):
        activity_entry.duration = timedelta(minutes=30)
        assert activity_entry.duration_in_seconds() == 1800

    def test_auto_now_fields(self, activity_entry):
        old_created_at = activity_entry.created_at
        old_updated_at = activity_entry.updated_at
        
        activity_entry.duration = timedelta(minutes=45)
        activity_entry.save()
        
        assert activity_entry.created_at == old_created_at
        assert activity_entry.updated_at > old_updated_at

@pytest.mark.django_db
class TestDaytisticModel:
    @pytest.fixture
    def daytistic(self):
        user = CustomUserFactory()
        return DaytisticFactory(user=user)

    @pytest.fixture
    def activity_entry(self, daytistic):
        return ActivityEntryFactory(user=daytistic.user)

    def test_daytistic_creation(self, daytistic):
        assert isinstance(daytistic, Daytistic)
        assert daytistic.user is not None
        assert isinstance(daytistic.date, timezone.datetime)

    def test_add_activity_entry(self, daytistic, activity_entry):
        daytistic.activities.add(activity_entry)
        assert activity_entry in daytistic.activities.all()

    def test_multiple_activity_entries(self, daytistic, activity_entry):
        activity_entry_2 = ActivityEntryFactory(user=daytistic.user)
        daytistic.activities.add(activity_entry, activity_entry_2)
        assert daytistic.activities.count() == 2

    def test_date_field(self):
        specific_date = timezone.now().date()
        user = CustomUserFactory()
        daytistic_with_date = DaytisticFactory(user=user, date=specific_date)
        assert daytistic_with_date.date == specific_date