from typing import Annotated
from datetime import datetime, timedelta, timezone

from fastapi import Depends
from passlib.context import CryptContext
from sqlmodel import Session

from . import AuthenticationService
from ..models import User
from ..repositories import UserRepository
from ..schemas import UserRegistrationInput
from daytistics.config import SecurityConfig
from daytistics.exceptions import ConfigurationError
from daytistics.integrations.injections import container

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(
        self,
    ) -> None:
        with container.sync_context() as ctx:
            self.authentication_service = ctx.resolve(AuthenticationService)
            self.user_repository = ctx.resolve(UserRepository)

    async def register_user(self, user_input: UserRegistrationInput) -> User:
        user = User(
            username=user_input.username,
            email=user_input.email,
            hashed_password=self.authentication_service.get_password_hash(
                user_input.password
            ),
        )

        created_user = await self.user_repository.create_user(user)

        return created_user
