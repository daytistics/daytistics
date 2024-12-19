from typing import Dict, Any
import json

import strawberry
from aioinject import Injected
from aioinject.ext.strawberry import inject

from daytistics.domains.users.schemas import (
    UserRegistrationInput,
    UserType,
    LoginResultType,
    JwtType,
)
from daytistics.domains.users.services import UserService, AuthenticationService


@strawberry.type
class Mutation:
    @strawberry.mutation
    @inject
    async def register_user(
        self,
        user: UserRegistrationInput,
        user_service: Injected[UserService],
    ) -> UserType:
        created_user = await user_service.register_user(user)
        return UserType(
            **created_user.model_dump(
                include={field for field in UserType.__annotations__.keys()}
            )
        )

    @strawberry.mutation
    @inject
    async def verify_user(
        self,
        token: str,
        user_service: Injected[UserService],
    ) -> UserType:
        user = await user_service.verify_user(token)

        # stringify the data
        return UserType(
            **user.model_dump(
                include={field for field in UserType.__annotations__.keys()}
            )
        )

    @strawberry.mutation
    @inject
    async def login_user(
        self,
        email: str,
        password: str,
        user_service: Injected[UserService],
        auth_service: Injected[AuthenticationService],
    ) -> LoginResultType:
        user = await user_service.login_user(email, password)
        access_token = await auth_service.generate_access_token(user)
        refresh_token = await auth_service.generate_refresh_token(user)

        return LoginResultType(
            user=UserType(
                **user.model_dump(
                    include={field for field in UserType.__annotations__.keys()}
                )
            ),
            jwt=JwtType(access=access_token, refresh=refresh_token),
        )
