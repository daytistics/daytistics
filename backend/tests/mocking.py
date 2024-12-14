from unittest.mock import patch

from sqlmodel import SQLModel


from daytistics.integrations.database import Database

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager


@asynccontextmanager
async def _async_session(*args, **kwargs):
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with AsyncSession(engine) as session:
        try:
            yield session
        finally:
            # Clean up the whole database after the test
            await session.close()


mock_db_context = patch.object(Database, "get_async_session", _async_session)
