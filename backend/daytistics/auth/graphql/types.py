from typing import Optional

import strawberry


@strawberry.type()
class UserType:
    id: int
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    last_login: Optional[str]
    date_joined: Optional[str]


@strawberry.type
class JWTType:
    access: str
    refresh: str
