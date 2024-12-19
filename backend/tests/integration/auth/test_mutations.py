from unittest.mock import patch

from strawberry import Schema
import pytest
from daytistics.domains.users.exceptions import (
    InvalidEmailError,
    InvalidPasswordError,
    InvalidUsernameError,
)


@pytest.mark.asyncio
class TestRegisterUserMutation:
    @pytest.mark.parametrize(
        "email, password, username, expected_error",
        [
            # Valid cases
            ("user@example.com", "Password1@", "username", None),  # Minimum length
            # Invalid email cases
            ("", "", "", InvalidEmailError),  # Empty email
            ("plainaddress", "", "", InvalidEmailError),  # Missing '@' symbol
            (
                "@missingusername.com",
                "",
                "",
                InvalidEmailError,
            ),  # Missing username part before '@'
            (
                "missingdomain@.com",
                "",
                "",
                InvalidEmailError,
            ),  # Missing domain name after '@'
            ("user@domain", "", "", InvalidEmailError),  # Missing dot in domain
            # Invalid password cases
            ("valid@example.com", "", "", InvalidPasswordError),  # Empty password
            (
                "valid@example.com",
                "short",
                "",
                InvalidPasswordError,
            ),  # Too short (less than 8 characters)
            (
                "valid@example.com",
                "missinguppercase",
                "",
                InvalidPasswordError,
            ),  # Missing uppercase letter
            (
                "valid@example.com",
                "MISSINGLOWERCASE",
                "",
                InvalidPasswordError,
            ),  # Missing lowercase letter
            (
                "valid@example.com",
                "Missing123",
                "",
                InvalidPasswordError,
            ),  # Missing symbol
            (
                "valid@example.com",
                "Valid1Password@",
                "",
                InvalidPasswordError,
            ),  # Correct password, this won't raise an error, so we won't test here
            # Invalid username cases
            (
                "valid@example.com",
                "Valid1Password@",
                "",
                InvalidUsernameError,
            ),  # Empty username
            (
                "valid@example.com",
                "Valid1Password@",
                "usr",
                InvalidUsernameError,
            ),  # Too short (less than 4 characters)
            (
                "valid@example.com",
                "Valid1Password@",
                "a" * 21,
                InvalidUsernameError,
            ),  # Too long (more than 20 characters)
            (
                "valid@example.com",
                "Valid1Password@",
                "user@name",
                InvalidUsernameError,
            ),  # Invalid characters (contains '@')
            (
                "valid@example.com",
                "Valid1Password@",
                "user!name",
                InvalidUsernameError,
            ),  # Invalid characters (contains '!')
        ],
    )
    async def test_register_user_mutation(
        self, client: Schema, email, password, username, expected_error, mocked_session
    ):
        # with mock_db_context:
        with patch(
            "daytistics.shared.services.MailService.send_registration_verification_email"
        ) as mock_send_email:
            variables = {
                "user": {
                    "email": email,
                    "password": password,
                    "username": username,
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

            result = await client.execute(query, variable_values=variables)

            if not expected_error:
                assert result.data == {
                    "registerUser": {
                        "email": variables["user"]["email"],
                        "username": variables["user"]["username"],
                        "isVerified": False,
                    }
                }

                assert mock_send_email.called

            elif result.errors:
                assert len(result.errors) == 1
                assert isinstance(
                    result.errors[0].original_error,
                    expected_error,
                )

            else:
                assert 1 == 0, "Something went completely wrong :D"


# @pytest.mark.asyncio
# class TestVerifyUserMutation:
#     async def test_verify_user_mutation(self, gql_schema: Schema):
#         # with mock_db_context:
#         with container.sync_context() as ctx:
#             mail_service = ctx.resolve(MailService)
#             database = ctx.resolve(Database)
#             user = UserFactory.build(is_verified=False)

#             async with database.get_async_session() as session:
#                 session.add(user)
#                 await session.commit()
#                 await session.refresh(user)

#             assert not user.is_verified
#             assert (
#                 await session.exec(select(User).where(User.email == user.email))
#             ).first() == user

#             with patch("daytistics.shared.services.MailService._send_email"):
#                 token = await mail_service.send_registration_verification_email(user)

#                 variables = {"token": token}

#                 query = """#graphql
#                     mutation VerifyUser($token: String!) {
#                         verifyUser(token: $token) {
#                             isVerified
#                         }
#                     }
#                 """

#                 result = await gql_schema.execute(query, variable_values=variables)
#                 assert result.data == {"verifyUser": {"isVerified": True}}


# @pytest.mark.asyncio
# class TestLoginUserMutation:
#     async def test_login_user_mutation(self, gql_schema: Schema):
#         # with mock_db_context:
#         with container.sync_context() as ctx:
#             database = ctx.resolve(Database)
#             user_service = ctx.resolve(UserService)

#             with patch("daytistics.shared.services.MailService._send_email"):
#                 user = await user_service.register_user(
#                     UserRegistrationInput(
#                         email="test@example.com",
#                         password="password",
#                         username="testuser",
#                     )
#                 )

#             async with database.get_async_session() as session:
#                 user.is_verified = True
#                 session.add(user)
#                 await session.commit()
#                 await session.refresh(user)

#             variables = {"email": "test@example.com", "password": "password"}

#             query = """#graphql
#                 mutation LoginUser($email: String!, $password: String!) {
#                     loginUser(email: $email, password: $password) {
#                         user {
#                             email
#                             username
#                             isVerified
#                         },
#                         jwt {
#                             access
#                             refresh
#                         }
#                     }
#                 }
#             """

#             result = await gql_schema.execute(query, variable_values=variables)

#             assert result.data is not None
#             data = result.data.get("loginUser")

#             assert data is not None

#             user_data = data.get("user")

#             assert user_data == {
#                 "email": user.email,
#                 "username": user.username,
#                 "isVerified": user.is_verified,
#             }

#             jwt_data = data.get("jwt")

#             assert jwt_data is not None
#             assert jwt_data.get("access") is not None
#             assert jwt_data.get("refresh") is not None
