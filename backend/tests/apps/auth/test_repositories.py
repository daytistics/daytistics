import pytest

from tests.factories import UserFactory
from daytistics.apps.auth.repositories import UserRepository
from daytistics.apps.auth.exceptions import UserAlreadyExistsError


class TestUserRepository:
    @pytest.fixture
    def user_repository(self, session):
        return UserRepository(session)

    @pytest.mark.parametrize("already_exists", [True, False])
    def test_create_user(self, user_repository: UserRepository, already_exists: bool):
        user = UserFactory.build()
        if already_exists:
            user_repository.create_user(user)

            with pytest.raises(UserAlreadyExistsError):
                created_user = user_repository.create_user(user)
        else:
            created_user = user_repository.create_user(user)
            for field in user.model_fields_set:
                assert getattr(created_user, field) == getattr(user, field)
