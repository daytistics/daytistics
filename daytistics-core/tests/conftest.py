from pytest_factoryboy import register
import pytest
from tests.factories import (
    ActivityFactory,
    DaytisticFactory,
    CustomUserFactory,
    ActivityEntryFactory,
)
import random
from datetime import timedelta

register(ActivityFactory)
register(DaytisticFactory)
register(CustomUserFactory)
register(ActivityEntryFactory)


@pytest.fixture
def custom_user():
    return CustomUserFactory()


@pytest.fixture
def client():
    from django.test import Client

    return Client()


@pytest.fixture
def day_generator():
    def generate_days(start_date, n):
        current_date = start_date
        for _ in range(n):
            days_to_jump = random.randint(1, 10)
            current_date += timedelta(days=days_to_jump)
            yield current_date

    return generate_days
