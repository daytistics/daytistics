from typing import Optional

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
    id: int
    username: str
    email: str
    hashed_password: str
    is_verified: bool
    is_locked: bool
    is_superuser: bool
    last_login: Optional[str]
    date_joined: Optional[str]
    created_at: str
    updated_at: str


@strawberry.type
class JWTType:
    access: str
    refresh: str
