from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from daytistics.modules.auth.models import User


fake = Faker()


class UserFactory(SQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = User

    username = fake.user_name()
    email = fake.email()
    hashed_password = "password123"
    is_active = True
    last_login = None
    is_locked: bool = False
    is_superuser = False
    is_verified = True
    created_at = fake.date_time_this_month()
    updated_at = fake.date_time_this_month()


class ModernUserFactory(SQLAlchemyFactory[User]):
    __model__ = User
