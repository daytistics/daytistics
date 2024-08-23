import factory 
from datetime import timedelta
from faker import Faker
from factory.django import DjangoModelFactory
from django.utils import timezone
from accounts.models import CustomUser
from daytistics.models import Daytistic, ActivityEntry
from activities.models import Activity

fake = Faker()

class ActivityFactory(DjangoModelFactory):
    class Meta:
        model = Activity

    name = factory.LazyFunction(lambda: fake.word())
    is_global = False

class DaytisticFactory(DjangoModelFactory):
    class Meta:
        model = Daytistic

    user = factory.SubFactory('tests.factories.CustomUserFactory')
    date = factory.LazyFunction(timezone.now)

class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.LazyFunction(lambda: fake.user_name())
    email = factory.LazyFunction(lambda: fake.email())


class ActivityEntryFactory(DjangoModelFactory):
    class Meta:
        model = ActivityEntry
    
    activity = factory.SubFactory(ActivityFactory)
    daytistic = factory.SubFactory(DaytisticFactory)
    duration = factory.LazyFunction(lambda: timedelta(minutes=fake.random_int(min=1, max=1440)))
    user = factory.SelfAttribute('daytistic.user')