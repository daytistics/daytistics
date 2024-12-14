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

from tests.mocking import mock_db_context


@pytest.mark.asyncio
class TestRegisterUserMutation:
    async def test_register_user_mutation(self, gql_schema: Schema):
        with mock_db_context:
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
