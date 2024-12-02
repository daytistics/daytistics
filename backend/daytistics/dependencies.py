from typing import AsyncGenerator

from sqlmodel import Session

strawberry_sqlalchemy_mapper = None


async def get_session() -> AsyncGenerator[Session, None]:
    """
    Get a session from the database.

    Returns:
        Generator[Session, None, None]: A session from the database.
    """
    from daytistics.database import engine

    with Session(engine) as session:
        yield session


def get_authentification_service():
    """
    Get the authentification service.

    Returns:
        Any: The authentification service.
    """
    from daytistics.auth import Auth

    return Auth()
