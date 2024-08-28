from tests.factories import (
    CustomUserFactory,
    ActivityFactory,
    DaytisticFactory,
    ActivityEntryFactory,
)
import pytest
from datetime import timedelta, datetime
import random
from app.daytistics.models import Daytistic


@pytest.fixture
def global_activity():
    return ActivityFactory(is_global=True)


@pytest.mark.django_db
class TestCustomUser:
    def test_custom_user_creation(self):
        user = CustomUserFactory()
        assert user.pk is not None

    def test_all_activities(self):
        user = CustomUserFactory()
        global_activity = ActivityFactory(is_global=True)
        non_global_activity = ActivityFactory()

        user.activities.add(non_global_activity)

        all_activities = user.all_activities

        assert global_activity in all_activities
        assert non_global_activity in all_activities

    def test_global_activities_added_on_user_creation(self, global_activity):
        user = CustomUserFactory()
        assert global_activity in user.activities.all()

    def test_non_global_activities_not_added_on_user_creation(self):
        non_global_activity = ActivityFactory()
        user = CustomUserFactory()
        assert non_global_activity not in user.activities.all()

    def test_get_daytistics_by_time_updated_no_limit(self):
        DAYTISTICS_COUNT = 10

        user = CustomUserFactory()
        daytistics = [DaytisticFactory(user=user) for _ in range(DAYTISTICS_COUNT)]

        assert Daytistic.objects.all().count() == DAYTISTICS_COUNT

        user_daytistics = user.get_daytistics_by_time_updated()

        assert len(user_daytistics) == DAYTISTICS_COUNT

        for daytistic in daytistics:
            assert daytistic in user_daytistics

    def test_get_daytistics_by_time_updated_with_limit(self):
        DAYTISTICS_COUNT = 10
        LIMIT = 5

        user = CustomUserFactory()

        daytistics = list()
        for i in range(DAYTISTICS_COUNT):
            daytistic = DaytisticFactory(user=user)
            if i >= LIMIT:
                daytistics.append(daytistic)

        assert Daytistic.objects.all().count() == DAYTISTICS_COUNT

        user_daytistics = user.get_daytistics_by_time_updated(LIMIT)

        assert len(user_daytistics) == LIMIT

        for daytistic in user_daytistics:
            assert daytistic in daytistics

    def test_get_daytistics_by_time_created_no_limit(self):
        DAYTISTICS_COUNT = 10

        user = CustomUserFactory()
        daytistics = [DaytisticFactory(user=user) for _ in range(DAYTISTICS_COUNT)]

        assert Daytistic.objects.all().count() == DAYTISTICS_COUNT

        user_daytistics = user.get_daytistics_by_time_created()

        assert len(user_daytistics) == DAYTISTICS_COUNT

        for daytistic in daytistics:
            assert daytistic in user_daytistics

    def test_get_daytistics_by_time_created_with_limit(self):
        DAYTISTICS_COUNT = 10
        LIMIT = 5

        user = CustomUserFactory()

        daytistics = list()
        for i in range(DAYTISTICS_COUNT):
            daytistic = DaytisticFactory(user=user)
            if i >= LIMIT:
                daytistics.append(daytistic)

        assert Daytistic.objects.all().count() == DAYTISTICS_COUNT

        user_daytistics = user.get_daytistics_by_time_created(LIMIT)

        assert len(user_daytistics) == LIMIT

        for daytistic in user_daytistics:
            assert daytistic in daytistics

    def test_get_daytistics_by_time_created_with_invalid_limit(self):
        LIMIT = -3

        user = CustomUserFactory()

        with pytest.raises(ValueError):
            user_daytistics = user.get_daytistics_by_time_created(LIMIT)

    def test_get_daytistics_by_time_updated_with_invalid_limit(self):
        LIMIT = -3

        user = CustomUserFactory()

        with pytest.raises(ValueError):
            user_daytistics = user.get_daytistics_by_time_updated(LIMIT)

    def test_get_daytistics_randomized_invalid_limit(self):
        LIMIT = -1

        user = CustomUserFactory()

        with pytest.raises(ValueError):
            user_daytistics = user.get_daytistics_randomized(LIMIT)

    def test_get_daytistics_randomized_with_large_limit(self):
        LIMIT = 11
        DAYTISTICS_COUNT = 10

        user = CustomUserFactory()

        daytistics = list()
        for i in range(DAYTISTICS_COUNT):
            daytistic = DaytisticFactory(user=user)
            if i >= LIMIT:
                daytistics.append(daytistic)

        user_daytistics = user.get_daytistics_randomized(limit=LIMIT)

        assert len(user_daytistics) == DAYTISTICS_COUNT

        for daytistic in daytistics:
            assert daytistic in user_daytistics

    def test_get_daytistics_by_date_with_limit(self, day_generator):
        LIMIT = 5
        DAYTISTICS_COUNT = 10

        user = CustomUserFactory()

        daytistics = list()

        dates = day_generator(datetime.now().date(), DAYTISTICS_COUNT)

        for i in range(DAYTISTICS_COUNT):
            date = next(dates)
            daytistic = DaytisticFactory(user=user, date=date)
            if i >= LIMIT:
                daytistics.append(daytistic)

            assert daytistic.date == date

        user_daytistics = user.get_daytistics_by_date(LIMIT)

        assert len(user_daytistics) == LIMIT

        for daytistic in user_daytistics[LIMIT:]:
            assert daytistic in user_daytistics

    def test_get_daytistics_by_date_no_limit(self, day_generator):
        LIMIT = -1
        DAYTISTICS_COUNT = 10

        user = CustomUserFactory()

        daytistics = list()

        dates = day_generator(datetime.now().date(), DAYTISTICS_COUNT)

        for i in range(DAYTISTICS_COUNT):
            date = next(dates)
            daytistic = DaytisticFactory(user=user, date=date)
            if i >= LIMIT:
                daytistics.append(daytistic)

            assert daytistic.date == date

        user_daytistics = user.get_daytistics_by_date(LIMIT)

        assert len(user_daytistics) == DAYTISTICS_COUNT

        for daytistic in daytistics:
            assert daytistic in user_daytistics

    def test_get_daytistics_by_date_invalid_limit(self):
        LIMIT = -2

        user = CustomUserFactory()

        with pytest.raises(ValueError):
            user_daytistics = user.get_daytistics_by_date(LIMIT)
