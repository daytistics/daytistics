from datetime import datetime
from enum import Enum

import jwt
from passlib.context import CryptContext

from daytistics.settings import AppSettings, JwtSettings
from daytistics.exceptions import ConfigurationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CryptoService:
    class TokenType(Enum):
        ACCESS_TOKEN = "access"
        REFRESH_TOKEN = "refresh"
        ACCOUNT_VERIFICATION = "verify"
        PASSWORD_RESET = "reset"
        ACCOUNT_DELETION = "deletion"

    def __init__(self, app_settings: AppSettings, jwt_settings: JwtSettings) -> None:
        self.SECRET_KEY = app_settings.SECRET_KEY
        self.ALGORITHM = jwt_settings.ALGORITHM

    def generate_jwt_token(
        self,
        token_type: TokenType,
        sub: int,
        exp: datetime,
    ):
        payload = {
            "sub": str(sub),
            "type": token_type.value,
            "exp": exp,
        }

        if self.SECRET_KEY is None:
            raise ConfigurationError("SECRET_KEY is not set")

        return jwt.encode(
            payload,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM,
        )

    def decode_token(self, token: str) -> dict | None:
        if self.SECRET_KEY is None:
            raise ConfigurationError("SECRET_KEY is not set")

        try:
            return jwt.decode(
                token,
                self.SECRET_KEY,
                algorithms=[self.ALGORITHM],
            )
        except jwt.PyJWTError:
            return None

    def get_hash(self, text: str) -> str:
        return pwd_context.hash(text)

    def verify_hash(self, plain_text: str, hashed_text: str) -> bool:
        return pwd_context.verify(plain_text, hashed_text)
