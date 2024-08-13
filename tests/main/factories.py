import factory
from django.contrib.auth import get_user_model
from daytistics.models import Activity

class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Activity

    name = factory.Faker('word')
    is_global = factory.Faker('boolean')

class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password')

    @factory.post_generation
    def activities(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for activity in extracted:
                self.activities.add(activity)