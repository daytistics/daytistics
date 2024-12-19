from contextlib import asynccontextmanager
from typing import AsyncIterator

import aioinject
from aioinject import Provider
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)

from sqlalchemy.ext.declarative import declarative_base

from daytistics.settings import DatabaseSettings, get_settings

_settings = get_settings(DatabaseSettings)

engine = create_async_engine(
    _settings.URL,
    pool_size=20,
    pool_pre_ping=True,
    pool_use_lifo=True,
    echo=_settings.ECHO,
)
async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


@asynccontextmanager
async def create_engine() -> AsyncIterator[AsyncEngine]:
    try:
        yield engine
    except:
        await engine.dispose()
        raise


@asynccontextmanager
async def create_session(
    _: AsyncEngine,
) -> AsyncIterator[AsyncSession]:
    async with async_session_factory.begin() as session:
        yield session


providers: list[Provider] = [
    aioinject.Singleton(create_engine),
    aioinject.Scoped(create_session),
]

Base = declarative_base()
