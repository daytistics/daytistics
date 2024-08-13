from tests.main.factories import ActivityFactory, CustomUserFactory
from pytest_factoryboy import register
import pytest

register(ActivityFactory)
register(CustomUserFactory)

@pytest.fixture
def test_user_with_activities(db):
    activities = ActivityFactory.create_batch(10)  
    user = CustomUserFactory(activities=activities)
    return user

@pytest.fixture
def global_activities(db):
    activities = [
        ActivityFactory(is_global=True) for _ in range(10)
    ]
    return activities