from typing import Optional

from pydantic import EmailStr

import strawberry


@strawberry.input
class UserRegistrationInput:
    username: str
    email: str
    password: str


@strawberry.input
class UserLoginInput:
    email: str
    password: str


@strawberry.type
class UserType:
    id: Optional[int]
    username: str
    email: str
    is_verified: bool
    is_locked: bool
    is_superuser: bool
    last_login: Optional[str]
    created_at: str
    # auth_provider: str
    # provider_user_id: Optional[str]


@strawberry.type
class JwtType:
    access: Optional[str]
    refresh: Optional[str]


@strawberry.type
class LoginResultType:
    user: UserType
    jwt: JwtType
