import pytest
from pytest_factoryboy import register
from django.conf import settings
from ninja.testing import TestClient
from faker import Faker

import tests.factories as factories


register(factories.CustomUserFactory)
register(factories.DaytisticFactory)

fake = Faker()


@pytest.fixture()
def users_client():
    from daytistics.core.api import users_router

    client = TestClient(users_router)
    return client


@pytest.fixture()
def daytistics_client():
    from daytistics.core.api import daytistics_router

    return TestClient(daytistics_router)


@pytest.fixture()
def activities_client():
    from daytistics.core.api import activities_router

    return TestClient(activities_router)


@pytest.fixture()
def timezone():
    return "Europe/Athens"


@pytest.fixture()
def default_activities():
    default_categories = [fake.word() for _ in range(3)]
    default_activities = {
        default_categories[0]: [fake.word() for _ in range(3)],
        default_categories[1]: [fake.word() for _ in range(3)],
        default_categories[2]: [fake.word() for _ in range(3)],
    }

    from daytistics.activities.models import ActivityCategory, ActivityType

    activities = []

    for key, value in default_activities.items():
        category, _ = ActivityCategory.objects.get_or_create(name=key)

        for activity in value:
            activity = ActivityType.objects.get_or_create(
                name=activity, category=category
            )
            activities.append(activity)

    assert len(activities) == 9
    assert len(default_categories) == 3
    assert len(default_activities) == 3
    assert len(default_activities[default_categories[0]]) == 3
    assert len(default_activities[default_categories[1]]) == 3
    assert len(default_activities[default_categories[2]]) == 3

    return activities
