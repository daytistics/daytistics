from datetime import datetime

from ninja import Schema


class UserRegisterRequest(Schema):
    username: str
    email: str
    password1: str
    password2: str


class UserLoginRequest(Schema):
    email: str
    password: str


class JwtTokensResponse(Schema):
    accessToken: str
    refreshToken: str


class UserProfileResponse(Schema):
    username: str
    email: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    groups: list[str]
    user_permissions: list[str]
    date_joined: datetime
    last_login: datetime
