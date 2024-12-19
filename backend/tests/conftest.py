import os
import pkgutil
from collections.abc import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
import aioinject
import dotenv

from daytistics.libs.graphql import schema
from daytistics.libs.container import create_container
from daytistics.libs.database import async_session_factory

from tests.types import Resolver


from aioinject import Object
from asgi_lifespan import LifespanManager
from fastapi import FastAPI

import tests.plugins


@pytest.fixture
def client():
    return schema


dotenv.load_dotenv(".env")

pytest_plugins = [
    "anyio",
    *(
        mod.name
        for mod in pkgutil.walk_packages(
            tests.plugins.__path__,
            prefix="tests.plugins.",
        )
        if not mod.ispkg
    ),
]


@pytest.fixture(scope="session", autouse=True)
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def worker_id() -> str:
    return "main"


@pytest.fixture(scope="session")
async def http_app() -> AsyncIterator[FastAPI]:
    from daytistics.app import create_app

    app = create_app()
    async with LifespanManager(app):
        yield app  # type: ignore


@pytest.fixture(scope="session")
async def container() -> AsyncIterator[aioinject.Container]:
    async with create_container() as container:
        yield container


@pytest.fixture(autouse=True)
async def resolver(
    container: aioinject.Container,
    session: AsyncSession,
) -> AsyncIterator[Resolver]:
    with container.override(Object(session, AsyncSession)):
        async with container.context() as ctx:
            yield ctx.resolve
