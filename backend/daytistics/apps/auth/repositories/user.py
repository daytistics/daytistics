from sqlmodel import select

from ..models import User
from ..exceptions import UserAlreadyExistsError, UserNotFoundError
from daytistics.integrations.injections import container
from daytistics.integrations.database import Database


class UserRepository:
    def __init__(self):
        with container.sync_context() as ctx:
            self.db: Database = ctx.resolve(Database)

    async def create_user(self, user: User) -> User:
        async with self.db.get_async_session() as session:
            if (
                await session.exec(select(User).where(User.email == user.email))
            ).first():
                raise UserAlreadyExistsError

            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def get_user_by_email(self, email: str) -> User:
        async with self.db.get_async_session() as session:
            user = session.exec(select(User).where(User.email == email)).first()
            if not user:
                raise UserNotFoundError
            return user

    async def toggle_user_verification(self, user: User) -> User:
        async with self.db.get_async_session() as session:
            user.is_verified = not user.is_verified
            await session.commit()
            await session.refresh(user)
            return user
