from typing import Optional, TypeVar
import functools
from collections.abc import Sequence

from pydantic_settings import BaseSettings, SettingsConfigDict
import dotenv

TSettings = TypeVar("TSettings", bound=BaseSettings)


@functools.cache
def _load_dotenv_once() -> None:
    dotenv.load_dotenv()


def get_settings(cls: type[TSettings]) -> TSettings:
    _load_dotenv_once()
    return cls()


class AppSettings(BaseSettings):
    SECRET_KEY: Optional[str] = None


class JwtSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JWT_")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    EMAIL_TOKEN_EXPIRE_MINUTES: int = 60 * 24


class CorsSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CORS_")
    ALLOW_ORIGINS: list[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_HEADERS: list[str] = ["*"]


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")
    URL: str = "sqlite+aiosqlite:///db.sqlite"
    ECHO: bool = False


class MailSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MAIL_")


settings_classes: Sequence[type[BaseSettings]] = [
    AppSettings,
    JwtSettings,
    CorsSettings,
    DatabaseSettings,
    MailSettings,
]
