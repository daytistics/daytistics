from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from contextlib import asynccontextmanager
import os


class Database:
    def __init__(self) -> None:
        self.engine = None

    def connect(self) -> None:
        if not self.engine:
            self.engine = create_async_engine(
                # "sqlite+aiosqlite:///:memory:",
                "postgresql+asyncpg://daytistics_user:daytistics_pw@database:5432/daytistics_dev"
                # os.environ.get("DATABASE_URL", "sqlite:///db.sqlite")
            )
        else:
            raise ConnectionAbortedError("Database is already connected")

    @asynccontextmanager
    async def get_async_session(self):
        if not self.engine:
            raise ConnectionError("Database is not connected")

        async with AsyncSession(self.engine) as session:
            try:
                yield session
            finally:
                await session.close()
