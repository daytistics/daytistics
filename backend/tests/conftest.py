from fastapi import FastAPI
import pytest
from unittest.mock import patch

from sqlmodel import create_engine, Session, SQLModel, StaticPool


from daytistics.integrations.graphql import schema
from daytistics.integrations.database import Database

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager


@pytest.fixture
def gql_schema():
    return schema


@pytest.fixture(scope="session", autouse=True)
def app() -> FastAPI:
    from daytistics.main import app

    return app
