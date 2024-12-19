from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from pydantic import EmailStr
from faker import Faker

from daytistics.modules.users.models import User

fake = Faker()


class UserFactory(SQLAlchemyFactory[User]):
    __model__ = User

    email: EmailStr = fake.email()
