from typing import AsyncGenerator

from sqlmodel import Session


async def get_session() -> AsyncGenerator[Session, None]:
    """
    Get a session from the database.

    Returns:
        Generator[Session, None, None]: A session from the database.
    """
    from daytistics.database import engine

    with Session(engine) as session:
        yield session
