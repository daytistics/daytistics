from os import environ

from typing import Optional


def _env_string_to_list(value: str) -> list[str]:
    return value.split(",")


class SecurityConfig:
    SECRET_KEY: Optional[str] = environ.get("SECRET_KEY")

    # JWT
    JWT_AUTH_ALGORITHM: str = environ.get("JWT_AUTH_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    )
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(
        environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7)
    )
    EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES: int = int(
        environ.get("EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES", 60 * 24)
    )

    # CORS
    CORS_ALLOW_ORIGINS: list[str] = _env_string_to_list(
        environ.get("CORS_ALLOW_ORIGINS", "*")
    )
    CORS_ALLOW_CREDENTIALS: bool = (
        environ.get("CORS_ALLOW_CREDENTIALS", "true") == "true"
    )
    CORS_ALLOW_METHODS: list[str] = _env_string_to_list(
        environ.get("CORS_ALLOW_METHODS", "GET,POST,PUT,DELETE")
    )
    CORS_ALLOW_HEADERS: list[str] = _env_string_to_list(
        environ.get("CORS_ALLOW_HEADERS", "*")
    )


class DatabaseConfig:
    DATABASE_URL: str = environ.get("DATABASE_URL", "sqlite:///./db.sqlite")
