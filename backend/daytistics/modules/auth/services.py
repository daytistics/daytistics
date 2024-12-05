from typing import Annotated
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends
from passlib.context import CryptContext

from daytistics.config import SecurityConfig
from daytistics.exceptions import ConfigurationError
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticationService:
    def generate_access_token(
        self, user: User, config: Annotated[SecurityConfig, Depends()]
    ) -> str:
        exp = datetime.now(timezone.utc) + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": str(user.id),
            "type": "access",
            "exp": exp,
        }

        if config.SECRET_KEY is None:
            raise ConfigurationError("SECRET_KEY is not set")

        return jwt.encode(
            payload, config.SECRET_KEY, algorithm=config.JWT_AUTH_ALGORITHM
        )

    def generate_refresh_token(
        self, user: User, config: Annotated[SecurityConfig, Depends()]
    ) -> str:
        exp = datetime.now(timezone.utc) + timedelta(
            minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": str(user.id),
            "type": "refresh",
            "exp": exp,
        }

        if config.SECRET_KEY is None:
            raise ConfigurationError("SECRET_KEY is not set")

        return jwt.encode(
            payload, config.SECRET_KEY, algorithm=config.JWT_AUTH_ALGORITHM
        )

    def decode_token(
        self, token: str, config: Annotated[SecurityConfig, Depends()]
    ) -> dict | None:
        if config.SECRET_KEY is None:
            raise ConfigurationError("SECRET_KEY is not set")

        try:
            return jwt.decode(
                token, config.SECRET_KEY, algorithms=[config.JWT_AUTH_ALGORITHM]
            )
        except jwt.PyJWTError as error:
            return None

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
