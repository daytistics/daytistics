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
from rest_framework.test import APIClient
from faker import Faker
from rest_framework_simplejwt.tokens import RefreshToken

register(ActivityFactory)
register(DaytisticFactory)
register(CustomUserFactory)
register(ActivityEntryFactory)


@pytest.fixture
def api_client():
    user = CustomUserFactory()
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client

@pytest.fixture
def fake():
    return Faker()

@pytest.fixture
def day_generator():
	def generate_days(start_date, n):
		current_date = start_date
		for _ in range(n):
			days_to_jump = random.randint(1, 10)
			current_date += timedelta(days=days_to_jump)
			yield current_date

	return generate_days
