from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from contextlib import asynccontextmanager
import os


class Database:
    def __init__(self) -> None:
        self.engine = None

    def connect(self) -> None | AsyncEngine:
        if not self.engine:
            try:
                self.engine = create_async_engine(
                    os.environ.get("DATABASE_URL", "sqlite:///db.sqlite")
                )
            except Exception as exception:
                self.engine = None
                raise exception
        else:
            return self.engine

    @asynccontextmanager
    async def get_async_session(self):
        if not self.engine:
            raise ConnectionError("Database is not connected")

        async with AsyncSession(self.engine) as session:
            try:
                yield session
            except Exception as exception:
                await session.rollback()
                raise exception
            finally:
                await session.close()
