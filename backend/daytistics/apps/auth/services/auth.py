from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from daytistics.integrations.injections import container
from daytistics.config import SecurityConfig
from daytistics.exceptions import ConfigurationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticationService:
    """
    The authentication service provides methods to generate secure tokens and hash passwords.
    It also provides a method to verify hashed passwords.
    It is commonly used in combination with the user service to authenticate users.
    """

    def __init__(self) -> None:
        with container.sync_context() as ctx:
            self.security_config = ctx.resolve(SecurityConfig)

    def generate_access_token(self, sub: int) -> str:
        exp = datetime.now(timezone.utc) + timedelta(
            minutes=self.security_config.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": str(sub),
            "type": "access",
            "exp": exp,
        }

        if self.security_config.SECRET_KEY is None:
            raise ConfigurationError("SECRET_KEY is not set")

        return jwt.encode(
            payload,
            self.security_config.SECRET_KEY,
            algorithm=self.security_config.JWT_AUTH_ALGORITHM,
        )

    def generate_refresh_token(self, sub: int) -> str:
        exp = datetime.now(timezone.utc) + timedelta(
            minutes=self.security_config.REFRESH_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": str(sub),
            "type": "refresh",
            "exp": exp,
        }

        if self.security_config.SECRET_KEY is None:
            raise ConfigurationError("SECRET_KEY is not set")

        return jwt.encode(
            payload,
            self.security_config.SECRET_KEY,
            algorithm=self.security_config.JWT_AUTH_ALGORITHM,
        )

    def decode_token(self, token: str) -> dict | None:
        if self.security_config.SECRET_KEY is None:
            raise ConfigurationError("SECRET_KEY is not set")

        try:
            return jwt.decode(
                token,
                self.security_config.SECRET_KEY,
                algorithms=[self.security_config.JWT_AUTH_ALGORITHM],
            )
        except jwt.PyJWTError:
            return None

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
