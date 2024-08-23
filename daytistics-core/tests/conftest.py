from pytest_factoryboy import register
import pytest
from tests.factories import ActivityFactory, DaytisticFactory, CustomUserFactory, ActivityEntryFactory
import os

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