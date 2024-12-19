# This file is almost entirely copied from https://gitlab.com/ThirVondukr/sqlalchemy-pytest


from __future__ import annotations

import pytest
from alembic import config
from sqlalchemy.ext.asyncio import AsyncSession


from collections.abc import AsyncGenerator, AsyncIterable, AsyncIterator
from typing import TYPE_CHECKING, cast

import sqlalchemy
from sqlalchemy import Connection, make_url
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker as AsyncSessionmaker  # noqa: N812
from sqlalchemy.ext.asyncio import create_async_engine


import abc
import pathlib

from sqlalchemy import text


if TYPE_CHECKING:
    from alembic import config


def get_op(engine: AsyncEngine, connection_url: sqlalchemy.URL) -> Op:
    match engine.dialect.name:
        case "postgresql":
            return PostgresOp(engine, connection_url)
        case "sqlite":
            return SqliteOp(engine, connection_url)
        case _:
            raise NotImplementedError


class Op(abc.ABC):
    def __init__(self, engine: AsyncEngine, connection_url: sqlalchemy.URL) -> None:
        self._engine = engine
        self._connection_url = connection_url

    @property
    def _db_name(self) -> str:
        if not self._connection_url.database:
            msg = "Connection URL should have a database"
            raise ValueError(msg)

        return self._connection_url.database

    @abc.abstractmethod
    async def create_db_if_not_exists(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def drop_db(self, *, reuse_db: bool) -> None:
        raise NotImplementedError


class PostgresOp(Op):
    async def create_db_if_not_exists(self) -> None:
        async with self._engine.connect() as conn:
            exists = await conn.scalar(
                text(
                    f"SELECT 1 FROM pg_database WHERE datname='{self._db_name}'",  # noqa: S608
                ),
            )
            if not exists:
                await conn.execute(text(f'create database "{self._db_name}";'))

    async def drop_db(self, *, reuse_db: bool) -> None:
        async with self._engine.connect() as conn:
            if reuse_db:
                return
            await conn.execute(
                text(
                    f"""
                    select pg_terminate_backend(pg_stat_activity.pid)
                    from pg_stat_activity
                    where pg_stat_activity.datname = '{self._db_name}'
                    and pid <> pg_backend_pid();
                    """,  # noqa: S608
                ),
            )
            await conn.execute(text(f'drop database "{self._db_name}";'))


class SqliteOp(Op):
    async def create_db_if_not_exists(self) -> None:
        if pathlib.Path(self._db_name).exists():
            return

        async with self._engine.connect():
            pass

    async def drop_db(self, *, reuse_db: bool) -> None:
        if reuse_db:
            return
        pathlib.Path(self._db_name).unlink(missing_ok=True)


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("daytistics-pytest-sqlalchemy")
    group.addoption(
        "--reuse-db",
        dest="reuse_db",
        action="store_true",
        default=False,
    )


@pytest.fixture(scope="session")
def reuse_db(request: pytest.FixtureRequest) -> bool:
    return cast(bool, request.config.getvalue("reuse_db"))


# TODO: Add fixtures database_url and worker_id
@pytest.fixture(scope="session")
def sqlalchemy_pytest_database_url(database_url: str, worker_id: str) -> sqlalchemy.URL:
    url = make_url(database_url)
    return url.set(database=f"{url.database}-{worker_id}")


@pytest.fixture(scope="session")
async def _sqlalchemy_create_database(
    database_url: str,
    sqlalchemy_pytest_database_url: sqlalchemy.URL,
    reuse_db: bool,  # noqa: FBT001
) -> AsyncIterable[None]:
    engine = create_async_engine(
        database_url,
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    op = get_op(engine=engine, connection_url=sqlalchemy_pytest_database_url)
    await op.create_db_if_not_exists()
    yield
    await op.drop_db(reuse_db=reuse_db)


@pytest.fixture(scope="session")
async def sqlalchemy_pytest_engine(
    sqlalchemy_pytest_database_url: sqlalchemy.URL,
) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(sqlalchemy_pytest_database_url)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def _sqlalchemy_run_migrations(
    _sqlalchemy_create_database: None,
    sqlalchemy_pytest_engine: AsyncEngine,
    database_url: str,
) -> None:
    from alembic import command

    alembic_config = config.Config("backend/alembic.ini")
    alembic_config.set_main_option("script_location", "backend/alembic/")

    if alembic_config is None:
        return

    def run_upgrade(connection: Connection, cfg: config.Config) -> None:
        cfg.attributes["connection"] = connection
        command.upgrade(cfg, revision="head")

    async with sqlalchemy_pytest_engine.begin() as conn:
        alembic_config.set_main_option("sqlalchemy.url", database_url)
        await conn.run_sync(run_upgrade, alembic_config)
        await conn.commit()


@pytest.fixture
async def session(
    _sqlalchemy_run_migrations: None,
    sqlalchemy_pytest_engine: AsyncEngine,
    async_sessionmaker: AsyncSessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with sqlalchemy_pytest_engine.connect() as conn:
        transaction = await conn.begin()
        async_sessionmaker.configure(bind=conn)

        async with async_sessionmaker() as session:
            yield session

        if transaction.is_active:
            await transaction.rollback()
