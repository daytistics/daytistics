import pytest
from unittest.mock import patch
from contextlib import asynccontextmanager

from daytistics.integrations.database import Database

from strawberry import Schema

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager


@pytest.mark.asyncio
class TestRegisterUserMutation:
    async def test_register_user_mutation(self, gql_schema: Schema):
        # Mock the async context manager behavior
        @asynccontextmanager
        async def async_session(*args, **kwargs):
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

        with patch.object(Database, "get_async_session", async_session):
            variables = {
                "user": {
                    "email": "john.doe@example.com",
                    "password": "password",
                    "username": "johndoe",
                }
            }

            query = """#graphql 
                mutation RegisterUser($user: UserRegistrationInput!) {
                    registerUser(user: $user) {
                        email
                        username
                        isVerified
                    }
                }
            """

            result = await gql_schema.execute(query, variable_values=variables)
            assert result.data == {
                "registerUser": {
                    "email": variables["user"]["email"],
                    "username": variables["user"]["username"],
                    "isVerified": False,
                }
            }
