from typing import cast

from daytistics.domains.users.models import User
from daytistics.domains.users.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    UserAlreadyVerifiedError,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, user: User) -> User:
        if (
            await self.session.execute(select(User).where(User.email == user.email))
        ).first():
            raise UserAlreadyExistsError

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_by_email(self, email: str) -> User:
        result = (
            await self.session.execute(select(User).where(User.email == email))
        ).first()
        if not result:
            raise UserNotFoundError
        user = result[0]
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            raise UserNotFoundError

        return user

    async def verify_user(self, user_id: int) -> User:
        user = await self.session.get(User, user_id)

        if not user:
            raise UserNotFoundError

        if user.is_verified:  # type: ignore
            raise UserAlreadyVerifiedError

        user.is_verified = True  # type: ignore
        await self.session.commit()
        await self.session.refresh(user)
        return user
