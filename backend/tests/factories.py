from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from daytistics.apps.auth.models import User


class UserFactory(SQLAlchemyFactory[User]):
    __model__ = User
