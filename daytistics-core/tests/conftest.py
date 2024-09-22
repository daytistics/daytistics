from ninja.testing import TestClient
from pytest_factoryboy import register
import pytest
import tests.factories as factories
import random
from datetime import timedelta


register(factories.CustomUserFactory)
register(factories.DaytisticFactory)


@pytest.fixture()
def users_client():
    from app.config.api import users_router

    return TestClient(users_router)


@pytest.fixture()
def daytistics_client():
    from app.config.api import daytistics_router

    return TestClient(daytistics_router)


@pytest.fixture
def day_generator():
    def generate_days(start_date, n):
        current_date = start_date
        for _ in range(n):
            days_to_jump = random.randint(1, 10)
            current_date += timedelta(days=days_to_jump)
            yield current_date

    return generate_days
